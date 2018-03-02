from django.shortcuts import render, HttpResponse, redirect
from .models import User, Quote
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
            return redirect('/quotes')
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
            return redirect('/quotes')
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

def quotes(request):
    print "in quotes route"

    if 'id' in request.session:
        this_user = User.objects.get(id = request.session['id'])
        fav_list = this_user.list.all()
        # other_list = Quote.objects.all().exclude(adder_id = request.session['id']).exclude(lists = request.session['id'])
        other_list = Quote.objects.all().exclude(lists = request.session['id'])

        if request.session['action'] == "registration":
            context = {
                "user": User.objects.get(id = request.session['id']),
                "message": "Successfully registered!",
                "fav_list": fav_list,
                "other_list": other_list,
            }
        if request.session['action'] == "login":
            context = {
                "user": User.objects.get(id = request.session['id']),
                "message": "Successfully logged in!",
                "fav_list": fav_list,
                "other_list": other_list,
            }
        return render(request, 'login/success.html', context)
    return redirect('/')

def process_quote(request):
    print "in process_quote route"

    if request.method == "POST":
        errors = User.objects.quote_adder(request.POST)
        if 'new_quote' in errors:
            return redirect('/quotes')
        else:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags = tag)

            return redirect('/quotes')

    return redirect('/quotes')

def add_quote(request, id):
    print "in add_qoute route"

    this_quote = Quote.objects.get(id = id)
    this_user = User.objects.get(id = request.session['id'])
    this_user.list.add(this_quote)

    return redirect('/quotes')

def remove_quote(request, id):
    print "in remove_quote route"

    this_quote = Quote.objects.get(id = id)
    this_user = User.objects.get(id = request.session['id'])
    remove_quote = this_user.list.remove(this_quote)
    this_quote.save()

    return redirect('/quotes')

def show_user(request, id):
    print "in show_user route"

    this_user = User.objects.get(id = request.session['id'])

    user_quotes = this_user.quotes.all()
    count = len(user_quotes)
    print "****** user_quotes is: ", user_quotes.all()

    context = {
        "user": this_user,
        "count": count,
        "user_quotes": user_quotes
    }

    return render(request, 'login/view.html', context)