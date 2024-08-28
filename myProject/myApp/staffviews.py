from django.shortcuts import render,redirect,get_object_or_404
from myApp.forms import *
from myApp.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import secrets
import string
import os

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(length))
    return password

@login_required
def addstaff(request):
    password = generate_random_password()
    if request.method == 'POST':
        staffform = StaffForm(request.POST, request.FILES)
        personalform = PersonalInfoForm(request.POST)
        
        if staffform.is_valid():
            staff = staffform.save(commit=False)
            EmployID = staff.EmployID
            userrtype = 'Staff'
            
            staff_exists = CustomUserModel.objects.filter(username=EmployID).exists()
            
            if not staff_exists:
                staffuser = CustomUserModel.objects.create_user(username=EmployID,password=password,UserType=userrtype)
                staffuser.save()
                
                staff.Imsuser=staffuser
                staff.save()
                
                if personalform.is_valid():
                    personalinfo = personalform.save(commit=False)
                    personalinfo.Imsuser = staffuser
                    personalinfo.Password =password
                    personalinfo.save()
                    messages.success(request,'Successfully Added')
                    return redirect('stafflist')
            else:
                messages.error(request,'User Already Exists')
            
    else:
        staffform = StaffForm()
        personalform = PersonalInfoForm()
        
    context = {
        'staffform':staffform,
        'personalform':personalform
    }
        
    return render(request,'staff/addstaff.html',context)

@login_required
def editstaff(request, myid):
    staffdata = get_object_or_404(StaffModel, id=myid)
    personaldata = get_object_or_404(PersonalInfoModel, Imsuser=staffdata.Imsuser)
    
    if request.method == 'POST':
        staffform = StaffForm(request.POST, request.FILES, instance=staffdata)
        personalform = PersonalInfoForm(request.POST, instance=personaldata)
        
        if staffform.is_valid() and personalform.is_valid():
            staffform.save()
            personalform.save()
            messages.success(request,'Successfully Updated')
            return redirect('stafflist')
    else:
        staffform = StaffForm(instance=staffdata)
        personalform = PersonalInfoForm(instance=personaldata)
        
    context={
        'staffform':staffform,
        'personalform':personalform,      
    }

    return render(request,'staff/editstaff.html',context)

@login_required
def deletestaff(request,myid):
    staffdata = get_object_or_404(StaffModel, id=myid)
    staffdata.delete()
    messages.success(request,'Successfully Deleted')
    return redirect('stafflist')

@login_required
def stafflist(request):
    staffdata = StaffModel.objects.all()
    staffdata={
        'staffdata':staffdata
    }
    
    return render(request,'staff/stafflist.html',staffdata)
@login_required
def viewstaff(request):
    return render(request,'staff/viewstaff.html')


