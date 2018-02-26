from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages
import bcrypt

# Create your views here.

def index(request):
    print "in index route"

    return render(request, 'login/index.html')

def registration(request):
    print "in registration route"
    print "request.method is:", request.method
    if request.method == "POST":
        errors = User.objects.basic_validator(request.POST)
        if 'new_user' in errors:
            request.session['id'] = errors['new_user'].id
            request.session['action'] = request.POST['action']
            return redirect('/success')
        else:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags = tag)

            return redirect('/')
    else:
        print "request.method == request.GET"
        return redirect('/')

def login(request):
    print "in login route"

    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if 'user' in errors:
            request.session['id'] = errors['user'].id
            request.session['first_name'] = errors['user'].fname
            return redirect('/success')
        else:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags = tag)

            return redirect('/')


        # if request.POST['action'] == "login":
        #     hash1 = User.objects.filter(email = request.POST['login_email'])
        #     request.session['id'] = hash1[0].id
        #     print "request.session['id'] is: ", request.session['id']
        #     print "hash1 is: ", hash1[0].password
        #     pw = request.POST['login_password']
        #     # if bcrypt.checkpw(pw.encode(), hash1[0].password.encode()):
        #         print "passwords match"
        #         return redirect('/success')
        #     else: 
        #         print "passwords don't match"
        #         return redirect('/')
    else:
        print "redirecting to index"
        return redirect('/')

def success(request):
    print "in success route"

    if request.session['action'] == "registration":
        context = {
            "user": User.objects.get(id = request.session['id']),
            "message": "Successfully registered!"
        }
    if request.session['action'] == "login":
        context = {
            "user": User.objects.get(id = request.session['id']),
            "message": "Successfully logged in!"
        }

    return render(request, 'login/success.html', context)