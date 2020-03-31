from django.urls import path
from vote.views import (
    vote_create_view,
    vote_detail_view,
    poll_create_view,
    poll_detail_view,
)


urlpatterns = [

    # poll management
    path('<int:pollid>/new', vote_create_view, name='vote_create'),
    # re_path(r'new$', poll_create_view, name='poll_create'),
    # re_path(r'<int:pollid>$', poll_detail_view, name='poll_detail'),
    path('<int:pollid>/<int:voterid>',
         vote_detail_view, name='vote_detail'),

]
