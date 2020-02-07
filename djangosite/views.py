from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.shortcuts import redirect, HttpResponse


# Основная страница
def main_page(request):
    return render(request, "main_page/wrapper.html")


# Выход из аккаунта
def logout_user(request):
    logout(request)
    return redirect("/")
