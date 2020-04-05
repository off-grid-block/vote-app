from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView


from client import DeonClient
from vote.forms import CreateVoteForm, CreatePollForm


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

            client = DeonClient(
                obj_type='vote', method=request.method, payload=payload)

            print(client.payload)

            err_resp = client.send_request()
            if client.error_status_code:
                print(err_resp)
                return HttpResponse(status=client.error_status_code)

            return redirect(reverse('vote_detail', args=[pollid, voterid]))

    else:
        form = CreateVoteForm()

    return render(request, 'vote_create.html', {'form': form})


def vote_detail_view(request, pollid, voterid):

    # all users can access the public vote information
    public_data_client = DeonClient(
        obj_type='vote', pollid=pollid, voterid=voterid, method=request.method)
    public_data_dict = public_data_client.send_request()

    if public_data_client.error_status_code:
        return HttpResponse(status=public_data_client.error_status_code)

    # **TODO**: add check for permission
    private_data_client = DeonClient(
        obj_type='vote', pollid=pollid, voterid=voterid,
        method=request.method, modifier='private')
    private_data_dict = private_data_client.send_request()

    if private_data_client.error_status_code:
        return HttpResponse(status=private_data_client.error_status_code)

    context_dict = {
        'public': public_data_dict,
        'private': private_data_dict,
    }

    return render(request, 'vote_detail.html', context=context_dict)


def poll_create_view(request):

    if request.method == 'POST':
        form = CreatePollForm(request.POST)

        if form.is_valid():
            payload = {}
            pollid = form.cleaned_data['pollid']
            payload['pollid'] = str(pollid)
            payload['content'] = form.cleaned_data['name']

            client = DeonClient(
                obj_type='poll', method=request.method, payload=payload
            )

            err_resp = client.send_request()
            if client.error_status_code:
                print(err_resp)
                return HttpResponse(status=client.error_status_code)

            return redirect(reverse('poll_detail', args=[pollid]))

    else:
        form = CreatePollForm()

    return render(request, 'poll_create.html', {'form': form})


def poll_detail_view(request, pollid):

    # requesting public data

    public_data_client = DeonClient(
        obj_type='poll', pollid=pollid, method=request.method)
    public_data_resp = public_data_client.send_request()

    if public_data_client.error_status_code:
        print('Error while requesting public poll data')
        return HttpResponse(status=public_data_client.error_status_code)

    # requesting private data

    private_data_client = DeonClient(
        obj_type='poll', pollid=pollid, method=request.method,
        modifier='private')
    private_data_resp = private_data_client.send_request()

    if private_data_client.error_status_code:
        print('Error while requesting private poll data')
        return HttpResponse(status=private_data_client.error_status_code)

    # querying vote data

    vote_data_client = DeonClient(
        obj_type='vote', params={'type': 'public', 'pollid': pollid},
        method=request.method)
    vote_data_resp = vote_data_client.send_request()

    if vote_data_client.error_status_code:
        print(f'Error while requesting vote data for poll {pollid}')
        return HttpResponse(status=vote_data_client.error_status_code)

    context_dict = {
        'public': public_data_resp,
        'private': private_data_resp,
        'votes': vote_data_resp
    }

    return render(request, 'poll_detail.html', context=context_dict)
