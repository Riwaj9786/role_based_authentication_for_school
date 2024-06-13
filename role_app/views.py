from django.shortcuts import render, redirect
from django.http import HttpResponse
from role_app.forms import RegistrationForm, LoginForm
from role_app import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return HttpResponse("You are a Staff!")
        
        if request.user.is_student:
            return HttpResponse("You are a Student!")
        
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    return HttpResponse("Logged In as a Staff!")
                elif user.is_student:
                    login(request,user)
                    return HttpResponse("Logged In as a Student!")
                else:
                    form.add_error(None, "User is not a staff!")
            else:
                form.add_error(None, "Invalid Username and Password!")
        else:
            form.add_error(None, 'Form is not Valid!')
    else:
        form = LoginForm()

    return render(request, 'index.html', {'form': form})


def registeruser(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data.get('email')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            is_student = form.cleaned_data.get('is_student')
            user.password = make_password(form.cleaned_data['password'])

            if is_student:
                try:
                    student = models.Student.objects.get(email=email, date_of_birth=date_of_birth)
                    user.is_student = True
                    user.save()
                    student.user = user
                    student.save()
                    login(request, user)
                    return redirect('roles:home')
                except models.Student.DoesNotExist:
                    form.add_error(None, 'No student found with the provided details.')
            else:
                user.save()
                login(request, user)
                return redirect('roles:home')
    else:
        form = RegistrationForm()

    return render(request, 'signup.html', {'form': form})

