from django.shortcuts import redirect, render 
from .models import Document
from .forms import DocumentForm
from django.http import JsonResponse
import os
from dss.dex import DEXModel
from django.http import HttpResponse
from django.conf import settings

folder = 'D:/uploads/'

def get_file():
    filess = []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            filess.append(filename)
    return filess

def dex_local_input(request):
    if request.method == 'GET':
        files = get_file()
        dex = DEXModel(f'{folder}{files[len(files) - 1]}')
        return dex.get_intput_attributes()

def dex_input(request):
    if request.method == 'GET':
        dex = DEXModel(settings.DEX_MODEL) 
        return JsonResponse(dex.get_intput_attributes(), safe=True)

def dex_evaluate(request):
    if request.method == 'GET':
        dex = DEXModel(settings.DEX_MODEL) 
        return JsonResponse(dex.evaluate_model(dex_local_input(request)), safe=False)
    

def my_view(request):
    message = 'Upload as many files as you want!'
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            return redirect('my-view')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()

    documents = Document.objects.all()

    context = {'documents': documents, 'form': form, 'message': message}
    return render(request, 'list.html', context)
