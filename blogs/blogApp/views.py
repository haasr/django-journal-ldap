from django.shortcuts import render
from . import forms

# Create your views here.
def index(request):
    return render(request, 'blogApp/index.html')

def register(request):
    form = forms.FormName()

    if request.method == "POST":
        form = forms.FormName(request.POST)
        if form.is_valid():
            print("validation success")

    return render(request, 'blogApp/registeration.html',{'form':form})

def user_login(request):
    return render(request, 'blogApp/login.html')
