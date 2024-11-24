from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from exam_helper.forms import UploadFileForm
from exam_helper.utils import ROOT_DIR
import json
import exam_helper.multiple_choice
import exam_helper.qwen
from os import path

def handle_uploaded_file(f):
     with open(path.join(ROOT_DIR, "uploaded_files", f.name), "wb+") as file:
          for chunk in f.chunks():
               file.write(chunk)

@csrf_exempt
def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            return JsonResponse({'redirect_url': 'options'})

        # Return the response with the redirection URL
        return JsonResponse({'redirect_url': 'options'})
    
    if request.method == 'GET':
        template = loader.get_template('main.html')
        return HttpResponse(template.render())

@csrf_exempt
def options(request):
        if request.method == 'POST':
            print("options received")
        template = loader.get_template('file-options.html')
        return HttpResponse(template.render())


@csrf_exempt
def summary(request):
        if request.method == 'POST':
            print("options received")
        template = loader.get_template('Summary.html')
        return HttpResponse(template.render())

@csrf_exempt
def flashcard(request):
        if request.method == 'POST':
            payload = json.loads(request.body)

            f = open("data.txt", "r")
            text_data = f.read()
            f.close()

            final_data = generate_n_questions_for_info(3, text_data, get_qwen_pipe())

            data = {
                'questions': final_data,
            }

            return JsonResponse(data)

        if request.method == 'GET':
            template = loader.get_template('flashcard.html')
            return HttpResponse(template.render())

@csrf_exempt
def podcast(request):
        if request.method == 'POST':
            print("options received")
        template = loader.get_template('podcast.html')
        return HttpResponse(template.render())

@csrf_exempt
def quiz(request):
        if request.method == 'POST':
            print("options received")
        template = loader.get_template('quiz.html')
        return HttpResponse(template.render())


@csrf_exempt
def trial(request):
    if request.method == 'POST':
        a = request.POST['message']
        return HttpResponse(a)
    
    template = loader.get_template('trial.html')
    return HttpResponse(template.render())
