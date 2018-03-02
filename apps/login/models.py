from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
from datetime import datetime
from time import gmtime, strftime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# print datetime.now()
today = datetime.now()
formatedDate = today.strftime('%Y%m%d %h:%m:%s')

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        a = strftime('%Y-%m-%d', gmtime())
        if len(postData['name']) < 3:
            errors["name"] = "name must be at least 3 chars"
        if len(postData['alias']) < 1:
            errors["alias"] = "alias cannot be blank"
        if len(User.objects.filter(alias = postData['alias'])) > 0:
            errors["alias"] = "alias taken"
        if len(postData['email']) < 1:
            errors["alias"] = "email cannot be blank"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "invalid email format"
        if len(postData['password']) < 8:
            errors["password"] = "password must be at least 8 characters"
        if len(postData['confirm']) < 1:
            errors["confirm"] = "confirm cannot be blank"
        if not postData['password'] == postData['confirm']:
            errors["password"] = "passwords must match"
        if postData['dob'] > a:
            errors["invalid_date"] = "dob must be in the past"
        if len(errors) == 0:
            hash_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            new_user = User.objects.create(name = postData['name'], alias = postData['alias'], email = postData['email'], password = hash_pw, dob = postData['dob'])
            errors['new_user'] = new_user
        return errors

    def login_validator(self, postData):
        errors = {}
        hash1 = User.objects.filter(email = postData['email'])
        if hash1:
            if bcrypt.checkpw(postData['login_password'].encode(), hash1[0].password.encode()):
                errors['user'] = hash1[0]
            else:
                errors['invalid_password'] = "invalid password"
        else:
            errors['no_email'] = "invalid email"
        return errors

    def quote_adder(self, postData):
        errors = {}
        if len(postData['quoted_by']) < 1:
            errors["quoted_by"] = "Quoted By cannot be blank"
        if (len(postData['quoted_by']) > 1 and len(postData['quoted_by'])) < 3:
            errors["quoted_by_length"] = "Quoted By must be at least 3 characters"
        if len(postData['content']) < 1:
            errors["content"] = "Message name cannot be blank"
        if len(postData['content']) < 10:
            errors["content_length"] = "Message must be at least 10 characters"
        if len(errors) < 1:
            adder = User.objects.get(id = postData['adder'])
            new_quote = Quote.objects.create(content = postData['content'], quoted_by = postData['quoted_by'], adder = adder)
            errors['new_quote'] = new_quote
        return errors

class User(models.Model):
    name = models.CharField(max_length = 50)
    alias = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    dob = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()

class Quote(models.Model):
    content = models.TextField(max_length = 200)
    quoted_by = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)
    adder = models.ForeignKey(User, related_name = "quotes")
    lists = models.ManyToManyField(User, related_name = "list")