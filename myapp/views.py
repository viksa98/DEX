from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from .models import Document, Polinja
from .forms import DocumentForm, PolinjaForm
from django.http import JsonResponse
import os
from dss.dex import DEXModel
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize
import numpy as np
from django.views.generic.edit import CreateView


from django.conf import settings


class NumpyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(self, obj)


folder = "D:/uploads/"


def get_file():
    filess = []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            filess.append(filename)
    return filess


def dex_local_input(request):
    if request.method == "GET":
        files = get_file()
        dex = DEXModel(f"{folder}{files[len(files) - 1]}")
        return dex.get_intput_attributes()


@require_http_methods(["GET"])
def dex_input(request):
    dex = DEXModel(settings.DEX_MODEL)
    return JsonResponse(dex.get_intput_attributes(), safe=True)


@csrf_exempt
@require_http_methods(["POST"])
def dex_evaluate(request):
    dex = DEXModel(settings.DEX_MODEL)
    data = json.loads(request.body)
    res, qq_res = dex.evaluate_model(data)

    dex_res = dict()
    dex_res["quantitative"] = res
    dex_res["qualitative"] = qq_res

    return JsonResponse(dex_res, safe=False, encoder=NumpyEncoder)


def my_view(request):
    message = "Upload as many files as you want!"
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES["docfile"])
            newdoc.save()

            return redirect("my-view")
        else:
            message = "The form is not valid. Fix the following error:"
    else:
        form = DocumentForm()

    documents = Document.objects.all()

    context = {"documents": documents, "form": form, "message": message}
    return render(request, "list.html", context)


# def CreatePolinjalView(request):
#     if request.method == 'POST':
#         instance = get_object_or_404(Pole)
#         model = Polinja
#         form = PolinjaForm()
#         context = {
#             'form': form,
#             'book_instance': book_instance,
#         }
#     template_name = 'myapp/templates/template.html'
#     # success_url = 'myapp/success.html'


@csrf_exempt
def post_edit(request):
    if request.method == "POST":
        form = PolinjaForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            dataa = form.cleaned_data
            return JsonResponse(dataa)

    else:
        form = PolinjaForm()
    return render(request, "template.html", {"form": form})
