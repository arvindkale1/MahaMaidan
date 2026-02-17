from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Turf, Booking

def home(request):
    return render(request,'index.html')

def user_login(request):
    if request.method=="POST":
        user=authenticate(username=request.POST['username'],
                          password=request.POST['password'])
        if user:
            login(request,user)
            return redirect('turf_list')
    return render(request,'login.html')

def register(request):
    if request.method=="POST":
        User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password'])
        return redirect('login')
    return render(request,'register.html')

@login_required
def turf_list(request):
    return render(request,'turf_list.html',{'turfs':Turf.objects.all()})

@login_required
def book_turf(request,turf_id):
    if request.method=="POST":
        Booking.objects.create(
            user=request.user,
            turf_id=turf_id,
            date=request.POST['date'],
            time_slot=request.POST['time_slot'])
        return redirect('turf_list')
    return render(request,'book_turf.html')
