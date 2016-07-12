"""courseproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import django
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login
from django.views.generic import TemplateView
from course.views import *
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^registration$',get_registrationform,name="registration"),
    url(r'^$',login,name="login"),
    url(r'^success/$',loginsuccess,name="success"),
    url(r'^studentform/$',studentform_fillup,name="studentform"),
    url(r'^teachersform/$',teacherform_fillup,name="teachersform"),
    url(r'^logoutuser/$',logout_view,name="logoutsuccess"),
    url(r'^courses/$',courselist,name="courselist"),
    url(r'^courses/(?P<id>[0-9]+)/$',coursedetails,name="coursedetail"),
    url(r'^courses/(?P<id>[0-9]+)/assignments/$',assignmentslist,name="assignmentslist"),
    url(r'^courses/(?P<id>[0-9]+)/assignments/(?P<pk>[0-9]+)/$',assignmentdetail,name="assignmentsdetail"),
    url(r'^mycourses/$',mycourseslist,name="mycourses"),
    url(r'^allcourses/$',allcourseslist,name="allcourselist"),
    url(r'^getteacher/(?P<id>[0-9]+)/$',teacherinfobasedoncourseid,name="teacherinfooncourseid"),
    url(r'^unenroll/(?P<id>[0-9]+)/$',unenrollcourse,name="unenrollcourse"),
    url(r'^submission/(?P<id>[0-9]+)/$',assignmentsubmission,name="assignmentsubmission"),
    url(r'^submittedstudents/(?P<id>[0-9]+)/$',getsubmittedstudentnames,name="getsubmittedstudentnames"),
    url(r'^submissions/(?P<sid>[0-9]+)/assignment/(?P<aid>[0-9]+)/$',getsubmissionbasedonassignmentidandstudentid,name="getsubmissionbasedonsidandaid"),
    url(r'^submitgrade/(?P<studentid>[0-9]+)/submission/(?P<submissionid>[0-9]+)/$',addgradetoserverwithstudentidandsubmissionid,name='addgrade'),
    url(r'^coursestudents/(?P<id>[0-9]+)/$',viewallstudentsincourse,name="viewallstudentsincourse"),
    url(r'^viewprogress/(?P<id>[0-9]+)/$',viewprogressofstudent,name="viewprogressofstudent"),
    url(r'^getgrade/(?P<id>[0-9]+)/$',getgradebasedonsubmissionid,name="getgrade"),
]
