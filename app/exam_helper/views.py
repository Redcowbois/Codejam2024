from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def options(request):
    template = loader.get_template('file-options.html')
    return HttpResponse(template.render())

def test(request):
    return HttpResponse("test")
