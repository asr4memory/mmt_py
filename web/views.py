from django.shortcuts import render

def welcome(request):
    return render(request, 'web/welcome.html')

def upload(request):
    return render(request, "web/upload.html")

def download(request):
    return render(request, "web/download.html")
