from django.shortcuts import render, redirect
from .models import Checks, CategoryPurchase
from .forms import CheckForm, CategoryPurchaseForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,Http404
from django.conf import settings
import os
from deep_translator import GoogleTranslator
import requests
import datetime
from qsstats import QuerySetStats
from django.db.models import Sum

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

@login_required
def analyze_checks(request):
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=today.day) + datetime.timedelta(1)
    end_date = today 
    queryset = Checks.objects.filter(owner = request.user)
    qsstats = QuerySetStats(queryset, date_field='date_check', aggregate=Sum('summ_check'))
    values = qsstats.time_series(start_date, end_date, interval='days')
    #google charts пишет дорбные числа через запятую, возникает ошибка, в итоге решила поменять на string
    i = 0
    for val in values:
        loclist = list(val)
        loclist[1] = str(loclist[1])
        values[i] = tuple(loclist)
        i+=1
    context = {"data_checks":values, "start_date": str(start_date), "end_date": str(end_date) }
    return render(request, 'cost_control/analitics_check.html', context)

@login_required
def analyze_checks_filters(request):
    start_date_str = request.GET["date_begin"]
    start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date_str = request.GET["date_end"]
    end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
    category_str = request.GET["category"]
    if category_str != "": 
        queryset = Checks.objects.filter(owner = request.user) & Checks.objects.filter(category__name_purchase__contains = category_str)
    else:
        queryset = Checks.objects.filter(owner = request.user)
    qsstats = QuerySetStats(queryset, date_field='date_check', aggregate=Sum('summ_check'))
    values = qsstats.time_series(start_date, end_date, interval='days')
    #google charts пишет дорбные числа через запятую, возникает ошибка, в итоге решила поменять на string
    i = 0
    for val in values:
        loclist = list(val)
        loclist[1] = str(loclist[1])
        values[i] = tuple(loclist)
        i+=1
    context = {"data_checks":values, "start_date": str(start_date), "end_date": str(end_date), "category":category_str }
    return render(request, 'cost_control/analitics_check.html', context)

@login_required
def category_list(request):
    list = CategoryPurchase.objects.filter(owner = request.user).order_by('date_added')
    context = {'categories': list}
    return render(request, 'cost_control\categories_list.html', context)

@login_required
def new_category(request):
    if request.method != 'POST':
        form = CategoryPurchaseForm()
    else:
        form =  CategoryPurchaseForm(data = request.POST)
        if form.is_valid():
            new_cat = form.save(commit=False)
            new_cat.owner = request.user
            new_cat.save()
            return redirect('cost_control_project:category_list')

    context = {"form" : form}
    return render(request, 'cost_control/new_category.html', context)

@login_required
def delete_category(request, category_id):
    cat = CategoryPurchase.objects.get(id = category_id)
    if cat.owner != request.user :
        raise Http404
    if request.method=="POST":
        cat.delete()
        return redirect('cost_control_project:category_list')
    context = {"item":cat}
    return render(request, 'cost_control/confirm_delete_category.html', context)
    
@login_required
def edit_category(request, category_id):
    cat = CategoryPurchase.objects.get(id = category_id)
    if cat.owner != request.user :
        raise Http404
    if request.method != 'POST':
        form = CategoryPurchaseForm(instance = cat)
    else:
        form =  CategoryPurchaseForm(instance = cat, data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('cost_control_project:category_list')

    context = {"item":cat, "form" : form}
    return render(request, 'cost_control/edit_category.html', context)
