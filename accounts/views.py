from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('turfs:turf_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class MahaMaidanLoginView(LoginView):
    template_name = 'accounts/login.html'


class MahaMaidanLogoutView(LogoutView):
    next_page = 'turfs:turf_list'
