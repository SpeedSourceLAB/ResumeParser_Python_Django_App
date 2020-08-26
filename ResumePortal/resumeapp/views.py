# -*- coding: utf-8 -*-
import glob
import pandas
from . import models
import docx
import os
from docx import Document
import json
from .models import Resume
from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from pyresparser import ResumeParser

# Open upload page
def upload_page(request):
    print ("First Page")
    return render(request, 'resumeapp/Upload_Screen.html')

#Open job search page
def job_search(request):
    print ("Job Search Page")
    return render(request, 'resumeapp/Job_Search.html')

#Open  the applicant details page
def applicant_file(request):
    print ("Second Page ")

    if request.method== 'POST':
        #Get the uploaded file
        fileuploaded = request.FILES['file1']
        fs = FileSystemStorage()
        fs.save(fileuploaded.name, fileuploaded)

        list_of_files = glob.glob(
            'C:\\Users\\prade\\PycharmProjects\\ResumePortal\\media\\*')  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        print(latest_file)

        # Parse the uploaded resume
        parsed_details = ResumeParser(latest_file).get_extracted_data()
        print(parsed_details)
        resume_dict =  parsed_details

        # Converting to JSON
        loaded_json = json.loads(json.dumps(resume_dict))
        print(loaded_json)

        # converting into .JSON file for .HTML
        with open('C:\\Users\\prade\\PycharmProjects\\ResumePortal\\resumeapp\\templates\\resumeapp\\Doc_JSON2.json',
                  'w') as fp:
            json.dump(loaded_json, fp)
        return render(request, 'resumeapp/Applicant_Screen.html')

#Getparsed Details from second page and store in DB
def uploaded_to_db(request):
    print ("Third Page")

    #Get parsed details from applicant page
    if request.method=='POST':
        fn = request.POST.get('name')
        ln = request.POST.get('lname')
        add = request.POST.get('addr')
        ph = request.POST.get('mobile_number')
        email = request.POST.get('email')
        edu = request.POST.get('degree')
        tech = request.POST.get('skills')
        wrk = request.POST.get('total_experience')
        emp = request.POST.get('visa_status')

        #Create new record
        newRecord = Resume(first_name=fn, last_name=ln, address=add, phone_number=ph, email_address=email,
                           education=edu, technical_skillset=tech, work_experience=wrk, employment_authorization=emp)
        #Save the new record in DB
        newRecord.save()
        return render(request, 'resumeapp/ThankYou_Screen.html')

# Diplay the requested list of jobs
def job_list(request):
    job_category = request.POST.get('jobcategory')
    job_loc = request.POST.get('joblocation')
    print(job_category,job_loc)
    pandas.set_option('display.max_columns', None)

    #Create pandas dataframe of provived csv
    df = pandas.read_csv('resumeapp\\templates\\resumeapp\\Jobs_Scrapped.csv')
    print(df.shape)

    #Search df with Searched Job Location & Job Category
    df = df.query('`Searched Job Location` == @job_loc & `Job Category` == @job_category')

    #Drop Duplicates
    df = df.drop_duplicates(subset=['Company Name'])

    #change the column names to lowercase and replace spaces with underscore
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
    print(df)

    # Create new df that shows the jobs with email address and phoneno.s at the beginning
    df1 = pandas.DataFrame()
    df1 = df1.append(df[(df["job_email"].notnull()) | (df["job_phone_no"].notnull())])
    df1 = df1.append(df[(df["job_email"].isnull()) & (df["job_phone_no"].isnull())])

    data_dict=df1.to_dict('records')

    context = {
        'dict' : data_dict,
        'selected_category': job_category,
        'selected_location': job_loc
    }

    return render(request,'resumeapp/Job_Search_Results.html',context)