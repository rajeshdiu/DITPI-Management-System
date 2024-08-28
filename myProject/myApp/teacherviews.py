from django.shortcuts import render,redirect,get_object_or_404
from myApp.forms import *
from myApp.models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date, datetime
import secrets
import string
import os

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(length))
    return password

@login_required
def addteacher(request):
    password = generate_random_password()
    if request.method == 'POST':
        teacherform = TeacherForm(request.POST,request.FILES)
        personalform = PersonalInfoForm(request.POST)
        if teacherform.is_valid():
            teacher = teacherform.save(commit = False)
            teacherid = teacher.EmployID
            usertype = 'Teacher'
            
            teacher_exists = CustomUserModel.objects.filter(username=teacherid).exists()
            if not teacher_exists:
                teacheruser = CustomUserModel.objects.create_user(username=teacherid,password=password,UserType=usertype)
                teacheruser.save()

                teacher.Imsuser=teacheruser
                teacher.save()
                if personalform.is_valid():
                    personalinfo = personalform.save(commit = False)
                    personalinfo.Imsuser = teacheruser
                    personalinfo.Password =password
                    personalinfo.save()
                    messages.success(request,'Successfully Added')
                    return redirect('teacherlist')
            else:
                messages.error(request,'User Already Exists')
    else:
        teacherform = TeacherForm()
        personalform = PersonalInfoForm()
    
    context = {
        'teacherform': teacherform,
        'personalform': personalform,
    }
    return render(request,'teachers/addteacher.html',context) 


@login_required
def editteacher(request, teacherid):
    teacherdata = get_object_or_404(TeacherModel, id=teacherid)
    personaldata = get_object_or_404(PersonalInfoModel, Imsuser=teacherdata.Imsuser)
    img = teacherdata.TeacherPhoto
    
    if request.method == 'POST':
        teacherform = TeacherForm(request.POST, request.FILES, instance=teacherdata)
        personalform = PersonalInfoForm(request.POST, instance=personaldata)
        if teacherform.is_valid() and personalform.is_valid():
            # Ensure the EmployID is not changed
            teacher = teacherform.save(commit=False)
            teacherform.instance.EmployID = teacherdata.EmployID
            
            image = teacher.TeacherPhoto
            if image != img:
                os.remove(img.path)
            teacher.save()
            personalform.save()
            messages.success(request, 'Successfully Updated')
            return redirect('teacherlist')
    else:
        teacherform = TeacherForm(instance=teacherdata)
        personalform = PersonalInfoForm(instance=personaldata)
    
    context = {
        'teacherform': teacherform,
        'personalform': personalform,
    }
    
    return render(request, 'teachers/editteacher.html', context)
 


@login_required
def teacherlist(request):
    teacherdata = TeacherModel.objects.all()
    return render(request,'teachers/teacherlist.html',{'teacherdata':teacherdata}) 


@login_required
def deleteteacher(request,teacherid):
    teacherdata=  get_object_or_404(TeacherModel,id=teacherid)
    teacherdata.delete()
    messages.success(request,'Successfully Deleted')
    return redirect('teacherlist')


@login_required
def viewteacher(request):
    return render(request,'teachers/viewteacher.html') 

@login_required
def teacherpersonalinfo(request):
    current_user=request.user
    teacherinfo=get_object_or_404(TeacherModel,Imsuser=current_user)
    context={
        'teacherinfo':teacherinfo,
    }
    return render(request,'teachers/teacherpersonalinfo.html',context) 

@login_required
def teacherbatchinfo(request):
    current_user = request.user
    
    teacherdata = get_object_or_404(TeacherModel,Imsuser=current_user )
    teacherbatchdata=TeacherBatchModel.objects.filter(teacheruser=teacherdata)
    
    combined_data = []
    totalstudent = 0
    for i in teacherbatchdata:
        batchno = i.batch
        batchdata = get_object_or_404(BatchInfoModel, BatchNo = batchno)
        coursename = batchdata.CourseName
        
        #------ Enrolled Student Count-----------
        enrolledstudent = AdmittedCourseModel.objects.filter(CourseName = coursename).count()
        totalstudent += enrolledstudent
        combined_data.append({
            'teacherbatchdata':teacherbatchdata,
            'batchdata':batchdata,
            'enrolledstudent':enrolledstudent,
            
        })
        
    context = {
        'teacherbatchdata':teacherbatchdata,
        'combined_data':combined_data,
        'totalstudent':totalstudent,
    }

    return render(request,'teachers/teacherbatchinfo.html',context) 

@login_required
def teachersalaryinfo(request):
    return render(request,'teachers/teachersalaryinfo.html') 

@login_required
def teacherattendence(request):
    current_date = date.today() 
    current_user = request.user
    teacherdata = get_object_or_404(TeacherModel, EmployID=current_user)
    
    try:
        getattendance = TeacherAttendance.objects.filter(Teacher=teacherdata, Date=current_date).first()
        
    except TeacherAttendance.DoesNotExist:
        getattendance = None
    
    allattendance = TeacherAttendance.objects.filter(Teacher=teacherdata).order_by('-date_time')
    
    context = {
        'current_date': current_date,
        'getattendance': getattendance,
        'allattendance': allattendance,
    }
    return render(request, 'teachers/teacherattendence.html', context)

def submitattendance(request):
    current_date = date.today() 
    current_time = datetime.now()
    current_user = request.user
    teacherdata = get_object_or_404(TeacherModel, EmployID=current_user)
    attendance = 'Pending'
    
    data = TeacherAttendance(
        Teacher=teacherdata,
        Attendance=attendance,
        Date=current_date,
        date_time=current_time,
    )
    data.save()
    
    return redirect('teacherattendence')


    