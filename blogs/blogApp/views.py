from django.shortcuts import render,redirect
from django.urls import reverse
from blogApp.helperFunc import helpers
from . import forms
from blogApp.models import journalModel,userModel
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# tring to get username from the user login view and than use it to query database to
# get the data of that particular user and than will show it o the main screen

def index(request):
    data = userModel.objects.all().values()
    print("helpers.id")
    print(helpers.userId)
    return render(request, 'blogApp/index.html',{'data':data})

def register(request):
    registered = False

    form = forms.FormName()

    if request.method == "POST":
        form = forms.FormName(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            print("validation success")
        else:
            print("validation error")
    else:
        form = forms.FormName()


    return render(request, 'blogApp/registeration.html',{'form':form,
                                                        'registered': registered,})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(request.POST.get('username'))

        response = authenticate(username=username, password=password)
        if isinstance(response, HttpResponseRedirect):
            return response
        elif response:
            print("user autheticated")
            if response.is_active:
                login(request, response)
                helpers.userId = request.POST.get('username')
                print("login successfull")
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not active")
        else:
            return HttpResponse("invalid login detailids supplied!")
    else:
        return render(request, 'blogApp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def blogView(request):
    form = forms.journalForm()
    if request.method == "POST":
        form = forms.journalForm(request.POST)
        if form.is_valid():
            form.save()
            data = journalModel.objects.all()
            for entry in data:
                x=str(entry.userId)
                y=int(x)
                entry.userIdInt = y
                entry.save()
            form = forms.journalForm()
            return redirect(reverse('index'))
            print("journal form validation success")
        else:
            print("journal form validation failed")

    return render(request, 'blogApp/blog.html', {'form':form})

