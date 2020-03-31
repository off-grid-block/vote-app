import json
import requests


class DeonClient:

    # DEON SDK API endpoint
    API_URL = 'http://localhost:8000/api/v1'

    # HTTP method constants
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'

    # Object types
    VOTE = 'vote'
    POLL = 'poll'

    def __init__(self, obj_type=VOTE, pollid=None, voterid=None,
                 payload=None, method=GET, modifier=None):

        self.method = method
        self.error_status_code = None
        self.url = self.build_request_url(obj_type, pollid, voterid, modifier)
        self.payload = payload

        # # serialize data to json format
        # try:
        #     self.payload_json = json.dumps(payload)
        # except TypeError:
        #     print('failed to serialize payload to JSON')
        #     self.payload_json = None

    @classmethod
    def build_request_url(cls, obj_type, pollid, voterid, modifier):
        params = [cls.API_URL, obj_type, pollid, voterid, modifier]
        return '/'.join([str(p) for p in params if p])

    def send_request(self):
        if self.method == self.GET:
            resp = requests.get(self.url)

        elif self.method == self.POST:
            resp = requests.post(self.url, json=self.payload)

        elif self.method == self.PUT:
            resp = requests.put(self.url, json=self.payload)

        if resp.status_code >= 300:
            self.error_status_code = resp.status_code
            return resp.text

        resp_str = resp.content.decode('UTF-8')
        if resp_str:
            return json.loads(resp_str)
