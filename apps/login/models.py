from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['fname']) < 3:
            errors["fname"] = "fname must be at least 2 chars"
        if len(postData['lname']) < 3:
            errors["lname"] = "lname must be at least 2 chars"
        if len(postData['email']) < 1:
            errors["email"] = "email cannot be blank"
        if len(postData['password']) < 1:
            errors["password"] = "password cannot be blank"
        if len(postData['confirm']) < 1:
            errors["confirm"] = "confirm cannot be blank"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "invalid email format"
        if not postData['password'] == postData['confirm']:
            errors["password"] = "passwords must match"
        if len(errors) == 0:
            hash_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            new_user = User.objects.create(fname = postData['fname'], lname = postData['lname'], email = postData['email'], password = hash_pw)
            errors['new_user'] = new_user
        return errors

    def login_validator(self, postData):
        errors = {}
        hash1 = User.objects.filter(email = postData['login_email'])
        if hash1:
            if bcrypt.checkpw(postData['login_password'].encode(), hash1[0].password.encode()):
                errors['user'] = hash1[0]
            else:
                errors['invalid_password'] = "invalid password"
        else:
            errors['no_email'] = "email not found"
        return errors

class User(models.Model):
    fname = models.CharField(max_length = 50)
    lname = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()