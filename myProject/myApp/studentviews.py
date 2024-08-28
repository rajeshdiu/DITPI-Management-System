from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from myApp.forms import *
import secrets
import string
import os

#-------Random Password Generate------------
def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for i in range(length))
    return password


@login_required
def addstudent(request):
    password = generate_random_password()
    if request.method == 'POST':
        studentform = StudentForm(request.POST, request.FILES)
        personalform = PersonalInfoForm(request.POST)
        
        if studentform.is_valid():
            student = studentform.save(commit = False)
            studentid = student.StudentID
            usertype= 'Student'
            
            student_exists = CustomUserModel.objects.filter(username=studentid).exists()
            
            if not student_exists:
                studentuser = CustomUserModel.objects.create_user(username=studentid,password=password,UserType=usertype)
                studentuser.save()
                
                student.Imsuser=studentuser
                student.save()
                
                if personalform.is_valid():
                    personalinfo = personalform.save(commit = False)
                    personalinfo.Imsuser =studentuser
                    personalinfo.Password =password
                    personalinfo.save()
                    messages.success(request,'Successfully Added')
                    return redirect('studentList')
            else:
                messages.error(request,'User Already Exists')
    else:
        studentform = StudentForm()
        personalform = PersonalInfoForm()
    
    context = {
        'studentform':studentform,
        'personalform':personalform,
    }
    return render(request,'students/addstudent.html',context)

@login_required
def editstudent(request, myid):
    studentdata = get_object_or_404(StudentModel, id=myid)
    personaldata = get_object_or_404(PersonalInfoModel, Imsuser=studentdata.Imsuser)
    
    img = studentdata.StudentPhoto
    if request.method == 'POST':
        studentform = StudentForm(request.POST,request.FILES, instance=studentdata)
        personalform = PersonalInfoForm(request.POST,instance=personaldata)
        
        if studentform.is_valid() and personalform.is_valid():
            student = studentform.save(commit=False)
            image = student.StudentPhoto
            print(image)
            if image != img:
                os.remove(img.path)
                
            student.save()
            personalform.save()
            return redirect('studentList')
    else:           
        personalform = PersonalInfoForm(instance=personaldata)
        studentform = StudentForm(instance=studentdata)
    
    context = {
        'studentform': studentform,
        'personalform': personalform,
    }
    return render(request, 'students/editstudent.html', context)

@login_required
def studentlist(request):
    studentdata = StudentModel.objects.all()
    personaldata = PersonalInfoModel.objects.all()
    
    combined_data = [] 
    for student in studentdata:
        personal_info = personaldata.filter(Imsuser=student.Imsuser).first()
        combined_data.append({
            'student': student,
            'personal_info': personal_info
        })
    context = {
        'combined_data': combined_data,
        'studentdata': studentdata
    }
    return render(request,'students/studentlist.html',context)

@login_required
def deletestudent(request,myid):
    studentdata = get_object_or_404(StudentModel, id = myid)
    user = studentdata.Imsuser
    userdata = get_object_or_404(CustomUserModel,username = user)
    img = studentdata.StudentPhoto
    os.remove(img.path)
    userdata.delete()
    return redirect('studentList')

@login_required
def viewstudent(request):
    return render(request,'students/viewstudent.html')

#------------Enroll Course------------------
@login_required
def enrollcourse(request):
    if request.method == 'POST':
        courseenrollform = EnrollCourseForm(request.POST)
        if courseenrollform.is_valid():
            courseenroll = courseenrollform.save(commit=False)
            studentid = courseenroll.StudentID
            
            # Check if the student exists
            student_exists = CustomUserModel.objects.filter(username=studentid).exists()
            if student_exists:
                student = get_object_or_404(CustomUserModel, username=studentid)
                batchno = courseenroll.LearningBatch
                
                # Check if the student is already enrolled in the batch
                batch_exists = AdmittedCourseModel.objects.filter(Courseuser=student, LearningBatch=batchno).exists()
                if not batch_exists:
                    batchdata = get_object_or_404(BatchInfoModel, BatchNo=batchno)
                    courseenroll.CourseName = batchdata.CourseName
                    courseenroll.Courseuser = student
                    coursefee = courseenroll.CourseFee
                    pay = courseenroll.Payment
                    courseenroll.Due = int(coursefee) - int(pay)
                    courseenroll.save()
                    return redirect('enrollcourselist')
                else:
                    messages.warning(request,'Student already enrolled in this batch.')
            else:
                messages.warning(request,'Student does not exist.')
    else:
        courseenrollform = EnrollCourseForm()
    
    return render(request, 'students/enrollcourse.html', {'courseenrollform': courseenrollform})

@login_required
def enrollcourselist(request):
    coursedata = AdmittedCourseModel.objects.all()
    
    return render(request,'students/enrollcourselist.html',{'coursedata':coursedata})

