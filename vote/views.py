from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from vote.forms import CreateVoteForm, CreatePollForm
from deon_apps.settings import API_URL

import json
import requests
import uuid


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            resp = requests.get(f'{API_URL}/poll')
        except requests.exceptions.Timeout:
            context['error'] = "Request to vote API timed out."
            return context
        except requests.exceptions.ConnectionError:
            context['error'] = "Failed to connect to vote API. Is it running?"
            return context
        except requests.exceptions.RequestException as e:
            raise(e)

        poll_resp_str = resp.content.decode('UTF-8')
        poll_resp_json = json.loads(poll_resp_str, strict=False)
        polls = [poll['Record'] for poll in poll_resp_json]

        context['polls'] = polls
        return context


@login_required
def vote_create_view(request, pollid):
    if request.method == "POST":
        form = CreateVoteForm(request.POST)

        if form.is_valid():

            # voterid = form.cleaned_data['voterid']
            voterid = request.user.voterid

            payload = {'pollID': str(pollid),
                       'voterID': str(voterid),
                       'sex': form.cleaned_data['sex'],
                       'age': str(form.cleaned_data['age']),
                       'content': form.cleaned_data['choice']}

            resp = requests.post(f'{API_URL}/vote', json=payload)

            if resp.status_code >= 300:
                return render(
                    request,
                    'error.html',
                    {'message': 'failed to create vote.'}
                )

            return redirect(reverse('vote_detail', args=[pollid, voterid]))

    else:
        form = CreateVoteForm()

    poll = requests.get(f'{API_URL}/poll/{pollid}')
    poll_str = poll.content.decode('UTF-8')
    poll_json = json.loads(poll_str, strict=False)

    return render(
        request,
        'vote_create.html',
        {'form': form, 'poll': poll_json}
    )


def vote_detail_view(request, pollid, voterid):
    # Send request to DEON Service API for vote data
    resp = requests.get(f'{API_URL}/vote/{pollid}/{voterid}')
    if resp.status_code >= 300:
        return render(
            request,
            'error.html',
            {'message': 'failed to get vote details.'}
        )

    resp_str = resp.content.decode('UTF-8')
    resp_json = json.loads(resp_str, strict=False)

    return render(
        request,
        'vote_detail.html',
        context={'vote': resp_json, 'voterid': voterid}
    )


@login_required
def poll_create_view(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)

        if form.is_valid():
            payload = {
                'pollid': str(uuid.uuid4()),
                'title': form.cleaned_data['title'],
                'content': form.cleaned_data['content'],
            }
            resp = requests.post(f'{API_URL}/poll', json=payload)

            if resp.status_code >= 300:
                return render(
                    request,
                    'error.html',
                    {'message': 'failed to create poll.'}
                )

            return redirect(
                reverse('poll_detail', args=[payload['pollid']])
            )

    else:
        form = CreatePollForm()

    return render(request, 'poll_create.html', {'form': form})


def poll_detail_view(request, pollid):

    poll = requests.get(f'{API_URL}/poll/{pollid}')
    if poll.status_code >= 300:
        return render(
                request,
                'error.html',
                {'message': 'failed to get poll details.'}
            )

    poll_str = poll.content.decode('UTF-8')
    poll_json = json.loads(poll_str, strict=False)
    if poll_json['Content']:
        poll_json['Content'] = json.loads(poll_json['Content'])

    votes = requests.get(
        f'{API_URL}/vote',
        params={'type': 'public', 'pollid': pollid}
    )
    if votes.status_code >= 300:
        return render(
            request,
            'error.html',
            {'message': 'failed to get vote details for this poll.'}
        )

    votes_str = votes.content.decode('UTF-8')
    votes_json = json.loads(votes_str, strict=False)

    context_dict = {
        'poll': poll_json,
        'votes': votes_json,
    }

    return render(request, 'poll_detail.html', context=context_dict)
