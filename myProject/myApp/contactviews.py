from django.shortcuts import render, redirect, get_object_or_404
from myApp.forms import *
from myApp.models import WebsiteContactModel

#------------Admin Contact----------
def addcontact(request):
    if request.method == 'POST':
        contactform = WebsiteContacForm(request.POST)
        if contactform.is_valid():
            contact = contactform.save(commit=False)
            contact.Imsuser = 'Authority'
            contact.save()
            return redirect('contactlist')
    else:    
        contactform = WebsiteContacForm()
    context = {
        'contactform':contactform,
     }
    return render(request,'contact/addcontact.html',context)

def contactlist(request):
    contactdata = WebsiteContactModel.objects.all()
    
    return render(request,'contact/contactlist.html',{'contactdata':contactdata})

def editcontact(request,myid):
    contactdata = get_object_or_404(WebsiteContactModel, id=myid)
    if request.method == 'POST':
        contactform = WebsiteContacForm(request.POST, instance=contactdata)
        if contactform.is_valid():
            contactform.save()
            return redirect('contactlist')
    else:
        contactform = WebsiteContacForm(instance=contactdata)
    context = {
        'contactform':contactform
    }
    return render(request,'contact/editcontact.html',context)

def deletecontact(request,myid):
    contactdata = get_object_or_404(WebsiteContactModel,id=myid)
    contactdata.delete()
    return redirect('contactlist')
    