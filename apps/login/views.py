from django.shortcuts import render, HttpResponse, redirect
from .models import User, Item
from django.contrib import messages
import bcrypt

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
            return redirect('/dashboard')
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
            return redirect('/dashboard')
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

def dashboard(request):
    print "in success route"

    if 'id' in request.session:
        all_items = Item.objects.all()
        if request.session['action'] == "registration":
            context = {
                "user": User.objects.get(id = request.session['id']),
                "message": "Successfully registered!",
                "all_items": all_items 
            }
        if request.session['action'] == "login":
            context = {
                "user": User.objects.get(id = request.session['id']),
                "message": "Successfully logged in!",
                "all_items": all_items 
            }
        print "all_items is: ", all_items
        return render(request, 'login/success.html', context)
    return redirect('/')

def add_item(request):
    print "in add_item route"

    return render(request, 'login/add.html')

def process_item(request):
    print "in process_item route"

    if request.method == "POST":
        errors = User.objects.item_adder(request.POST)
        if 'new_item' in errors:
            return redirect('/dashboard')
        else:
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags = tag)

            return redirect('/wish_items/create')

def remove(request):
    print "in remove route"


    return redirect('/dashboard')

def delete(request):
    print "in delete route"

    # item = Item.objects.get(id = id)
    # item.delete()

    return redirect('/dashboard')

def view_item(request, id):
    print "in show_item route"

    this_item = Item.objects.get(id = id)
    users = User.objects.filter(items = this_item)

    print "users is: ", users

    context = {
        "item": this_item,
        "users": users
    }

    return render(request, 'login/view.html', context)

def add_list(request, id):
    print "in add_list route"

    item = Item.objects.get(id = id)
    owner = User.objects.get(id = request.session['id'])

    Item.objects.create(name = item.name, owner = owner)

    return redirect('/dashboard')

# def remove_list(request, id):
#     print "in remove_list route"

#     item = Item.objects.get(id = id)
#     item.delete()
    
#     return redirect('/dashboard')