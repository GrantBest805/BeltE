from __future__ import unicode_literals
import re, datetime, bcrypt
from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def reg(self, data):
        errors = []
        # start of form data validations
        # first name validation
        if len(data['first_name']) < 3:
            errors.append("First name must be more then two characters.")
        if not data ['first_name'].isalpha():
            errors.append("First name must contain only letters.")
        # last name validation
        if len(data['last_name']) < 3:
            errors.append("Last name must be more then two characters.")
        if not data ['last_name'].isalpha():
            errors.append("Last name must contain only letters.")
        # email validation
        if data['email'] == "":
            errors.append("Email cannot be blank.")
        if not EMAIL_REGEX.match(data['email']):
            errors.append("Please enter a valid email address.")
        # check if email in database
        try:
            User.objects.get(email=data['email'])
            errors.append("Email is already registered.")
        except:
            pass

        # password validation
        if len(data['password']) < 8:
            errors.append("Email must be at least eight characters.")
        if data['password'] != data['confirm']:
            errors.append("Passwords do not match.")

        # end of validations
        if len(errors) == 0:
            data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            new_user = User.objects.create(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=data['password'])

            return {
                'new': new_user,
                'error_list': None
            }

        else:
            print(errors)
            return {
                'new': None,
                'error_list': errors
            }
    def login(self, log_data):
        errors = []

        try:
            found_user = User.objects.get(email=log_data['email'])
#            print(found_user.values())
            if bcrypt.hashpw(log_data['password'].encode('utf-8'), found_user.password.encode('utf-8')) != found_user.password.encode('utf-8'):
                errors.append("Incorrect password.")

        except:
            errors.append("Email address is not registered")
        if len(errors) == 0:
            return {
                'log_user': found_user,
                'list_errors': None
            }
        else:
            return {
                'log_user': None,
                'list_errors': errors
            }
class TripManager(models.Manager):
    def trip_info(self, trip_data):
        errors = []
        if trip_data['destination'] == "":
            errors.append("Can not leave blank!")
        if trip_data['description'] == "":
            errors.append("Can not leave blank!")

        if len(trip_data['trip_start']) == 0:
            errors.append("Can not leave blank")
        elif datetime.datetime.strptime(trip_data['trip_start'], '%Y-%m-%d') < datetime.datetime.now():
            errors.append("You do not have a time machine!")

        if len(trip_data['trip_finish']) == 0:
            errors.append("Can not leave blank")
        elif datetime.datetime.strptime(trip_data['trip_finish'], '%Y-%m-%d') <= datetime.datetime.strptime(trip_data['trip_start'], '%Y-%m-%d'):
            errors.append("You do not have a time machine!")

        print("********")
        if len(errors) == 0:
            user_id = User.objects.get(id=trip_data['id_user'])

            new_trip = Trip.objects.create(destination=trip_data['destination'], description=trip_data['description'], trip_start=trip_data['trip_start'], trip_finish=trip_data['trip_finish'], user_id=user_id)
            print(new_trip)
            return {
                'this_trip': new_trip,
                'the_errors': None
            }
        else:
            return {
                'this_trip': None,
                'the_errors': errors
            }



class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.TextField()
    trip_start = models.DateField()
    trip_finish = models.DateField()
    buddies = models.ManyToManyField(User, related_name="users_trips")
    user_id = models.ForeignKey(User, related_name="trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TripManager()
