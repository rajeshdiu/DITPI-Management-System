from django import forms
from myApp.models import *

class CourseCategoryForm(forms.ModelForm):
    class Meta:
        model = CourseCategoryModel
        fields = "__all__"
        
        labels = {
            "CategoryName":"Category Name"
        }

class CourseInfoForm(forms.ModelForm):
    class Meta:
        model = CourseInfoModel
        fields = "__all__"
        
        labels = {
            "CourseName":"Course Name",
            "Lecture":"No of Lecture",
            "ShortSummary":"Short Summary",
            "CourseCategory":"Course Category",
            "CourseDuration":"Course Duration",
            "WeeklyClass":"Weekly Class",
            "ClassDuration":"Class Duration(in Minutes)",
            "TotalProject":"Total Project",
            "CourseOverview":"Course Overview",
            "CourseCurrriculum":"Course Currriculum",
            "Software":"Course Software",
            "CourseFor":"Course For",
            "JobPositions":"Job Positions",
            "CourseFee":"Course Fee",
            "IntroVideo":"Intro Video Link",
            "CourseImage":"Course Image",
        }
 
class EnrollCourseForm(forms.ModelForm):
    class Meta:
        model = AdmittedCourseModel
        fields = "__all__"  
        exclude = ['Courseuser','Studentuser','CourseName','AdmissionDate','Due']
        
        labels = {
            "LearningBatch":"Batch No",
            "CourseFee":"Course Fee",
        }    
class PendingEnrollCourseForm(forms.ModelForm):
    class Meta:
        model = AdmittedCourseModel
        fields = "__all__"  
        exclude = ['StudentID','Courseuser','Studentuser','CourseName','AdmissionDate','Due']
        
        labels = {
            "LearningBatch":"Batch No",
            "CourseFee":"Course Fee",
        }    
class AdmittedCourseForm(forms.ModelForm):
    class Meta:
        model = AdmittedCourseModel
        fields = "__all__"  
        exclude = ['StudentID','AdmissionDate','Due']
        
        labels = {
            "LearningBatch":"Batch No",
            "CourseFee":"Course Fee",
        }    

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfoModel
        fields = "__all__"
        exclude = ['Imsuser','Password']
        
        widgets = {
            'DOB':forms.DateInput(attrs={
                'type': 'date'
            }),
        }
        
        labels = {
            "FatherName": "Father Name",
            "MotherName": "Mother Name",
            "DOB": "Date of Birth",
            "EmergencyContact": "Emergency Contact",
            "PresentAddress": "Present Address",
            "PermanentAddress": "Permanent Address",
        }

class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentModel
        fields = "__all__"
        exclude = ['Imsuser','AdmissionDate','LinkedInLink','GithubLink','FacebookLink']
        
        widgets = {
            'AdmissionDate':forms.DateInput(attrs={
                'type':'date'
            }),
        }
        labels = {
            "StudentID":"Student ID No",
            "StudentName":"Student Name",
            "StudentPhoto":"Student Photo",
            "AdmissionDate":"Admission Date",
            "EducationalQualification":"Educational Qualification",
            "LinkedInLink":"LinkedIn Link",
            "GithubLink":"Github Link",
            "FacebookLink":"Facebook Link",
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = TeacherModel
        fields = "__all__"
        exclude = ['Imsuser','Skills','JoinDate','LinkedInLink','GithubLink','FacebookLink']
        labels = {
            "EmployID":"Teacher ID",
            "TeacherName":"Teacher Name",
            "LinkedInLink":"LinkedIn Link",
            "GithubLink":"Github Link",
            "FacebookLink":"Facebook Link",
            "JoinDate":"Join Date",
        }
        

    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['EmployID'].widget.attrs['readonly'] = True

    def clean_EmployID(self):
        if self.instance and self.instance.pk:
            return self.instance.EmployID
        return self.cleaned_data['EmployID']
    
class StaffForm(forms.ModelForm):
    class Meta:
        model = StaffModel
        fields = "__all__"
        exclude =["Imsuser","JoinDate"]
        labels = {
            "StaffName":"Staff Name",
            "EmployID":"Employ ID",
            "StaffDesignation":"Staff Designation",
            "StaffPhoto":"Staff Photo",
            "JoinDate":"Join Date",

        }
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['EmployID'].widget.attrs['readonly'] = True

    def clean_EmployID(self):
        if self.instance and self.instance.pk:
            return self.instance.EmployID
        return self.cleaned_data['EmployID']

class BatchInfoForm(forms.ModelForm):
    class Meta:
        model = BatchInfoModel
        fields = "__all__"

        widgets = {
            'BatchStartDate':forms.DateInput(attrs={
                'type':'date'
            }),
            'BatchNo': forms.TextInput(attrs={
                'placeholder': 'Example: 75'
            }),
            'Batchschedule': forms.TextInput(attrs={
                'placeholder': 'Example: Sat, Mon, Wed'
            }),
            'TotalStudent': forms.TextInput(attrs={
                'placeholder': 'Example: 25'
            }),
            'BatchInstructor': forms.TextInput(attrs={
                'placeholder': 'Example: 20012, 24022'
            }),
        }
        labels = {
            "BatchNo":"Batch No",
            "Batchschedule":"Batchs Schedule",
            "BatchStartDate":"Batch Start Date",
            "TotalStudent":"Total Seat",
            "BatchInstructor":"Instructor ID No",
            "CourseName":"Course Name",
        }

class WebsiteContacForm(forms.ModelForm):
    class Meta:
        model = WebsiteContactModel
        fields = "__all__"
        exclude = ['Imsuser']
        
        labels = {
            "MapLink": "Map Link",
            "GithubLink": "Linkedin Link",
            "FacebookLink": "Facebook Link",
            "YoutubeLink": "Youtube Link",
            "TwitterLink" : "Twitter Link",
        }

class PendingStudentForm(forms.ModelForm):
    class Meta:
        model = PendingStudentModel
        fields = "__all__"
        
        widgets = {
            'DOB':forms.DateInput(attrs={
                'type': 'date'
            }),
        }
        
        labels = {
            "CourseName": "Course Name",
            "FatherName": "Father Name",
            "MotherName": "Mother Name",
            "DOB": "Date of Birth",
            "EmergencyContact": "Emergency Contact",
            "PresentAddress": "Present Address",
            "PermanentAddress": "Permanent Address",
            "StudentName":"Student Name",
            "StudentPhoto":"Student Photo",
            "EducationalQualification":"Educational Qualification",
        }
        
        
        
    def __init__(self, *args, **kwargs):
        super(PendingStudentForm, self).__init__(*args, **kwargs)
        self.fields['BatchNo'].widget.attrs['readonly'] = True
        self.fields['CourseName'].widget.attrs['readonly'] = True

class searchBatchForm(forms.ModelForm):
    class Meta:
        model = TeacherBatchModel
        fields = "__all__"
        exclude = ['teacheruser']
