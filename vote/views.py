from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse


from vote.client import DeonClient
from vote.forms import CreateVoteForm, CreatePollForm


def vote_create_view(request, pollid):

    # pollid = 1234

    if request.method == "POST":
        form = CreateVoteForm(request.POST)

        if form.is_valid():
            voterid = form.cleaned_data['voterid']

            payload = {}
            payload['ollID'] = str(pollid)
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
    pass


def poll_detail_view(request, pollid):
    pass
