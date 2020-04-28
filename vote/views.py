from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView

from vote.models import Poll
from vote.forms import CreateVoteForm, CreatePollForm
from deon_apps.settings import API_URL

import json
import requests


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['polls'] = Poll.objects.all()
        return context


def vote_create_view(request, pollid):
    if request.method == "POST":
        form = CreateVoteForm(request.POST)

        if form.is_valid():

            voterid = form.cleaned_data['voterid']

            payload = {'pollID': str(pollid),
                       'voterID': str(voterid),
                       'sex': form.cleaned_data['sex'],
                       'age': str(form.cleaned_data['age']),
                       'content': form.cleaned_data['choice']}

            resp = requests.post(f'{API_URL}/vote', json=payload)
            if resp.status_code >= 300:
                return HttpResponse(status=resp.status_code)

            return redirect(reverse('vote_detail', args=[pollid, voterid]))

    else:
        form = CreateVoteForm()

    return render(
        request,
        'vote_create.html',
        {'form': form, 'pollid': pollid}
    )


def vote_detail_view(request, pollid, voterid):
    # Send request to DEON Service API for vote data
    resp = requests.get(f'{API_URL}/vote/{pollid}/{voterid}')
    if resp.status_code >= 300:
        return HttpResponse(status=resp.status_code)

    resp_str = resp.content.decode('UTF-8')
    resp_json = json.loads(resp_str, strict=False)

    return render(
        request,
        'vote_detail.html',
        context={'vote': resp_json, 'voterid': voterid}
    )


def poll_create_view(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)

        if form.is_valid():
            payload = {
                'pollid': str(form.cleaned_data['pollid']),
                'content': form.cleaned_data['name'],
            }
            resp = requests.post(f'{API_URL}/poll', json=payload)
            if resp.status_code >= 300:
                return HttpResponse(status=resp.status_code)

            # create poll proxy object and save it to db
            Poll(id=payload['pollid'], name=payload['content']).save()

            return redirect(
                reverse('poll_detail', args=[form.cleaned_data['pollid']])
            )

    else:
        form = CreatePollForm()

    return render(request, 'poll_create.html', {'form': form})


def poll_detail_view(request, pollid):

    poll_resp = requests.get(f'{API_URL}/poll/{pollid}')
    if poll_resp.status_code >= 300:
        return HttpResponse(status=poll_resp.status_code)

    poll_resp_str = poll_resp.content.decode('UTF-8')
    poll_resp_json = json.loads(poll_resp_str, strict=False)
    poll_resp_json['Content'] = json.loads(poll_resp_json['Content'])

    votes = requests.get(
        f'{API_URL}/vote',
        params={'type': 'public', 'pollid': pollid}
    )
    if votes.status_code >= 300:
        return HttpResponse(status=votes.status_code)

    votes_str = votes.content.decode('UTF-8')
    votes_json = json.loads(votes_str, strict=False)

    context_dict = {
        'poll_info': poll_resp_json,
        'votes': votes_json,
    }

    return render(request, 'poll_detail.html', context=context_dict)
