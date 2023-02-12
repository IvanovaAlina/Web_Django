from django.shortcuts import render, redirect
from .models import Checks
from .forms import CheckForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,Http404
from django.conf import settings
import os
from deep_translator import GoogleTranslator
import requests

# Create your views here.

def index(request):
    return render(request, 'cost_control\index.html')

@login_required
def check_list(request):
    list = Checks.objects.filter(owner = request.user).order_by('date_added')
    context = {'checks': list}
    return render(request, 'cost_control\check_list.html', context)

@login_required
def new_check(request):
    if request.method != 'POST':
        form = CheckForm()
    else:
        form =  CheckForm(data = request.POST)
        if form.is_valid():
            new_check = form.save(commit=False)
            new_check.owner = request.user
            if request.FILES:
                file = request.FILES['photo_check']
                name_file_parts = file.name.split(".")
                file_name = GoogleTranslator(source='auto', target='english').translate(name_file_parts[0])
                file_name = '{}.{}'.format(file_name, name_file_parts[-1])
                file.name = file_name
                new_check.photo_check = file
            new_check.save()
            return redirect('cost_control_project:check_list')

    context = {"form" : form}
    return render(request, 'cost_control/new_check.html', context)

@login_required
def delete_check(request, check_id):
    check = Checks.objects.get(id = check_id)
    if check.owner != request.user :
        raise Http404
    if request.method=="POST":
        if check.photo_check:
            check.photo_check.delete();
        check.delete()
        return redirect('cost_control_project:check_list')
    context = {"item":check}
    return render(request, 'cost_control/confirm_delete_check.html', context)
    
@login_required
def edit_check(request, check_id):
    check = Checks.objects.get(id = check_id)
    if check.owner != request.user :
        raise Http404
    if request.method != 'POST':
        form = CheckForm(instance = check)
    else:
        form =  CheckForm(instance = check, data = request.POST)
        if form.is_valid():
            edit_check = form.save()
            if request.FILES:
                file = request.FILES['photo_check']
                name_file_parts = file.name.split(".")
                file_name = GoogleTranslator(source='auto', target='english').translate(name_file_parts[0])
                file_name = '{}.{}'.format(file_name, name_file_parts[-1])
                file.name = file_name
                edit_check.photo_check = file
                edit_check.save()
            return redirect('cost_control_project:check_list')

    context = {"check":check, "form" : form}
    return render(request, 'cost_control/edit_check.html', context)

@login_required
def download_upload(request, check_id):
    check = Checks.objects.get(id = check_id)
    file_path = settings.MEDIA_ROOT + "/" + check.photo_check.name
    file_path = file_path.replace('/', '\\')
    if os.path.exists(file_path):
        fh = open(file_path, 'rb')
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
    form = CheckForm(instance = check)
    context = {"check":check, "form" : form}
    return render(request, 'cost_control/edit_check.html', context)

@login_required
def  delete_upload(request, check_id):
    check = Checks.objects.get(id = check_id)
    if check.owner != request.user :
        raise Http404
    if request.method=="POST":
        if check.photo_check:
            check.photo_check.delete();
        form = CheckForm(instance = check)
        context = {"check":check, "form" : form}
        return render(request, 'cost_control/edit_check.html', context)
    context = {"item":check}
    return render(request, 'cost_control/confirm_delete_photo_check.html', context)

