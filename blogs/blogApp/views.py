from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'blogApp/index.html')

def register(request):
    return render(request, 'blogApp/registeration.html')

def user_login(request):
    return render(request, 'blogApp/login.html')
