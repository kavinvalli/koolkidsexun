from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

def login(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            url = "/jobs/"+str(user.id)
            return redirect(url)
        else:
            return render(request, "login/login.html", {"message": "Invalid credentials."})
    else:
        return render(request, "login/login.html", {"message": None, 'action_url':'/login/','heading':'Login Now!!!'})

def logout(request):
    auth_logout(request)
    return render(request, "jobs/index.html")