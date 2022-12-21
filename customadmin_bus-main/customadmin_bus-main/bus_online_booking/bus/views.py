from asyncio import transports
from asyncio.trsock import TransportSocket
from email import message
import email
from multiprocessing import context
from operator import add
from tracemalloc import start
# from pyexpat.errors import messages
from django.contrib import messages

from unicodedata import category
from urllib import request
from django import views

from django.shortcuts import render, redirect

from django.http import HttpResponse, JsonResponse

from django.views import *
from datetime import datetime


from .models import *

from django.contrib.auth.models import User, auth

# from django.contrib.auth import *


class Login(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
                    auth.login(request, user)
                    return render(request, 'userprofile.html')
        else:
            messages.info(request, 'Invalid input')
            return redirect('login')


class Register(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST['username']
        firstname = request.POST['fn']
        lastname = request.POST['ln']
        Email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username is Already Taken..')
            return redirect('register')
        elif User.objects.filter(email=Email).exists():
            messages.info(request, 'Email is Already Taken..')
            return redirect('register')

        elif password == confirmpassword :
                regi = User.objects.create_user(
                    first_name=firstname, last_name=lastname, email=Email, password=password, username=username)
                regi.save()
                return redirect('register')
        else :
            return redirect('register')






class Bookingbus(View):
    print('******************************')
    def get(self, request, id):
        print('******************************---------------------------------')

        transport = Transport.objects.filter(id=id)
        for transports in transport:
            t1 = transports.transport_name

        d = datetime.now()
        return render(request, 'booked_bus.html', {'t1': t1, 'date': d})

    def post(self, request, id):

        bus = Transport.objects.get(transport_name=request.POST['bus'])
        # busid=Booked_bus.objects.get(pk=id)
        pessengername = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        date = datetime.now()
        age = request.POST['age']

        busbooking = Booked_bus.objects.create(
            busname=bus, name=pessengername, address=address, phone=phone, book_date_time=date, age=age, user=request.user)
        busbooking.save()

        transport = Transport.objects.get(pk=id)
        busnumber = transport.number_plate
        price = transport.price_per_person
        context = {'bus': bus, 'pessengername': pessengername, 'address': address,
            'phone': phone, 'date': date, 'age': age, 'busnumber': busnumber, 'price': price}

        return render(request, 'ticketdetail.html', context)






             




    


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect('login')


class Userhome(View):
    def get(self, request):
        if Transport.objects.all().exists():
            return render(request, 'home.html')
        else:
            messages.info(
                request, '- - - - - - - - - - Sorry Bus Are not Available - - - - - - - - - -')
            return render(request, 'home.html')

    def post(self, request):
        start = request.POST['start1']
        end = request.POST['end1']
        date = request.POST['date1']
     
        journey = Journey.objects.filter(start_point=start, end_point=end)
        for i in journey:
            date_filter = i.transport.filter(date_time_dpt=date)
            for j in date_filter:
                id = j.id
                name = j.transport_name
                number_plate = j.number_plate
                seats_available = j.seats_available
                price_per_person = j.price_per_person
                category = j.bus_category
                bus_category = category.category
                date_time_dpt = j.date_time_dpt
        return JsonResponse({"id":id, "name":name, "number_plate":number_plate, "seats_available":seats_available, "price_per_person":price_per_person, "date_time_dpt":date_time_dpt, "bus_category":bus_category})




class Userprofile(View):
    def get(self, request):
        return render(request, 'userprofile.html')







class Cancleticket(View):

    def get(self, request):
        if request.user.is_authenticated:

                return render(request, 'canclebooking.html')

        else:
            return redirect('login')

    def post(self, request):
        phone = request.POST['phone']
        ph = Booked_bus.objects.filter(phone=phone)
        if phone != '':
            if Booked_bus.objects.filter(phone=phone).exists():
                return render(request, 'cancleticket.html', {'phn': ph})
            else:
              
                return redirect('canclebooking')
        else:
            return redirect('canclebooking   ')


class Deletepessenger(View):
     def get(self, request, id):
        if request.user.is_authenticated:
                delet = Booked_bus.objects.get(pk=id)
                delet.delete()
                return render(request, 'canclemessege.html')
        else:
            return redirect('login')


class Canclemessege(View):
        def get(self, request):
            if request.user.is_authenticated:
                return render(request, 'canclemessege.html')
            else:
                return redirect('login')


class Pessengerdetail(View):
        def get(self, request):
            if request.user.is_authenticated:
                detail = Booked_bus.objects.all()
                return render(request, 'showpessenger.html', {'detail': detail})
            else:
                return redirect('login')



        

class Registerhome(View):
    def get(self,request):
        return render(request,'ragisterhome.html')


class Createadmin(View):
    def get(self, request):
      
                    return render(request, 'createadmin.html')

    def post(self, request):
        username = request.POST['username']
        firstname = request.POST['fn']
        lastname = request.POST['ln']
        Email = request.POST['email']
        pass1 = request.POST['password']
        # pass2 = request.POST['confirmpassword']
        # staff=request.POST['admin']
        # print('***********',staff)
        if User.objects.filter(username=username).exists():
            messages.info(request, 'This Admin Username is Already Taken..')
            return redirect('createadmin')
        elif User.objects.filter(email=Email).exists():
            messages.info(request, 'Email is Already Taken..')
            return redirect('createadmin')

        else:
                regi = User.objects.create_user(first_name=firstname, last_name=lastname, email=Email,
        password=pass1, username=username, is_staff=True, is_superuser=True)
                regi.save()
                return redirect('createadmin')




                         




                
                
            

             
     
        



        





        

        


       


    

       
        


