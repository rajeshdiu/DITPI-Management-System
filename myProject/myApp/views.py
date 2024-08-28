from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from myApp.models import *
from myApp.forms import *

from django.contrib import messages

# Create your views here.

def homepage(request):
    coursedata = CourseInfoModel.objects.all()
    categorydata = CourseCategoryModel.objects.all()
    studentdata = StudentModel.objects.all()
    batchdata = BatchInfoModel.objects.all()
    teacherdata = TeacherModel.objects.all()
    contactdata = WebsiteContactModel.objects.get(Imsuser = 'Authority')
    getcourseReview = ReviewModel.objects.filter(Status = 'Approved')
    
    
    coursecount = coursedata.count()
    studentcount = studentdata.count()
    teachercount = teacherdata.count()
    batchcount = batchdata.count()
    
    current_path = request.path
    
    #------No of Student in a Course
    coursestudent = []
    enrolledstudent = 0
    max_nostudent_course = []
    max_nostudent = 0
    for course in coursedata:
        nostudent = AdmittedCourseModel.objects.filter(CourseName=course).count()
        enrolledstudent += nostudent
        coursestudent.append({
            'course':course,
            'student':nostudent,
        })
        # Check if the current course has more students than the current maximum
        if nostudent > max_nostudent:
            max_nostudent = nostudent
            max_nostudent_course.append({
                'course': course,
                'student': nostudent,
            })
    
    context = {
        'teacherdata':teacherdata,
        'teachercount':teachercount,
        
        'coursestudent':coursestudent,
        'coursedata':coursedata,
        'coursecount':coursecount,
        'categorydata':categorydata,
        'max_nostudent_course':max_nostudent_course,
        
        'contactdata':contactdata,
        'batchdata':batchdata,
        'batchcount':batchcount,
        
        'studentcount':studentcount,
        'enrolledstudent':enrolledstudent,
        'path':current_path,
        
        'getcourseReview':getcourseReview,
        
    }
    return render(request,'common/homepage.html',context)

@login_required
def dashboard(request):
    coursedata = CourseInfoModel.objects.all()
    categorydata = CourseCategoryModel.objects.all()
    studentdata = StudentModel.objects.all()
    batchdata = BatchInfoModel.objects.all()
    teacherdata = TeacherModel.objects.all()
    admittedcourse = AdmittedCourseModel.objects.all()
    
    totalenrolledstudent = admittedcourse.count()
    totalteacher = teacherdata.count()
    totalbatch = batchdata.count()
    totalcourse = coursedata.count()
    
    combined_data = []
    
    for data in batchdata:
        enrolledstudent = AdmittedCourseModel.objects.filter(LearningBatch=data).count()
        combined_data.append({
            'batchdata': data, 
            'enrolledstudent': enrolledstudent,
        })
        
    #------------Student----------
    current_user = request.user
    coursefee=0
    payment=0
    studentcoursedata=AdmittedCourseModel.objects.filter(Courseuser=current_user)
    for batch in studentcoursedata:
        coursefee += int(batch.CourseFee)
        payment += int(batch.Payment)
    due = int(coursefee) - int(payment)
    

    spenttime = 0
    lecture = 0
    project = 0
    for batch in studentcoursedata:
        course = get_object_or_404(CourseInfoModel,CourseName =batch.LearningBatch.CourseName)
        spenttime += int(course.CourseDuration)
        lecture += int(course.Lecture)
        project += int(course.TotalProject)
    
    
    context = {
        'teacherdata':teacherdata,
        'coursedata':coursedata,
        'categorydata':categorydata,
        'studentdata':studentdata,
        'totalenrolledstudent':totalenrolledstudent,
        'totalteacher':totalteacher,
        'totalbatch':totalbatch,
        'totalcourse':totalcourse,
        'combined_data':combined_data,
        
        #------Student---------
        'studentcoursedata':studentcoursedata,
        'coursefee':coursefee,
        'payment':payment,
        'due':due,
        'spenttime':spenttime,
        'lecture':lecture,
        'project':project,
    }
    
    return render(request,'common/dashboard.html',context)

def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('dashboard')
        else:
            return redirect('loginpage')
        
    
    return render(request, 'common/login.html')



def signupPage(request):
    error_messages = {
        'password_error': 'Password and Confirm Password not match',
    }
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        pass1 = request.POST.get("password")
        pass2 = request.POST.get("confirmpassword")
        UserType=request.POST.get("UserType")

        if pass1!= pass2:
             messages.error(request, error_messages['password_error'])
        else:
            # Use your customUser model to create a user
            myuser = CustomUserModel.objects.create_user(
                username=uname,
                email=email,
                password=pass1,
                UserType=UserType,
                )
            myuser.save()
            return redirect("loginpage")

    messages.success(request, 'Signup successful.')
    return render(request,'common/SignupPage.html')


