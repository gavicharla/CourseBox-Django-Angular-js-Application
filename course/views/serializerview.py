from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from course.serializer import *
from course.models import *

@csrf_exempt
@login_required(login_url="login")
@api_view(['GET','POST'])
def courselist(request):
    if request.method=='GET':
        courses=Course.objects.filter(owner__owner=request.user)
        ser=CourseSerializer(courses,many=True)
        return Response(ser.data)
    elif request.method=='POST':
        data=request.data
        data['coursename'] = data['coursename'].upper()
        data['owner']=TeacherInformation.objects.get(owner=request.user).id
        ser=CourseSerializer(data=data)
        if ser.is_valid():
            ser.save()
            courses = Course.objects.filter(owner__owner=request.user)
            ser = CourseSerializer(courses, many=True)
            return Response(ser.data)
        else:
            return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@login_required(login_url="login")
@api_view(['GET','PUT','DELETE'])
def coursedetails(request,id):
    try:
        course=Course.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        t=CourseSerializer(course)
        return Response(t.data)
    elif request.method=='PUT':
        data=request.data
        data['coursename']=data['coursename'].upper()
        data['owner']=TeacherInformation.objects.get(owner=request.user).id
        ser=CourseSerializer(course,data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        course.delete()
        return  Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@login_required(login_url="login")
@api_view(['GET','POST'])
def assignmentslist(request,id):
    if request.method=='GET':
        assn=Assignments.objects.filter(courseid=id)
        ser=AssignmentsSerializer(assn,many=True)
        return Response(ser.data)
    elif request.method=='POST':
        data=request.data
        data['courseid']=id
        ser=AssignmentsSerializer(data=data)
        if ser.is_valid():
            ser.save()
            assn = Assignments.objects.filter(courseid=id)
            ser = AssignmentsSerializer(assn, many=True)
            return Response(ser.data)
        else:
            return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@login_required(login_url="login")
@api_view(['GET','PUT','DELETE'])
def assignmentdetail(request,id,pk):
    try:
        assn=Assignments.objects.get(id=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        s=AssignmentsSerializer(assn)
        return Response(s.data)
    elif request.method=='PUT':
        data=request.data
        data['courseid']=id
        s=AssignmentsSerializer(assn,data=data)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        assn.delete()
        return  Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@login_required(login_url="login")
@api_view(['GET','POST'])
def mycourseslist(request):
    try:
        stud = StudentsInformation.objects.get(owner=request.user)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        scobj=StudentCourses.objects.filter(studentid=stud.id)
        a=set()
        for i in scobj:
            a.add(i.courseid.id)
        courses=Course.objects.filter(id__in=a)
        ser=CourseSerializer(courses,many=True)
        return Response(ser.data)
    elif request.method=='POST':
        data=request.data
        id=data['courseid']
        try:
            c=Course.objects.get(id=id)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data['studentid']=stud.id
        try:
            s=StudentCourses.objects.get(Q(courseid=id) & Q(studentid=stud.id))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except:
            ser = StudentCoursesSerializer(data=data)
            if ser.is_valid():
                ser.save()
                scobj = StudentCourses.objects.filter(studentid=stud.id)
                a = set()
                for i in scobj:
                    a.add(i.courseid)
                courses = Course.objects.filter(id__in=a)
                ser = CourseSerializer(courses, many=True)
                return Response(ser.data)
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@login_required(login_url="login")
@api_view(['GET'])
def allcourseslist(request):
    if request.method=='GET':
        courses=Course.objects.all()
        ser=CourseSerializer(courses,many=True)
        return Response(ser.data)
    return Response(status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@login_required(login_url="login")
@api_view(['GET'])
def teacherinfobasedoncourseid(request,id):
    try:
        course=Course.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        owner=course.owner_id
        t=TeacherInformation.objects.get(id=owner)
        ser=TeacherInformationStudentView(t)
        return Response(ser.data)

@csrf_exempt
@login_required(login_url="login")
@api_view(['DELETE'])
def unenrollcourse(request,id):
    try:
        sid=StudentsInformation.objects.get(owner=request.user).id
        cid=id
        course=StudentCourses.objects.get(Q(courseid=cid) & Q(studentid=sid))
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='DELETE':
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@login_required(login_url="login")
@api_view(['GET','PUT','POST'])
def assignmentsubmission(request,id):
    try:
        sid = StudentsInformation.objects.get(owner=request.user).id
        aid=id
        sub=Submissions.objects.get(Q(assignmentid=aid) & Q(studentid=sid))
    except:
        if request.method=='POST':
            data=request.data
            data['studentid']=sid
            s=SubmissionsSerializer(data=data)
            if s.is_valid():
                s.save()
                return Response(s.data)
            return Response(s.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        s=SubmissionsSerializer(sub)
        return Response(s.data)
    elif request.method=='PUT':
        data = request.data
        data['assignmentid'] = aid
        data['studentid'] = sid
        s = SubmissionsSerializer(data=data)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors,status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@login_required(login_url="login")
@api_view(['GET'])
def getsubmittedstudentnames(request,id):
    subs=Submissions.objects.filter(assignmentid=id)
    if subs.__len__()==0:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        a = set()
        for i in subs:
            a.add(i.studentid.id)
        studs =StudentsInformation.objects.filter(id__in=a)
        ser=StudentInformationSerializer(studs,many=True)
        return Response(ser.data)
    return Response(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@login_required(login_url="login")
@api_view(['GET'])
def getsubmissionbasedonassignmentidandstudentid(request,sid,aid):
    try:
        sub=Submissions.objects.get(Q(studentid=sid) & Q(assignmentid=aid))
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        ser= SubmissionsSerializer(sub)
        return Response(ser.data)
    return Response(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@login_required(login_url="login")
@api_view(['POST'])
def addgradetoserverwithstudentidandsubmissionid(request,studentid,submissionid):
    try:
        g=Grades.objects.get(Q(studentid=studentid) & Q(submissionid=submissionid))
    except:
        if request.method=='POST':
            data=request.data
            data['studentid']=studentid
            data['submissionid']=submissionid
            ser=GradesSerializer(data=data)
            if ser.is_valid():
                ser.save()
                return Response(ser.data)
            return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='POST':
        data=request.data
        data['studentid'] = studentid
        data['submissionid'] = submissionid
        ser = GradesSerializer(g,data=data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@login_required(login_url="login")
@api_view(['GET'])
def viewallstudentsincourse(request,id):
    try:
        studs=StudentCourses.objects.filter(courseid=id)
        a=set()
        for i in studs:
            a.add(i.studentid.id)
        students=StudentsInformation.objects.filter(id__in=a)
        ser=StudentInformationSerializer(students,many=True)
        return Response(ser.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@login_required(login_url="login")
@api_view(['GET'])
def viewprogressofstudent(request,id):
    if request.method=='GET':
        assignments=Assignments.objects.filter(courseid=id)
        a=set()
        for i in assignments:
            a.add(i.id)
        try:

            studid=StudentsInformation.objects.get(owner=request.user)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        submissions=Submissions.objects.filter(Q(studentid=studid) & Q(assignmentid__in=a))
        b=set()
        for i in submissions:
            b.add(i.id)
        grades=Grades.objects.filter(submissionid__in=b)
        sum=0
        for i in grades:
            sum+=i.grade
        sum+=0.0
        total=assignments.__len__()
        if(total==0):
            data = {"progress": 100}
            return Response(data)
        total*=5
        progress=(sum/total)*100
        progress=round(progress,2)
        data={"progress":progress}
        return Response(data)
    return Response(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@login_required(login_url="login")
@api_view(['GET'])
def getgradebasedonsubmissionid(request,id):
    try:
        s=Grades.objects.get(submissionid=id)
        ser=GradesSerializer(s)
        return Response(ser.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@login_required(login_url="login")
@api_view(['GET','POST'])
def getallpostsofcourse(request,id):
    try:
        p=Posts.objects.filter(courseid=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        ser=PostSerializer(p,many=True)
        return Response(ser.data)
    elif request.method=='POST':
        data=request.data
        id=(int)(id)
        data['courseid']=id
        ser=PostSerializer(data=data)
        if ser.is_valid():
            ser.save()
            p = Posts.objects.filter(courseid=id)
            ser=PostSerializer(p,many=True)
            return Response(ser.data)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@login_required(login_url="login")
@api_view(['GET','PUT','DELETE'])
def getpost(request,id):
    try:
        p=Posts.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        ser=PostSerializer(p)
        return Response(ser.data)
    elif request.method=='PUT':
        ser=PostSerializer(p,data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        p.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)


