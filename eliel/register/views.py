from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from sweetify import sweetify
from .forms import RegisterForm, LoginForm
from .models import Person
import re
from django import forms
from django.core.exceptions import ValidationError

def mi_vista(request):
    login_form = LoginForm()
    registration_form = RegisterForm()

    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('register:dashboard')
            else:
                error_message = "Nombre de usuario o contraseña incorrectos."
                sweetify.error(request, 'Error de inicio de sesión', text=error_message, persistent='Ok')
                return render(request, 'index.html', {'login_form': login_form, 'registration_form': registration_form})
        else:
            registration_form = RegisterForm(request.POST)
            if registration_form.is_valid():
                registration_form.save()
                sweetify.success(request, 'Registro exitoso', text='Ahora puedes iniciar sesión', persistent='Ok')
                return redirect('register:inicio')
            else:
                for field, errors in registration_form.errors.items():
                    for error in errors:
                        sweetify.error(request, 'Error de validación', text=f"Error en el campo {field}: {error}", persistent='Ok')
                return render(request, 'index.html', {'login_form': login_form, 'registration_form': registration_form})

    return render(request, 'index.html', {'login_form': login_form, 'registration_form': registration_form})

def dashboard(request):
    registered_users = Person.objects.all()
    return render(request, 'dashboard.html', {'registered_users': registered_users})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            sweetify.success(request, 'Registro exitoso', text='Ahora puedes iniciar sesión', persistent='Ok')
            return redirect('register:inicio')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    sweetify.error(request, 'Error de validación', text=f"Error en el campo {field}: {error}", persistent='Ok')
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
