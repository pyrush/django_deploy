from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse

from .models import ImageModel
from .forms import ImageUploadForm
from .tasks import test_func


def test(request):
    test_func.delay()
    return HttpResponse("Done")


class UploadImage(View):

    def get(self, request, *args, **kwargs):
        form = ImageUploadForm()
        context = {}
        context["form"] = form
        return render(request, 'image/imagemodel_form.html', context)

    # def form_valid(self, form):
    #     name = form.cleaned_data['name']
    #     messages.success(self.request, f"Image with {name} successfully saved")
    #     return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        return render(request, 'image/imagemodel_form.html')
