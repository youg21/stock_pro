from django.shortcuts import render,HttpResponse

def index(request):
    return HttpResponse('Hello Django!!!!')

def hello(request):
    pass