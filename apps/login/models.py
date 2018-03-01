from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# print datetime.now()
today = datetime.now()
formatedDate = today.strftime("%m-%d-%Y")

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 3:
            errors["name"] = "name must be at least 3 chars"
        if len(postData['username']) < 1:
            errors["username"] = "username cannot be blank"
        if len(User.objects.filter(username = postData['username'])) > 0:
            errors["username"] = "username taken"
        if len(postData['password']) < 8:
            errors["password"] = "password must be at least 8 characters"
        if len(postData['confirm']) < 1:
            errors["confirm"] = "confirm cannot be blank"
        if not postData['password'] == postData['confirm']:
            errors["password"] = "passwords must match"
        if len(errors) == 0:
            hash_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            new_user = User.objects.create(name = postData['name'], username = postData['username'], password = hash_pw)
            errors['new_user'] = new_user
        return errors

    def login_validator(self, postData):
        errors = {}
        hash1 = User.objects.filter(username = postData['username'])
        if hash1:
            if bcrypt.checkpw(postData['login_password'].encode(), hash1[0].password.encode()):
                errors['user'] = hash1[0]
            else:
                errors['invalid_password'] = "invalid password"
        else:
            errors['no_email'] = "invalid username"
        return errors

    def destination_adder(self, postData):
        errors = {}
        if len(postData['location']) < 1:
            errors["location"] = "location name cannot be blank"
        if len(postData['content']) < 1:
            errors["content"] = "Description name cannot be blank"
        if postData['start_date'] > postData['end_date']:
            errors["invalid_end_date"] = "start date cannot be after end date"

        # start_date = datetime.strptime(postData['start_date'], '%Y-%m-%d')
        # end_date = datetime.strptime(postData['end_date'], '%Y-%m-%d')
        # if start_date < datetime.date():
        #     errors["invalid_date"] = "dates must be furure dates"
        
        # if (postData['start_date'] or postData['end_date']) < datetime.now():
        #     errors["invalid_date"] = "dates must be furure dates"

        # if (postData['start_date'] or postData['end_date']) < datetime.date(int(formatedDate)):
        #     errors["invalid_date"] = "dates must be furure dates"
        
        # start_date = postData['start_date']
        # fstart = start_date.strftime("%m-%d-%Y")
        # end_date = postData['end_date']
        # fend = end_date.strftime("%m-%d-%Y")
        
        if len(errors) < 1:
            creator = User.objects.get(id = postData['adder'])
            new_location = Destination.objects.create(location = postData['location'], content = postData['content'], start_date = postData['start_date'], end_date = postData['end_date'], creator = creator)
            creator.plan.add(new_location)
            errors['new_location'] = new_location
        return errors

class User(models.Model):
    name = models.CharField(max_length = 50)
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()

class Destination(models.Model):
    location = models.CharField(max_length = 100)
    content = models.TextField(max_length = 200)
    created_at = models.DateTimeField(auto_now_add = True)
    start_date = models.DateField(auto_now_add = True)
    end_date = models.DateField(auto_now_add = True)
    creator = models.ForeignKey(User, related_name = "destinations")
    plans = models.ManyToManyField(User, related_name = "plan")