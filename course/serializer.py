from rest_framework import serializers

from course.models import *

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields=('id','owner','coursename','startdate','enddate','requiredhours','description')

class AssignmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Assignments
        fields=('id','courseid','heading','content','duedate')

class StudentCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentCourses
        fields=('id','courseid','studentid')

class TeacherInformationStudentView(serializers.ModelSerializer):
    class Meta:
        model=TeacherInformation
        fields=('id','fullname','qualification','company','experience','country')

class SubmissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Submissions
        fields=('id','assignmentid','studentid','submissiondate','content')

class StudentInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentsInformation
        fields=('id','fullname','qualification','university','country')

class GradesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Grades
        fields=('id','studentid','submissionid','grade')
