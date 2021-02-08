from django.shortcuts import render
from .forms import DexForm
from django.http import JsonResponse
from dss.dex import DEXModel
from django.views.decorators.http import require_http_methods
import json
from django.core.serializers.json import DjangoJSONEncoder
import numpy as np
from django.conf import settings

class NumpyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(self, obj)

# Vo slucaj da treba file uplaod
# def get_file():
#     filess = []
#     for filename in os.listdir(folder):
#         path = os.path.join(folder, filename)
#         if os.path.isfile(path):
#             filess.append(filename)
#     return filess

@require_http_methods(["GET"])
def dex_input(request):
    dex = DEXModel(settings.DEX_MODEL)
    return JsonResponse(dex.get_intput_attributes(), safe=True)

@require_http_methods(["POST"])
def dex_evaluate(request):
    dex = DEXModel(settings.DEX_MODEL)
    data = json.loads(request.body)
    res, qq_res = dex.evaluate_model(data)

    dex_res = dict()
    dex_res["quantitative"] = res
    dex_res["qualitative"] = qq_res

    return JsonResponse(dex_res, safe=False, encoder=NumpyEncoder)

# Vo slucaj da treba file uplaod
# def my_view(request):
#     message = "Upload as many files as you want!"
#     if request.method == "POST":
#         form = DocumentForm(request.POST, request.FILES)
#         if form.is_valid():
#             newdoc = Document(docfile=request.FILES["docfile"])
#             newdoc.save()

#             return redirect("my-view")
#         else:
#             message = "The form is not valid. Fix the following error:"
#     else:
#         form = DocumentForm()

#     documents = Document.objects.all()

#     context = {"documents": documents, "form": form, "message": message}
#     return render(request, "list.html", context)

def provide_attributes(request):
    dex = DEXModel(settings.DEX_MODEL)
    if request.method == "POST":
        form = DexForm(dex.get_intput_attributes(), request.POST)
        print(form.is_valid())
        if form.is_valid():
            dataa = form.cleaned_data
            res, qq_res = dex.evaluate_model(dataa)
            
            dex_res = dict()
            dex_res["quantitative"] = res
            dex_res["qualitative"] = qq_res

            return JsonResponse(dex_res, safe=False, encoder=NumpyEncoder)
    else:
        form = DexForm((dex.get_intput_attributes()))
    return render(request, "template.html", {"form": form})
