from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Input


def index(request):
    return render(request, 'members_app/index.html')


def save_input(request):
    user_input = request.POST['input']
    input_obj = Input(member_input=user_input)
    input_obj.save()
    return redirect('members_app:results')


def results(request):
    user_results = Input.objects.all()
    return render(request, 'members_app/results.html',{'user_results': user_results})



