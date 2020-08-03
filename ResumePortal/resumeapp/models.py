# -*- coding: utf-8 -*-
#from import unicode_literals

from django.db import models

# Create your models here.
# Create your models here.
class Resume(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=12)
    email_address = models.CharField(max_length=50)
    education = models.CharField(max_length=50)
    technical_skillset = models.CharField(max_length=200)
    work_experience = models.CharField(max_length=20)
    employment_authorization = models.CharField(max_length=10)

    def __str__(self):
        return self.first_name+self.last_name+self.address+self.phone_number+self.email_address+self.education+self.technical_skillset+self.work_experience+self.employment_authorization