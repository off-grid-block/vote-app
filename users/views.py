from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView

from client import DeonClient
from users.forms import CustomUserCreationForm


class HomePageView(TemplateView):
    template_name = 'home.html'


class SignupPageView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('homepage')
    template_name = 'signup.html'


def user_vote_view(request, userid):

    vote_data_client = DeonClient(
        obj_type='vote', params={'voterid': userid},
        method=request.method)
    vote_data_resp = vote_data_client.send_request()

    if vote_data_client.error_status_code:
        return HttpResponse(status=vote_data_client.error_status_code)

    context_dict = {
        'userid': userid,
        'votes': vote_data_resp,
    }

    return render(request, 'user_vote.html', context_dict)
