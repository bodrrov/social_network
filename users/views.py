#  импортируем CreateView, чтобы создать ему наследника
from django.views.generic import CreateView
#  функция reverse_lazy позволяет получить URL по параметру "name" функции path()
#  берём, тоже пригодится
from django.urls import reverse_lazy

#  импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm  #из какого класса взять форму
    success_url = reverse_lazy("login") #  где login — это параметр "name" в path() #куда перенаправить пользователя после успешной отправки формы
    template_name = "signup.html"

