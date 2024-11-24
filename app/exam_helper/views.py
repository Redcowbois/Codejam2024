from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from exam_helper.forms import UploadFileForm
from exam_helper.utils import ROOT_DIR
import json
from exam_helper.flashcards import generate_n_flashcards_for_info
from exam_helper.multiple_choice import generate_n_questions_for_info
from exam_helper.qwen import get_qwen_pipe
from os import path
from exam_helper.utilities import convert_mp4_to_mp3, extract_text_from_pdf
from exam_helper.whisper import get_whisper_pipe


def handle_uploaded_file(f, file_path):
    with open(file_path, "wb+") as file:
        for chunk in f.chunks():
            file.write(chunk)


@csrf_exempt
def index(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse({"redirect_url": "options"})

        file_path = path.join(ROOT_DIR, "uploaded_files", request.FILES["file"].name)
        handle_uploaded_file(request.FILES["file"], file_path)
        filename, extension = path.splitext(file_path)
        data = ""
        if extension == ".mp4":
            convert_mp4_to_mp3(file_path, f"{filename}.mp3")
            extension = ".mp3"
        if extension == ".mp3":
            pipe = get_whisper_pipe()
            data = pipe(f"{filename}.mp3")["text"]
            del pipe
        if extension == ".txt":
            with open(file_path, "r") as file:
                data = file.read()
        if extension != ".pdf":
            with open("data.txt", "w+") as file:
                file.write(data)
        else:
            extract_text_from_pdf(file_path, "data.txt")

        return JsonResponse({"redirect_url": "options"})

        # Return the response with the redirection URL

    if request.method == "GET":
        template = loader.get_template("main.html")
        return HttpResponse(template.render())


@csrf_exempt
def options(request):
    if request.method == "POST":
        print("options received")
    template = loader.get_template("file-options.html")
    return HttpResponse(template.render())


@csrf_exempt
def summary(request):
    if request.method == "POST":
        print("options received")
    template = loader.get_template("Summary.html")
    return HttpResponse(template.render())


@csrf_exempt
def flashcard(request):
        if request.method == 'POST':
            payload = json.loads(request.body)
            file = open("data.txt", "r")
            text_data = file.read()
            file.close()

            pipe = get_qwen_pipe()
            text_data = generate_n_flashcards_for_info(3, text_data, pipe)
            del pipe
            data = {
                'message': text_data,
            }
            return JsonResponse(data)

        if request.method == 'GET':
            template = loader.get_template('flashcard.html')
            return HttpResponse(template.render())


@csrf_exempt
def podcast(request):
    if request.method == "POST":
        print("options received")
    template = loader.get_template("podcast.html")
    return HttpResponse(template.render())


@csrf_exempt
def quiz(request):
    if request.method == "POST":
        payload = json.loads(request.body)
        f = open("data.txt", "r")
        text_data = f.read()
        f.close()
        pipe = get_qwen_pipe()
        final_data = generate_n_questions_for_info(3, text_data, pipe)
        del pipe
        data = {
            'questions': final_data,
        }
        return JsonResponse(data)

    if request.method == "GET":
        template = loader.get_template("quiz.html")
        return HttpResponse(template.render())

@csrf_exempt
def trial(request):
    if request.method == "POST":
        a = request.POST["message"]
        return HttpResponse(a)

    template = loader.get_template("trial.html")
    return HttpResponse(template.render())
