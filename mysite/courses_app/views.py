from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    if not request.user.is_authenticated:
        return HttpResponse("You have no permissions to view this page")
    return HttpResponse("This is the Courses page")

