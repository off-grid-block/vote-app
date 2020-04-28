from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView

from vote.models import Poll
from users.forms import CustomUserCreationForm
from deon_apps.settings import API_URL

import requests
import json


class HomePageView(TemplateView):
    template_name = 'home.html'


class SignupPageView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('homepage')
    template_name = 'signup.html'


def user_vote_view(request, userid):
    resp = requests.get(f'{API_URL}/vote', params={'voterid': userid})
    if resp.status_code >= 300:
        return HttpResponse(status=resp.status_code)

    resp_str = resp.content.decode('UTF-8')
    resp_json = json.loads(resp_str, strict=False)

    context_dict = {
        'userid': userid,
        'votes': resp_json,
    }

    return render(request, 'user_vote.html', context_dict)
