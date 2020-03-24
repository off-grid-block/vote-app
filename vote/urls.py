from django.urls import path
from vote.views import (
    create_vote_view,
    read_vote_view,
    create_poll_view,
    read_poll_view,
    update_poll_view,
)


urlpatterns = [

    path('vote/create', create_vote_view, name='create_vote'),
    path(
        'vote/<int:pollid>/<int:voterid>',
        read_vote_view,
        name='read_vote'
    ),

    path('poll/create', create_poll_view, name='create_poll'),
    path('poll/<uuid:pollid>', read_poll_view, name='read_poll'),
    path('poll/<uuid:pollid>/update', update_poll_view, name='update_poll')

]
