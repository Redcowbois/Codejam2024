from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json
from exam_helper.multiple_choice import *
from exam_helper.qwen import *
from exam_helper.flashcards import *

@csrf_exempt
def index(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)

        # Extract fields from the JSON payload
        file_name = data.get('name')
        file_type = data.get('type')
        file_size = data.get('size')
        file_content = data.get('content')  # Base64-encoded file content
        file_content = file_content.split(",")[1]

        # Decode the file content from Base64 if needed
        import base64
        # print(file_content)
        decoded =  base64.b64decode(file_content)
        decoded = decoded.decode('utf-8')
        f = open("data.txt", "w")
        f.write(decoded)
        f.close()
        
        redirect_url = reverse('options')  # Replace 'some_view_name' with the actual view name

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
            # Parse the incoming JSON data
            payload = json.loads(request.body)
            file = open("data.txt", "r")
            text_data = file.read()
            file.close()

            text_data = generate_n_flashcards_for_info(3, text_data, get_qwen_pipe())

            data = {
                'message': text_data,
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
