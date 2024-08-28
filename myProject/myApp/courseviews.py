from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from myApp.forms import *
import os

#------------Course Category---------
@login_required
def categorylist(request):
    categorydata = CourseCategoryModel.objects.all()
    
    return render(request,'courses/categorylist.html',{'categorydata':categorydata})

@login_required
def addcategory(request):
    if request.method == 'POST':
        categoryform = CourseCategoryForm(request.POST)
        if categoryform.is_valid():
            categoryform.save()
            return redirect('categorylist')
    else:
        categoryform = CourseCategoryForm()
    
    return render(request,'courses/addcategory.html',{'categoryform':categoryform})

@login_required
def editcategory(request,myid):
    categorydata = get_object_or_404(CourseCategoryModel, id=myid)
    if request.method == 'POST':
        categoryform = CourseCategoryForm(request.POST, instance=categorydata)
        if categoryform.is_valid():
            categoryform.save()
            return redirect('categorylist')
    else:
        categoryform = CourseCategoryForm(instance=categorydata)
    return render(request,'courses/editcategory.html',{'categoryform':categoryform})

@login_required
def deletecategory(request,myid):
    categorydata = get_object_or_404(CourseCategoryModel,id=myid)
    categorydata.delete()
    return redirect('categorylist')

#------------Admin Courses-------------
@login_required
def addcourse(request):
    if request.method == 'POST':
        courseform=CourseInfoForm(request.POST, request.FILES)
        if courseform.is_valid():
            courseform.save()
            return redirect('courselist')           
    else:
        courseform=CourseInfoForm()
    
    context = {
        'courseform':courseform,
    }
    return render(request,'courses/addcourse.html',context)

@login_required
def courselist(request):
    coursedata = CourseInfoModel.objects.all()
    context = {
        'coursedata':coursedata
    }
    return render(request,'courses/courselist.html',context)

@login_required
def editcourse(request,myid):
    coursedata = get_object_or_404(CourseInfoModel,id=myid)
    img = coursedata.CourseImage
    if request.method == 'POST':
        courseform = CourseInfoForm(request.POST, request.FILES, instance=coursedata)
        if courseform.is_valid():
            course = courseform.save(commit=False)
            image = course.CourseImage
            if image != img:
                os.remove(img.path)
            course.save()
            return redirect('courselist')
    else:
        courseform = CourseInfoForm(instance=coursedata)
    context = {
        'courseform':courseform,
    }
    return render(request,'courses/editcourse.html',context)

@login_required
def deletecourse(request,myid):
    coursedata = get_object_or_404(CourseInfoModel,id=myid)
    img = coursedata.CourseImage
    os.remove(img.path)
    coursedata.delete()
    return redirect('courselist')

@login_required
def viewcourse(request):
    return render(request,'courses/viewcourse.html')

