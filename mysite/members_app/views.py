from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Input


def index(request):
    return render(request, 'members_app/index.html')


def save_input(request):
    user_input = request.POST['input']
    input_obj = Input(member_input=user_input)
    input_obj.save()
    if 'results' not in request.session:
        request.session['results'] = []
    request.session['results'].append(user_input)
    request.session.modified = True
    return redirect('members_app:results')


def results(request):
    user_results = Input.objects.all()
    session_results = request.session.get('results', [])
    return render(request, 'members_app/results.html',
                  {'user_results': user_results, 'session_results': session_results})



