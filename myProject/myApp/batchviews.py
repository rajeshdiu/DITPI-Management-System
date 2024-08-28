from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from myApp.models import *
from myApp.forms import *

@login_required
def addbatch(request):
    if request.method == 'POST':
        batchform = BatchInfoForm(request.POST)
        
        if batchform.is_valid():
            batch = batchform.save(commit=False)
            batchteacher = batch.BatchInstructor
            batchno = batch.BatchNo
            teachers_list = [teacher.strip() for teacher in batchteacher.split(',')]
            len(teachers_list)
            teacher_instances = []
            for teacherid in teachers_list:
                try:
                    teacher_instance = TeacherModel.objects.get(EmployID=teacherid)
                    teacher_instances.append(teacher_instance)
                except TeacherModel.DoesNotExist:
                    messages.error(request, "Teacher Id not exists.")
                    return render(request, "batches/addbatch.html", {
                        'batchform': batchform,
                    })
                
                if len(teachers_list) == len(teacher_instances):
                    batch.save()
                    batchdata = get_object_or_404(BatchInfoModel, BatchNo=batchno)
                    for teacher_instance in teacher_instances:
                        teacherassign = TeacherBatchModel(
                            teacheruser= teacher_instance,
                            batch=batchdata,
                        )
                        teacherassign.save()

                    return redirect('batchlist')
    else:
        batchform = BatchInfoForm()
    context = {
        'batchform':batchform,
    }
    return render(request,"batches/addbatch.html",context)

@login_required
def batchlist(request):
    batchdata = BatchInfoModel.objects.all()
    combined_data = []
    
    for data in batchdata:
        enrolledstudent = AdmittedCourseModel.objects.filter(LearningBatch=data).count()
        combined_data.append({
            'batchdata': data, 
            'enrolledstudent': enrolledstudent,
        })
        
    context = {
        'combined_data': combined_data
    }
    return render(request, "batches/batchlist.html", context)


@login_required
def editbatch(request,myid):
    batchdata= get_object_or_404(BatchInfoModel,id=myid)
    previousteacher = batchdata.BatchInstructor

    if request.method == 'POST':
        batchform = BatchInfoForm(request.POST,instance=batchdata)
        if batchform.is_valid():
            batch = batchform.save(commit=False)
            batchteacher = batch.BatchInstructor
            batchno = batch.BatchNo
            teachers_list = [teacher.strip() for teacher in batchteacher.split(',')]
            len(teachers_list)
            teacher_instances = []
            for teacherid in teachers_list:
                try:
                    teacher_instance = TeacherModel.objects.get(EmployID=teacherid)
                    teacher_instances.append(teacher_instance)
                except TeacherModel.DoesNotExist:
                    messages.error(request, "Teacher Id not exists.")
                    return render(request, "batches/addbatch.html", {
                        'batchform': batchform,
                    })
                
                if len(teachers_list) == len(teacher_instances):
                    #------Delete previous teachers------------
                    preteachers_list = [teacher.strip() for teacher in previousteacher.split(',')]
                    for preteacherid in preteachers_list:
                        preteacherdata = TeacherModel.objects.get(EmployID=preteacherid)
                        prebatchdata = BatchInfoModel.objects.get(BatchNo=batchno)
                        
                        preteacher_instance = TeacherBatchModel.objects.get(teacheruser= preteacherdata, batch=prebatchdata)
                        preteacher_instance.delete()
                    
                    batch.save()
                    batchdata = get_object_or_404(BatchInfoModel, BatchNo=batchno)
                    for teacher_instance in teacher_instances:
                        teacherassign = TeacherBatchModel(
                            teacheruser= teacher_instance,
                            batch=batchdata,
                        )
                        teacherassign.save()

                    return redirect('batchlist')
    else:
        batchform = BatchInfoForm(instance=batchdata)
    context = {
        'batchform':batchform,
    }
    return render(request,"batches/editbatch.html",context)

@login_required
def deletebatch(request,myid):
    batchdata= get_object_or_404(BatchInfoModel,id=myid)
    batchdata.delete()
    return redirect('batchlist')

@login_required
def viewbatch(request, myid):
    batchdata = get_object_or_404(BatchInfoModel, BatchNo=myid)
    enrolledstudent = AdmittedCourseModel.objects.filter(LearningBatch = batchdata)
    totalstudent = enrolledstudent.count()
    print("Enrolled data: ",enrolledstudent)
    
    combined_data = []
    for data in enrolledstudent:
        studentid = data.StudentID
        studentdata = StudentModel.objects.get(StudentID = studentid)
        combined_data.append({
            'enrolldata':data,
            'studentdata':studentdata,
        })
        
    context = {
        'batchdata':batchdata,
        'totalstudent':totalstudent,
        'enrolledstudent':enrolledstudent,
        'combined_data':combined_data,
    }
    return render(request,"batches/viewbatch.html",context)     
