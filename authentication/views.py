from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth import logout
from authentication.github_api import *
from django.contrib.auth.decorators import login_required
import requests
import json
from django.urls import reverse
from social_django.models import UserSocialAuth
from django.urls import NoReverseMatch

# Create your views here.

class LoginView(View, ContextMixin):

    template_name = "login/login.html"

    def get(self, request, *args, **kwargs):
        context = {}
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        return redirect("social:begin", args=["github"])

class HomeView(View, ContextMixin, LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = "dash/home.html"

    def get(self, request, *args, **kwargs):
        token = UserSocialAuth.objects.get(extra_data__contains=request.user.username).access_token
        userdata = get_user_data(request.user, token)

        topic = None
        if request.GET.get("topic"):
            topic = request.GET.get("topic")

        if topic is not None:
            user_repositories = filter_repositories(request.user, token, topic)
        else:
            user_repositories = get_user_repositories(request.user, token)

        context = {"user_data": userdata, "user_repositories": user_repositories}

        try:
            return render(request, self.template_name, context)
        except NoReverseMatch: # token expirado
            return redirect("logout")



class DetailRepository(View):
    template_name = "dash/detail_repository.html"
    def get(self, request, *args, **kwargs):
        token = UserSocialAuth.objects.get(extra_data__contains=request.user.username).access_token
        context = {"repository_data": get_repository_info(request.user, kwargs["name"], token),"repository_tags": get_repository_tags(request.user, kwargs["name"], token)}
        
        try:
            return render(request, self.template_name, context)
        except NoReverseMatch:
            return redirect("logout")

    def post(self, request, *args, **kwargs):
        token = UserSocialAuth.objects.get(extra_data__contains=request.user.username).access_token
        lista_tags = request.POST.get("tag").split(',')
        lista_tags = [x.lower() for x in lista_tags if len(x) > 0]

        response = update_repository_tags(request.user, kwargs["name"], token, lista_tags)
        repo = get_repository_info(request.user, kwargs["name"], token)
        context = {"repository_data": repo,"repository_tags": get_repository_tags(request.user, kwargs["name"], token)}        
        try:
            return render(request, self.template_name, context)
        except NoReverseMatch:
            return redirect("logout")


def logout_view(request):
    social_user = UserSocialAuth.objects.get(extra_data__contains=request.user.username)
    social_user.extra_data["access_token"] = ""
    social_user.save()
    logout(request)
    return redirect("login")