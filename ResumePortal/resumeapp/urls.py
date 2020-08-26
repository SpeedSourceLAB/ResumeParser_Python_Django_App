from django.conf.urls import url
from django.contrib import admin
from .import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns =[
    url(r'^$', views.upload_page,name='upload-file'),
    url(r'^ApplicantDetails', views.applicant_file,name='upload-page2'),
    url(r'^Thankyou', views.uploaded_to_db,name='upload-page3'),
    url(r'^JobSearch', views.job_search, name='job-search'),
    url(r'^JobList', views.job_list, name='job-list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)