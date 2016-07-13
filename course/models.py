from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class AccountType(models.Model):
    owner=models.ForeignKey(User)
    actype=models.CharField(max_length=30)

class StudentsInformation(models.Model):
    owner=models.ForeignKey(User)
    fullname=models.CharField(max_length=64)
    qualification=models.CharField(max_length=16)
    university=models.CharField(max_length=64)
    phnenumber=models.CharField(max_length=15)
    country=models.CharField(max_length=32)


class TeacherInformation(models.Model):
    owner=models.ForeignKey(User)
    fullname=models.CharField(max_length=64)
    qualification=models.CharField(max_length=16)
    company=models.CharField(max_length=16)
    experience=models.IntegerField()
    phnenumber=models.CharField(max_length=12)
    country=models.CharField(max_length=32)

class Course(models.Model):
    owner=models.ForeignKey(TeacherInformation)
    coursename=models.CharField(max_length=64)
    startdate=models.DateField()
    enddate=models.DateField()
    requiredhours=models.IntegerField()
    description=models.TextField()

class StudentCourses(models.Model):
    courseid=models.ForeignKey(Course)
    studentid=models.ForeignKey(StudentsInformation)

class Assignments(models.Model):
    courseid=models.ForeignKey(Course)
    heading=models.CharField(max_length=64)
    content=models.TextField()
    duedate=models.DateField()

class Submissions(models.Model):
    studentid=models.ForeignKey(StudentsInformation)
    assignmentid=models.ForeignKey(Assignments)
    submissiondate=models.DateField()
    content=models.TextField()

class Grades(models.Model):
    studentid=models.ForeignKey(StudentsInformation)
    submissionid=models.ForeignKey(Submissions)
    grade=models.IntegerField()

class Posts(models.Model):
    courseid=models.ForeignKey(Course)
    heading=models.CharField(max_length=64)
    content=models.TextField()