@login_required
def editenrollcourse(request, myid):
    coursedata = get_object_or_404(AdmittedCourseModel,id=myid)
    batch= coursedata.LearningBatch
    if request.method == 'POST':
        courseenrollform = EnrollCourseForm(request.POST, instance=coursedata)
        if courseenrollform.is_valid():
            courseenroll = courseenrollform.save(commit=False)
            studentid = courseenroll.StudentID
            
            # Check if the student exists
            student_exists = CustomUserModel.objects.filter(username=studentid).exists()
            if student_exists:
                student = get_object_or_404(CustomUserModel, username=studentid)
                batchno = courseenroll.LearningBatch
                
                # Check if the student is already enrolled in the batch
                if batchno != batch:
                    batch_exists = AdmittedCourseModel.objects.filter(Courseuser=student, LearningBatch=batchno).exists()
                    if not batch_exists:
                        batchdata = get_object_or_404(BatchInfoModel, BatchNo=batchno)
                        courseenroll.CourseName = batchdata.CourseName
                        courseenroll.Courseuser = student
                        coursefee = courseenroll.CourseFee
                        pay = courseenroll.Payment
                        courseenroll.Due = int(coursefee) - int(pay)
                        courseenroll.save()
                        messages.success(request,'Successfully Updated.')
                        return redirect('enrollcourselist')
                    else:
                        messages.warning(request,'Student already enrolled in this batch.')
                        
                else:
                    courseenroll.Courseuser = student
                    coursefee = courseenroll.CourseFee
                    pay = courseenroll.Payment
                    courseenroll.Due = int(coursefee) - int(pay)
                    courseenroll.save()
                    messages.success(request,'Successfully Updated.')
                    
                    return redirect('enrollcourselist')
            else:
                messages.warning(request,'Student does not exist.')
    else:
        courseenrollform = EnrollCourseForm(instance=coursedata)
        
    return render(request, 'students/enrollcourse.html', {'courseenrollform': courseenrollform})

@login_required
def deleteenrollcourse(request,myid):
    coursedata = get_object_or_404(AdmittedCourseModel,id=myid)
    coursedata.delete()
    messages.success(request,'Enrolled Student Deleted')
    
    return redirect('enrollcourselist')

@login_required
def pendingstudentlist(request):
    pendingdata = PendingStudentModel.objects.all()
    
    context = {
        'pendingdata':pendingdata,
    }
    
    return render(request,'students/pendingstudentlist.html',context)

@login_required
def editpendingstudent(request, myid):
    studentdata = get_object_or_404(PendingStudentModel, id=myid)
    btcno = studentdata.BatchNo
    batchdata = get_object_or_404(BatchInfoModel, BatchNo=btcno)
    password = generate_random_password()
    
    initial_data = {
        'StudentName': studentdata.StudentName,
        'StudentPhoto': studentdata.StudentPhoto,
        'EducationalQualification': studentdata.EducationalQualification,
        'Religion': studentdata.Religion,
        'FatherName': studentdata.FatherName,
        'MotherName': studentdata.MotherName,
        'DOB': studentdata.DOB,
        'Gender': studentdata.Gender,
        'Mobile': studentdata.Mobile,
        'EmergencyContact': studentdata.EmergencyContact,
        'PresentAddress': studentdata.PresentAddress,
        'PermanentAddress': studentdata.PermanentAddress,
        'LearningBatch': batchdata,
    }

    if request.method == 'POST':
        studentform = StudentForm(request.POST, request.FILES)
        personalform = PersonalInfoForm(request.POST)
        courseenrollform = PendingEnrollCourseForm(request.POST)
        
        studentform.initial['StudentPhoto'] = initial_data['StudentPhoto']
        if studentform.is_valid() and personalform.is_valid() and courseenrollform.is_valid():
            student = studentform.save(commit=False)
            studentid = student.StudentID
            usertype = 'Student'
            
            student_exists = CustomUserModel.objects.filter(username=studentid).exists()
            
            if not student_exists:
                studentuser = CustomUserModel.objects.create_user(username=studentid, password=password, UserType=usertype)
                studentuser.save()
                student.Imsuser = studentuser
                student.save()
                
                #----------Personal info model Section--------------
                personalinfo = personalform.save(commit=False)
                personalinfo.Imsuser = studentuser
                personalinfo.Password = password
                personalinfo.save()
                
                #----------Admitted Course Section--------------
                courseenroll = courseenrollform.save(commit=False)
                batchno = courseenroll.LearningBatch
                batch_exists = AdmittedCourseModel.objects.filter(Courseuser=studentuser, LearningBatch=batchno).exists()
                if not batch_exists:
                    batchdata = get_object_or_404(BatchInfoModel, BatchNo=batchno)
                    courseenroll.CourseName = batchdata.CourseName
                    courseenroll.CourseName = batchdata.CourseName
                    courseenroll.Courseuser = studentuser
                    courseenroll.StudentID = studentid
                    coursefee = courseenroll.CourseFee
                    pay = courseenroll.Payment
                    courseenroll.Due = int(coursefee) - int(pay)
                    courseenroll.save()
                    
                    studentdata.delete()             
                    
                    messages.success(request, 'Successfully Added')
                    return redirect('pendingstudentlist')
                else:
                    messages.error(request, 'Batch Already Exists')
            else:
                messages.error(request, 'User Already Exists')
        else:
            messages.error(request, 'Form is not valid')
        
        # If the POST request didn't result in a redirect, re-render the form with errors
        context = {
            'studentform': studentform,
            'personalform': personalform,
            'courseenrollform': courseenrollform,
        }
        return render(request, 'students/editpendingstudent.html', context)
    
    else:
        studentform = StudentForm(initial=initial_data)
        personalform = PersonalInfoForm(initial=initial_data)
        courseenrollform = PendingEnrollCourseForm(initial=initial_data)
        context = {
            'studentform': studentform,
            'personalform': personalform,
            'courseenrollform': courseenrollform,
        }
        
        return render(request, 'students/editpendingstudent.html', context)

