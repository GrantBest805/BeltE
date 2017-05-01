from django.shortcuts import render, redirect, HttpResponse
from .models import User, Trip
from django.contrib import messages
from django.core.urlresolvers import reverse



def index(request):
    return render(request, 'belt/index.html')

def register(request):
    context = {
        'first_name': request.POST['first_name'],
        'last_name': request.POST['last_name'],
        'email': request.POST['email'],
        'password': request.POST['password'],
        'confirm': request.POST['confirm']
    }
    req_results = User.objects.reg(context)
    if req_results['new'] != None:
        request.session['user_id'] = req_results['new'].id
        request.session['user_first_name'] = req_results['new'].first_name
        return redirect(reverse('my_show'))
    else:
        print req_results['error_list']
        for error_str in req_results['error_list']:
            messages.add_message(request, messages.ERROR, error_str)

            return redirect(reverse('my_index'))


def travels(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, "You must be logged in to view this page.")
        return redirect(reverse('my_index'))
    current_user = User.objects.filter(id=request.session['user_id'])
    all_trips = Trip.objects.all().filter(buddies=current_user)
    context = {
    "user_trips": Trip.objects.all().filter(user_id=current_user),
    "others_trips": Trip.objects.all().exclude(user_id=current_user).exclude(buddies=current_user),
    "all_trips": all_trips
    }

    return render(request, 'belt/travels.html', context)
def login(request):

    p_data = {
        'email': request.POST['email'],
        'password': request.POST['password']
    }

    log_results = User.objects.login(p_data)
    if log_results['list_errors'] != None:
        for error in log_results['list_errors']:
            messages.add_message(request, messages.ERROR, error)
        return redirect(reverse('my_index'))
    else:
        request.session['user_id'] = log_results['log_user'].id
        request.session['user_first_name'] = log_results['log_user'].first_name
        return redirect(reverse('my_show'))

# log out function
def logout(request):
    request.session.clear()
    return redirect(reverse('my_index'))

def add_plan(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, "You must be logged in to view this page.")
        return redirect(reverse('my_index'))


    return render(request, 'belt/add_plan.html')

def add_trip(request):
    if request.method == "POST":
        trip_data = {
            'destination': request.POST['destination'],
            'description': request.POST['description'],
            'id_user': request.session['user_id'],
            'trip_start': request.POST['trip_start'],
            'trip_finish': request.POST['trip_finish'],

        }
        the_trip = Trip.objects.trip_info(trip_data)
        print(the_trip)
        if the_trip['the_errors'] != None:
            for error in the_trip['the_errors']:
                messages.add_message(request, messages.ERROR, error)
            return redirect(reverse('my_plan'))
        else:
            request.session['trip_id'] = the_trip['this_trip'].id
            request.session['user_id'] = the_trip['this_trip'].user_id.id

            return redirect(reverse('my_show'))
def destination(request, trip_id):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, "You must be logged in to view this page.")
        return redirect(reverse('my_index'))
    my_trips = Trip.objects.filter(id=trip_id)
    my_buddies = User.objects.filter(users_trips=my_trips)
    context = {
        'my_trips': my_trips,
        'my_buddies': my_buddies,
    }


    return render(request, 'belt/destination.html', context)

def join_trip(request, trip_id):
    join_user = User.objects.get(id=request.session['user_id'])
    join_trip = Trip.objects.get(id=trip_id)
    join_trip.buddies.add(join_user)

    return redirect(reverse('my_show'))
