# -*- coding: utf-8 -*-
import glob

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

# Create your views here.
def upload_page(request):
    print ("First Page")
    return render(request, 'resumeapp/Upload_Screen.html')

#sample upload
def applicant_file(request):
    print ("Second Page")

    if request.method== 'POST':
        fileuploaded = request.FILES['file1']
        fs = FileSystemStorage()
        fs.save(fileuploaded.name, fileuploaded)

        list_of_files = glob.glob(
            'C:\\Users\\prade\\PycharmProjects\\ResumePortal\\media\\*')  # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)

        print(latest_file)
        data1 = ResumeParser(latest_file).get_extracted_data()

        resume_dict = {x.translate({32: None}): y
                       for x, y in list(data1.items())}

        print(resume_dict)

        # Converting to JSON
        loaded_json = json.loads(json.dumps(resume_dict))
        print(loaded_json)

        # converting into .JSON file for .HTML
        with open('C:\\Users\\prade\\PycharmProjects\\ResumePortal\\resumeapp\\templates\\resumeapp\\Doc_JSON2.json',
                  'w') as fp:
            json.dump(loaded_json, fp)
        return render(request, 'resumeapp/Applicant_Screen.html')

def uploaded_to_db(request):
    print ("Third Page")

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
        newRecord = Resume(first_name=fn, last_name=ln, address=add, phone_number=ph, email_address=email,
                           education=edu, technical_skillset=tech, work_experience=wrk, employment_authorization=emp)
        newRecord.save()
        return render(request, 'resumeapp/ThankYou_Screen.html')
