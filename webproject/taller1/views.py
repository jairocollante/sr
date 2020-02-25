from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request,'taller1/index.html',{});
    
def ex1(request):
    return render(request,'taller1/ex1.html',{});
