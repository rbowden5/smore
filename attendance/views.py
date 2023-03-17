from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.db import connection
from django.urls import reverse
from django.utils import timezone

from .models import Child, Adult, Staff, Attendance_History

import datetime
now = timezone.now()

class registerChild(forms.Form):
    child_first_name = forms.CharField(label="Child's First Name", max_length=64)
    child_last_name = forms.CharField(label="Child's Last Name", max_length=64)

class addAdult(forms.Form):
    adult_first_name = forms.CharField(label="Adult's First Name", max_length=64)
    adult_last_name = forms.CharField(label="Adult's Last Name", max_length=64)
    adult_phone_number = forms.CharField(label="Phone Number", max_length=12)

# Create your views here.
def index(request):
    children = Child.objects.raw("SELECT * FROM attendance_child ORDER BY last_name, first_name")
    adults = Adult.objects.raw("SELECT * FROM attendance_adult ORDER BY last_name, first_name")
    presents = Child.objects.filter(attendance_status=1)
    """
    children = Child.objects.all()
    print(children)
    print(connection.queries)

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM attendance_child;")
    print(cursor.fetchall())    
    """

    return render(request, "attendance/index.html", { 
        "children": children,
        "adults": adults,
        "presents": presents
        })

def search(request):
    print(request.GET.get('q'))
    print(request.GET.get('t'))
    query = request.GET.get('q')
    model = request.GET.get('t')
    if model == "child":
        results = Child.objects.filter(last_name__contains=query)
    elif model == "adult":
        results = Adult.objects.filter(last_name__contains=query)
    else:
        results = ""
    print(results)
    print(model)
    return render(request, "attendance/search.html", {
        "results": results,
        "model": model
    })

def adult_details(request, adult_id):
    adult = Adult.objects.get(pk=adult_id)
    children = adult.children.all()
    return render(request, "attendance/adult.html", {
        "adult": adult,
        "children": children,
        "staffs": Staff.objects.all(),
        "message": ""
    })

def attendance_history(request):
    history = Attendance_History.objects.all().order_by("-timestamp")
    return render(request, "attendance/history.html", {
        "histories": history,
    })

def child_details(request, child_id):
    child = Child.objects.get(pk=child_id)
    return render(request, "attendance/child.html", {
        "child": child,
        "adults": child.adults.all(),
        "staffs": Staff.objects.all(),
    })


def register(request):
    if request.method == "POST":
        child_form = registerChild(request.POST)
        adult_form = addAdult(request.POST)
        if child_form.is_valid() and adult_form.is_valid():

            #Clean data from forms
            child_first_name = child_form.cleaned_data["child_first_name"].capitalize()
            child_last_name = child_form.cleaned_data["child_last_name"].capitalize()

            adult_first_name = adult_form.cleaned_data["adult_first_name"].capitalize()
            adult_last_name = adult_form.cleaned_data["adult_last_name"].capitalize()
            adult_phone_number = adult_form.cleaned_data["adult_phone_number"]

            #Check if adult in database, add if not
            num_adult = Adult.objects.filter(first_name=adult_first_name, last_name=adult_last_name, adult_phone_number=adult_phone_number).count()
            print(num_adult)

            if(num_adult > 0):
                adult_object = Adult.objects.get(first_name=adult_first_name, last_name=adult_last_name, adult_phone_number=adult_phone_number)
            else:
                adult_object = Adult.objects.create(first_name=adult_first_name, last_name=adult_last_name, adult_phone_number=adult_phone_number)

            #Check if child is in database, add if not
            num_child = Child.objects.filter(first_name=child_first_name, last_name=child_last_name).count()

            if(num_child > 0):
                child_object = Child.objects.get(first_name=child_first_name, last_name=child_last_name)
            else:
                child_object = Child.objects.create(first_name=child_first_name, last_name=child_last_name)

            #Connect child to adult
            adult_object.children.add(child_object)

            return render(request, "attendance/index.html", {
                "message": "Success",
            })
    else:
        return render(request, "attendance/register.html", {
            "child_form": registerChild(),
            "adult_form": addAdult()
        })
"""
def search(request):
    children = Child.objects.raw("SELECT * FROM attendance_child ORDER BY last_name, first_name")
    adults = Adult.objects.raw("SELECT * FROM attendance_adult ORDER BY last_name, first_name")
    
    if request.method == "GET":
        if request.GET.get('q'):
            query = str(request.GET.get('q'))
            results = Child.objects.filter(last_name__contains=query)
            return render(request, "attendance/index.html", {
                "children": children,
                "adults": adults,
                "results": results
            })
"""

def change_status(request, child_id):
    if(request.method == "POST"):
        #Retrieve all information from html
        child = Child.objects.get(pk=child_id)
        adult = Adult.objects.get(pk=request.POST.get('adult'))
        staff = Staff.objects.get(pk=request.POST.get('staff'))
        #Change child attendance status
        if(child.attendance_status == 0):
            child.attendance_status = 1
            child.save()
        else:
            child.attendance_status = 0
            child.save()
        #Add to history
        new = Attendance_History.objects.create(child=child, adult=adult, staff=staff, status=child.attendance_status)

        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))