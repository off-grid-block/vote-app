from django.shortcuts import render
from django.http import HttpResponse


import json
import requests


class DeonClient:

    # DEON SDK API endpoint
    API_URL = 'http://localhost:8000/api/v1/'

    # HTTP method constants
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'

    # Object types
    VOTE = 'vote'
    POLL = 'poll'

    def __init__(self, obj_type=VOTE, pollid=None, voterid=None,
                 payload=None, method=GET, modifier=None):
        self.url = self.build_request_url(obj_type, pollid, voterid, modifier)

        # set HTTP method
        self.method = method

        # serialize data to json format
        try:
            self.payload_json = json.dumps(payload)
        except TypeError:
            print('failed to serialize payload to JSON')
            self.payload_json = None

    @classmethod
    def build_request_url(cls, obj_type, pollid, voterid, modifier):

        req_url = cls.API_URL + obj_type + '/'
        if pollid:
            req_url += str(pollid) + '/'
        if voterid:
            req_url += str(pollid) + '/'
        if modifier:
            req_url += str(pollid)

        return req_url

    def send_request(self):
        if self.method == self.GET:
            resp = requests.get(self.url)

        if self.method == self.POST:
            resp = requests.post(self.url, json=self.payload_json)

        if self.method == self.PUT:
            resp = requests.put(self.url, json=self.payload_json)

        if resp.status_code >= 300:
            self.error_status_code = resp.status_code

        resp_str = resp.content.decode('UTF-8')
        return json.loads(resp_str)


def create_vote_view(request):
    pass


def read_vote_view(request, pollid, voterid):

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


def create_poll_view(request):
    pass


def read_poll_view(request, pollid):
    pass


def update_poll_view(request, pollid):
    pass
