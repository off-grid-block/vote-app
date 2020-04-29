from django.apps import AppConfig
from deon_apps.settings import API_URL

import requests


class VoteConfig(AppConfig):
    name = 'vote'

    def ready(self):
        resp = requests.post(
            f'{API_URL}/application',
            json={'name': 'Voting', 'secret': 'kerapwd', 'type': 'user'}
        )
        if resp.status_code >= 300:
            raise RuntimeError('Failed to register  app with DEON service')
