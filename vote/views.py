from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView


from vote.forms import CreateVoteForm, CreatePollForm


import json
import requests


API_URL = 'http://localhost:8000/api/v1'


class HomePageView(TemplateView):
    template_name = 'home.html'


def vote_create_view(request, pollid):

    if request.method == "POST":
        form = CreateVoteForm(request.POST)

        if form.is_valid():

            voterid = form.cleaned_data['voterid']

            payload = {}
            payload['pollID'] = str(pollid)
            payload['voterID'] = str(voterid)
            payload['sex'] = form.cleaned_data['sex']
            payload['age'] = str(form.cleaned_data['age'])
            payload['content'] = form.cleaned_data['choice']

            resp = requests.post(f'{API_URL}/vote', json=payload)
            if resp.status_code >= 300:
                return HttpResponse(status=resp.status_code)

            return redirect(reverse('vote_detail', args=[pollid, voterid]))

    else:
        form = CreateVoteForm()

    return render(request, 'vote_create.html', {'form': form})


def vote_detail_view(request, pollid, voterid):

    # Send request to DEON Service API for vote data
    resp = requests.get(f'{API_URL}/vote/{pollid}/{voterid}')
    if resp.status_code >= 300:
        return HttpResponse(status=resp.status_code)

    resp_str = resp.content.decode('UTF-8')
    resp_json = json.loads(resp_str, strict=False)

    return render(request, 'vote_detail.html', context={'vote': resp_json})


def poll_create_view(request):

    if request.method == 'POST':
        form = CreatePollForm(request.POST)

        if form.is_valid():
            payload = {}
            pollid = form.cleaned_data['pollid']
            payload['pollid'] = str(pollid)
            payload['content'] = form.cleaned_data['name']

            resp = requests.post(f'{API_URL}/poll', json=payload)
            if resp.status_code >= 300:
                return HttpResponse(status=resp.status_code)

            return redirect(reverse('poll_detail', args=[pollid]))

    else:
        form = CreatePollForm()

    return render(request, 'poll_create.html', {'form': form})


def poll_detail_view(request, pollid):

    poll_resp = requests.get(f'{API_URL}/poll/{pollid}')
    if poll_resp.status_code >= 300:
        return HttpResponse(status=poll_resp.status_code)

    poll_resp_str = poll_resp.content.decode('UTF-8')
    poll_resp_json = json.loads(poll_resp_str, strict=False)

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
