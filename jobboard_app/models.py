from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re

now = str(datetime.now())
EMAILREGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9_.+-]+.[a-zA-Z]+$')

class UserManager(models.Manager):

    def login_validator(self, postData):
        print(" i am in login validator-------!!!!!!!")
        print("POSTDATA is", postData)
        errors = {}
        
        #Email Validation
        if len(postData["login_email"]) < 1:
            print(" I am in less than 1 letter of email")
            errors["email"] = "email is required"
        elif not EMAILREGEX.match(postData['login_email']):
            errors['email']= "Email Address not valid"
        elif not User.objects.filter(email = postData["login_email"]):
            errors["email"] = "This email does not exist. Please register!"

        #Password Validation
        if len(postData['login_password']) < 1:
            errors['password'] = "password is required"

        return errors

# registration validator here
    def reg_validator(self, postData):
        print(" i am in reg validator-------!!!!!!!")
        print("POSTDATA is", postData)
        errors = {}
        
        if len(postData["name"]) < 1:
            errors["name"] = "name is required"

        #Email Validation
        if len(postData["email"]) < 1:
            print(" I am in less than 1 letter of email")
            errors["email"] = "email is required"
        elif not EMAILREGEX.match(postData['email']):
            errors['email']= "Email Address not valid"
        elif User.objects.filter(email = postData["email"]):
            errors["email"] = "This email is already registered. Please log in!"
        elif postData['password'] != postData['confirm_password']:
            errors["password_no_match"] = "Passwords do not match"

        #Password Validation
        if len(postData['password']) < 1:
            errors['password'] = "password is required"
        return errors


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255, default="")
    last_name = models.CharField(max_length=255, default="")
    email = models.CharField(max_length=255, default="")
    password = models.CharField(max_length=255, default="")
    admin = models.BooleanField(max_length=255, default=False)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    

    objects = UserManager()


class JobManager(models.Manager):
    def basic_validator(self, postData):
        print("POSTDATA is: ", postData)
        errors = {}
        #destination validation
        # if len(postData["destination"]) < 1:
        #     errors["destination"] = "destination is required"
        
        # #description validation
        # if len(postData["desc"]) < 1:
        #     errors["desc"] = "desc is required"

        print("About to return from basic validator")
        return errors


class Job(models.Model):
    company_name  = models.CharField(max_length=255, default="")
    company_location   = models.CharField(max_length=255, default="")
    job_description   = models.CharField(max_length=255, default="")
    job_technology   = models.CharField(max_length=255, default="")
    POC_name   = models.CharField(max_length=255, default="")
    POC_email  = models.CharField(max_length=255, default="")
    destination = models.CharField(max_length=255, default="")

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    

    #ONE TO MANY RELATIONSHIP
    added_by = models.ForeignKey(User, related_name="jobs", on_delete=models.CASCADE)

    objects = JobManager()

    #represent method
    def __repr__(self):
        return f"Job: {self.id} {self.comp_name}"

#MANY TO MANY RELATIONSHIP
class Saved(models.Model):
    user = models.ForeignKey(User, related_name="user_saving_jobs", on_delete=models.CASCADE)
    job = models.ForeignKey(Job, related_name="jobs_saved_by_users", on_delete=models.CASCADE)