@login_required
def logoutPage(request):
    request.user
    logout(request)
    return redirect('homepage')

def teachers(request):
    teacherdata = TeacherModel.objects.all()
    contactdata = WebsiteContactModel.objects.get(Imsuser = 'Authority')
    current_path = request.path
    context = {
        'pagetitle':'Meet with Our Makers',
        'subtitle':'Trainers',
        'teacherdata':teacherdata,
        'contactdata':contactdata,
        'path':current_path,
    }
    return render(request,'common/teachers.html',context)


def courses(request):
    coursedata = CourseInfoModel.objects.all()
    contactdata = WebsiteContactModel.objects.get(Imsuser = 'Authority')
    
    #------No of Student in a Course
    coursestudent = []
    for course in coursedata:
        nostudent = AdmittedCourseModel.objects.filter(CourseName=course).count()
        coursestudent.append({
            'course':course,
            'student':nostudent,
        })
    current_path = request.path
    context = {
        'pagetitle':'All Courses',
        'subtitle':'Courses',
        'coursedata':coursedata,
        'coursestudent':coursestudent,
        'contactdata':contactdata,
        'path':current_path,
    }
    
    return render(request,'common/courses.html',context)

def coursedetails(request, myid):
    coursedata = get_object_or_404(CourseInfoModel, id=myid)
    contactdata = WebsiteContactModel.objects.get(Imsuser = 'Authority')
    studentcount = AdmittedCourseModel.objects.filter(CourseName = coursedata).count()
    all_courses = CourseInfoModel.objects.all()
    getcourseReview = ReviewModel.objects.filter(CourseName=coursedata,Status='Approved')
    print(getcourseReview)
    
    context = {
        'pagetitle':coursedata,
        'subtitle':'Course',
        'coursedata':coursedata,
        'contactdata':contactdata,
        'studentcount':studentcount,
        'getcourseReview': getcourseReview,
        'all_courses': all_courses,
    }
    
    return render(request,'common/coursedetails.html',context)

def batches(request):
    batchdata = BatchInfoModel.objects.all()
    contactdata = WebsiteContactModel.objects.get(Imsuser = 'Authority')
    current_path = request.path
    context = {
        'pagetitle':'All Batches',
        'subtitle':'Batches',
        'headtitle': 'List of All Batches',
        'contactdata':contactdata,
        'batchdata':batchdata,
        'path':current_path,
    }
    
    return render(request,'common/batches.html',context)

def batchdetails(request, myid):
    batchdata = get_object_or_404(BatchInfoModel, id = myid)
    contactdata = WebsiteContactModel.objects.get(Imsuser = 'Authority')
    studentcount = AdmittedCourseModel.objects.filter(LearningBatch=batchdata).count()
    totalstudent = batchdata.TotalStudent
    remainstudent = int(totalstudent) - int(studentcount)
    current_path = request.path
    batchteachers = batchdata.BatchInstructor
    teachers_list = [teacher.strip() for teacher in batchteachers.split(',')]
    
    teacherinfo =[]
    for teacherid in teachers_list:
        teacher  = get_object_or_404(TeacherModel, EmployID = teacherid)
        teacherinfo.append({
            'EmployID': teacher.EmployID,
            'TeacherName': teacher.TeacherName,
            'Designation': teacher.Designation,
            'TeacherPhoto': teacher.TeacherPhoto.url if teacher.TeacherPhoto else None,
        })
        print(teacher.TeacherPhoto.url)

    
    context = {
        'batchdata':batchdata,
        'teacherinfo':teacherinfo,
        'pagetitle':'Batch Details',
        'subtitle':'Batches',
        'headtitle': 'Batch Details',
        'contactdata':contactdata,
        'studentcount':studentcount,
        'remainstudent':remainstudent,
        'path':current_path,
    }
    
    return render(request, 'common/batchdetails.html',context)

def upcommingbatch(request):
    batchdata = BatchInfoModel.objects.filter(Status='Upcomming')
    contactdata = WebsiteContactModel.objects.get(Imsuser = 'Authority')
    current_path = request.path
    context = {
        'pagetitle':'All Batches',
        'subtitle':'Batches',
        'headtitle': 'List of Upcomming Batches',
        'contactdata':contactdata,
        'batchdata':batchdata,
        'path':current_path,
    }
    
    return render(request,'common/upcommingbatch.html',context)

def ongoingbatch(request):
    batchdata = BatchInfoModel.objects.filter(Status='On-Going')
    contactdata = WebsiteContactModel.objects.get(Imsuser = 'Authority')
    current_path = request.path
    context = {
        'pagetitle':'All Batches',
        'subtitle':'Batches',
        'headtitle': 'List of On-Going Batches',
        'contactdata':contactdata,
        'batchdata':batchdata,
        'path':current_path,
    }
    
    return render(request,'common/ongoingbatch.html',context)

