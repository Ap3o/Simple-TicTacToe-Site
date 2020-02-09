from django.contrib.auth import logout
from django.shortcuts import render
from django.shortcuts import redirect

# Для регистрации
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView


# Вариант регистрации на базе класса FormView
class MyRegisterFormView(FormView):
    # Указажем какую форму мы будем использовать для регистрации наших пользователей (Стандартная)
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    success_url = "/"

    # Шаблон, который будет использоваться при отображении
    template_name = "registration/register.html"

    def form_valid(self, form):
        form.save()
        # Функция super( тип [ , объект или тип ] )
        # Возвратите объект прокси, который делегирует вызовы метода родительскому или родственному классу типа .
        return super(MyRegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(MyRegisterFormView, self).form_invalid(form)


# Основная страница
def main_page(request):
    return render(request, "main_page/wrapper.html")


# Выход из аккаунта
def logout_user(request):
    logout(request)
    return redirect("/")
