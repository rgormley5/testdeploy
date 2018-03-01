from django.shortcuts import render, HttpResponse, redirect
from .models import User, Destination
from django.contrib import messages
import bcrypt
from datetime import datetime

# Create your views here.

def index(request):
    print "in index route"

    return redirect('/main')

def main(request):
    print "in main route"

    return render(request, 'login/index.html')

def registration(request):
    print "in registration route"
    if request.method == "POST":
        print "request.POST is: ", request.POST
        errors = User.objects.basic_validator(request.POST)
        if 'new_user' in errors:
            request.session['id'] = errors['new_user'].id
            request.session['action'] = request.POST['action']
            return redirect('/travels')
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
            request.session['name'] = errors['user'].name
            request.session['action'] = request.POST['action']
            return redirect('/travels')
        else:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags = tag)

            return redirect('/')

    else:
        print "redirecting to index"
        return redirect('/')

def logout(request):
    print "in logout route"

    request.session.clear()

    return redirect('/')

def travels(request):
    print "in success route"

    if 'id' in request.session:
        this_user = User.objects.get(id = request.session['id'])
        user_trips = this_user.plan.all()
        other_trips = Destination.objects.all().exclude(creator_id = request.session['id']).exclude(plans = request.session['id'])

        # myDate = datetime.now()
        # formatedDate = myDate.strftime("%m-%d-%Y ")
        # start_date = []

        if request.session['action'] == "registration":
            context = {
                "user": User.objects.get(id = request.session['id']),
                "message": "Successfully registered!",
                "user_trips": user_trips,
                "other_trips": other_trips,
                # "date": formatedDate,
            }
        if request.session['action'] == "login":
            context = {
                "user": User.objects.get(id = request.session['id']),
                "message": "Successfully logged in!",
                "user_trips": user_trips,
                "other_trips": other_trips,
                # "date": formatedDate,
            }
        return render(request, 'login/success.html', context)
    return redirect('/')

def add_destination(request):
    print "in add_destination route"

    return render(request, 'login/add.html')

def process_destination(request):
    print "in process_destination route"

    if request.method == "POST":
        errors = User.objects.destination_adder(request.POST)
        if 'new_location' in errors:
            return redirect('/travels')
        else:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags = tag)

            return redirect('/travels/add')

    return redirect('/travels')

def join_destination(request, id):
    print "in join_destination route"

    this_location = Destination.objects.get(id = id)
    this_user = User.objects.get(id = request.session['id'])
    this_user.plan.add(this_location)

    return redirect('/travels')

def view_destination(request, id):
    print "in view_destination route"

    this_location = Destination.objects.get(id = id)
    users = this_location.plans.all()

    print "****** this_location is: ", this_location

    context = {
        "location": this_location,
        "users": users
    } 

    return render(request, 'login/view.html', context)