def completedbatch(request):
    batchdata = BatchInfoModel.objects.filter(Status='Completed')
    contactdata = WebsiteContactModel.objects.get(Imsuser = 'Authority')
    current_path = request.path
    context = {
        'pagetitle':'All Batches',
        'subtitle':'Batches',
        'headtitle': 'List of Completed Batches',
        'batchdata':batchdata,
        'contactdata':contactdata,
        'path':current_path,
    }
    
    return render(request,'common/completedbatch.html',context)

def contactpage(request):
    contactdata = WebsiteContactModel.objects.get(Imsuser = 'Authority')
    current_path = request.path
    context = {
        'pagetitle':'Contact US',
        'subtitle':'Contact',
        'contactdata':contactdata,
        'path':current_path,
    }
    return render(request,'contact/contact.html',context)

def applybatch(request, myid):
    batchdata = get_object_or_404(BatchInfoModel, BatchNo=myid)
    contactdata = WebsiteContactModel.objects.get(Imsuser = 'Authority')
    current_path = request.path
    coursename = batchdata.CourseName
    if request.method == "POST":
        applyform = PendingStudentForm(request.POST, request.FILES)
        if applyform.is_valid():
            applyform.save()
            messages.success(request,'Successfully Apply.')            
            return redirect('batches')
    else:
        initial_data = {'BatchNo': batchdata, 'CourseName':coursename}
        applyform = PendingStudentForm(initial=initial_data)
    
    context = {
        'pagetitle': 'Apply For Batch',
        'subtitle': 'Apply',
        'contactdata': contactdata,
        'path': current_path,
        'applyform': applyform,
        'batchdata':batchdata,
    }
    
    return render(request, 'common/applybatch.html', context)

#----------Review Section-------------
def reviewlist(request):
    reviewdata = ReviewModel.objects.all()
    context={
        'reviewdata':reviewdata        
    }
    return render(request,'common/reviewlist.html',context)

def deletereview(request, myid):
    reviewdata = get_object_or_404(ReviewModel, id=myid)
    reviewdata.delete()
    messages.success(request,'Successfully Deleted')    
    return redirect('reviewlist')

def approvereview(request,myid):
    reviewdata = get_object_or_404(ReviewModel, id=myid)
    if reviewdata.Status == 'Approved':
        messages.warning(request,'Review already approved.') 
    else:  
        reviewdata.Status = 'Approved'
        reviewdata.save()
    return redirect('reviewlist')

def categorydetails(request, myid):
    categorydata = CourseCategoryModel.objects.get(id = myid)
    categoryname = categorydata.CategoryName
    
    coursedata = CourseInfoModel.objects.filter(CourseCategory = categorydata)
    print("course data: ",coursedata)
    contactdata = WebsiteContactModel.objects.get(Imsuser = 'Authority')
    
    #------No of Student in a Course
    coursestudent = []
    for course in coursedata:
        nostudent = AdmittedCourseModel.objects.filter(CourseName=course).count()
        coursestudent.append({
            'course':course,
            'student':nostudent,
        })
    current_path = request.path
    context = {
        'pagetitle':categoryname,
        'subtitle':'Courses',
        'coursedata':coursedata,
        'coursestudent':coursestudent,
        'contactdata':contactdata,
        'path':current_path,
    }
    
    return render(request,'common/categorydetails.html',context)

def coursereview(request):
    if request.method == 'POST':
        courseid = request.POST.get('courseid')
        reviewtext = request.POST.get('reviewtext')
        courseName = request.POST.get('courseName')
        current_user = request.user

        admittedcoursedata = AdmittedCourseModel.objects.filter(Courseuser=current_user).exists()
        courseinfo = get_object_or_404(CourseInfoModel, CourseName=courseName)
        userdata = get_object_or_404(StudentModel, Imsuser=current_user)
        
        if admittedcoursedata:
            reviewdata = ReviewModel(
                Imsuser=userdata, 
                CourseName=courseinfo,
                Review=reviewtext,
            )
            reviewdata.save()
            messages.success(request, 'Review Submitted Successfully.')
            return redirect('coursedetails', myid=courseid)
        else:
            messages.warning(request, 'You are not admitted to this course.')

    return redirect('courses')  # Redirect to courses or any appropriate view


def teacherattendenceList(request):
    teacherattendancedata = TeacherAttendance.objects.all().order_by('-date_time')
    
    context = {
        'teacherattendancedata':teacherattendancedata,
    }
    
    return render(request,'common/teacherattendancelist.html',context)

def rejectattendance(request,myid):
    teacherdata = get_object_or_404(TeacherAttendance, id=myid)
    teacherdata.Attendance = 'Absent'
    teacherdata.save()
    
    return redirect('teacherattendenceList')

def accpetattendance(request,myid):
    teacherdata = get_object_or_404(TeacherAttendance, id=myid)
    teacherdata.Attendance = 'Present'
    teacherdata.save()
    
    return redirect('teacherattendenceList')