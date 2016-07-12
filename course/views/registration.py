from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView

from course.forms import *
from course.models import *


def get_registrationform(request):
    if(request.method=='POST'):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password1=form.cleaned_data['password1']
            password2=form.cleaned_data['password2']
            accountType=form.cleaned_data['role']
            if password1==password2:
                User.objects.create_user(username,email,password1)
                AccountType.objects.create(actype=accountType,owner=User.objects.get(username=username))
                return HttpResponseRedirect("/")
    else:
        form=RegistrationForm()
    return render(request,'registration.html',{'form':form})

@login_required(login_url='/')
def loginsuccess(request):
    u=AccountType.objects.get(owner=request.user)
    if u.actype=='teacher':
        t=TeacherInformation.objects.filter(owner=request.user)
        a=t.__len__()
        if a==0:
            return HttpResponseRedirect("/teachersform")
        else:
            t=TeacherInformation.objects.get(owner=request.user)
            return render(request,'teachersuccesspage.html',{'role':t.fullname})
    else:
        s=StudentsInformation.objects.filter(owner=request.user)
        a=s.__len__()
        if a==0:
            return HttpResponseRedirect("/studentform")
        else:
            s=StudentsInformation.objects.get(owner=request.user)
            return render(request,"studentsuccesspage.html",{'role':s.fullname})

@login_required(login_url='/')
def studentform_fillup(request):
    actype=AccountType.objects.get(owner=request.user).actype
    if actype=='teacher':
        return HttpResponseRedirect("/success")
    u=StudentsInformation.objects.filter(owner=request.user.id)
    a=u.__len__()
    if a==0 :
        if(request.method=='POST'):
            form=StudentsInformationForm(request.POST)
            if form.is_valid():
                owner=request.user
                fullname=form.cleaned_data['fullname']
                qualification=form.cleaned_data['qualification']
                university=form.cleaned_data['university']
                phnenumber=form.cleaned_data['phonenumber']
                country=form.cleaned_data['country']
                StudentsInformation.objects.create(fullname=fullname,owner=owner,qualification=qualification,university=university,phnenumber=phnenumber,country=country)
                return HttpResponseRedirect("/success")
        else:
            form=StudentsInformationForm()
        return render(request,'studentsinfoinput.html',{'form':form})
    else:
        return HttpResponseRedirect("/success")

@login_required(login_url='/')
def teacherform_fillup(request):
    actype = AccountType.objects.get(owner=request.user).actype
    if actype == 'student':
        return HttpResponseRedirect("/success")
    u=TeacherInformation.objects.filter(owner=request.user)
    a=u.__len__()
    if a== 0 :
        if(request.method=='POST'):
            form=TeacherInformationForm(request.POST)
            if form.is_valid():
                owner=request.user
                fullname=form.cleaned_data['fullname']
                qualification=form.cleaned_data['qualification']
                company=form.cleaned_data['university']
                phnenumber=form.cleaned_data['phonenumber']
                country=form.cleaned_data['country']
                experience=form.cleaned_data['experience']
                TeacherInformation.objects.create(fullname=fullname,owner=owner,qualification=qualification,company=company,phnenumber=phnenumber,country=country,experience=experience)
                return HttpResponseRedirect("/success")
        else:
            form=TeacherInformationForm()
        return render(request,'teachersinfoinput.html',{'form':form})
    else:
        return HttpResponseRedirect("/success")