@login_required
def deletependingstudent(request, myid):
    studentdata = get_object_or_404(PendingStudentModel, id = myid)
    studentdata.delete()
    messages.success(request, 'Successfully Deleted')
    return redirect('pendingstudentlist')

@login_required
def studentAttendance(request):
    context = {}

    if request.method == 'POST':
        if 'date' in request.POST:
            date = request.POST['date']
            batch_no = request.POST['batch_no']
            if not date:
                return render(request, 'students/studentAttendance.html', {
                    'error': 'Date is required',
                    'searchform': searchBatchForm(),
                    'batchno': batch_no,
                    'combined_data': combined_data
                })
            try:
                batchinfo = get_object_or_404(BatchInfoModel, BatchNo=batch_no)
                
                for student in request.POST:
                    if student.startswith('attendance_'):
                        student_id = student.split('_')[1]
                        attendance_value = request.POST[student]
                        
                        student_instance = get_object_or_404(StudentModel, StudentID=student_id)
                        attendance_record = StudentAttendanceModel(
                            Student=student_instance,
                            Attendance=attendance_value,
                            BatchNo=batchinfo,
                            Date=date
                        )
                        attendance_record.save()
                return redirect('teacherbatchinfo')  # Redirect to a success page or the same page with a success message
            
            except ValidationError:
                context['error'] = 'Invalid date format. Please use YYYY-MM-DD format.'
        else:
            # Process batch search form submission
            searchform = searchBatchForm(request.POST)
            if searchform.is_valid():
                batchno = searchform.cleaned_data['batch']
                batchinfo = get_object_or_404(BatchInfoModel, BatchNo=batchno)
                enrolldata = AdmittedCourseModel.objects.filter(LearningBatch=batchinfo)
                
                combined_data = []
                for data in enrolldata:
                    studentid = data.StudentID
                    studentdata = StudentModel.objects.get(StudentID=studentid)
                    combined_data.append({
                        'enrolldata': enrolldata,
                        'studentdata': studentdata,
                    })
                
                context = {
                    'searchform': searchform,
                    'batchinfo': batchinfo,
                    'batchno': batchno,
                    'combined_data': combined_data,
                }
    else:
        searchform = searchBatchForm()
        
        context = {
            'searchform': searchform,
        }
    
    return render(request, 'students/studentAttendance.html', context)

@login_required
def studentInfo(request):
    current_user=request.user
    studentdata=get_object_or_404(StudentModel,Imsuser=current_user)
    context={
        'studentdata':studentdata,
    }
    return render(request,'students/studentInfo.html',context)

@login_required
def studentbatches(request):
    current_user = request.user
    batchdata=AdmittedCourseModel.objects.filter(Courseuser=current_user)

    spenttime = 0
    lecture = 0
    project = 0
    for batch in batchdata:
        course = get_object_or_404(CourseInfoModel,CourseName =batch.LearningBatch.CourseName)
        spenttime += int(course.CourseDuration)
        lecture += int(course.Lecture)
        project += int(course.TotalProject)
        
    context = {
        'batchdata':batchdata,
        'spenttime':spenttime,
        'lecture':lecture,
        'project':project,
    }
    
    return render(request,'students/studentbatches.html',context)
@login_required
def studentongoingbatch(request):
    current_user = request.user
    coursedata=AdmittedCourseModel.objects.filter(Courseuser=current_user)

    for batch in coursedata:
        batchdata = BatchInfoModel.objects.filter(Status = 'On-Going')

    context = {
        'batchdata':batchdata,
    }
    
    return render(request,'students/studentongoginbatch.html',context)

@login_required
def studentPayment(request):
    current_user = request.user
    coursefee=0
    payment=0
    coursedata=AdmittedCourseModel.objects.filter(Courseuser=current_user)
    for batch in coursedata:
        coursefee += int(batch.CourseFee)
        payment += int(batch.Payment)
    due = int(coursefee) - int(payment)
    context = {
        'coursedata':coursedata,
        'coursefee':coursefee,
        'payment':payment,
        'due':due,
    }
    return render(request,'students/studentPayment.html',context)

@login_required
def studentAttendancelist(request):
    current_user = request.user
    studentdata = get_object_or_404(StudentModel, StudentID=current_user)

    allattendance = StudentAttendanceModel.objects.filter(Student=studentdata).order_by('-Date')
    
    context = {
        'allattendance': allattendance,
    }
    return render(request, 'students/studentattendancelist.html', context)