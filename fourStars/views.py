from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

#create your views here
def home(request):
    # return HttpResponse("<h1>Four Stars Project</h1>")
    return render(request, 'home.html', {'name': 'Vale Hornung'})

def about(request):
    return HttpResponse("<h1>About Four Stars </h1>")

