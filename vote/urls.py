from django.urls import path
from vote.views import (
    vote_create_view,
    vote_detail_view,
    poll_create_view,
    poll_detail_view,
    HomePageView,
)


urlpatterns = [

    path('<int:pollid>/new', vote_create_view, name='vote_create'),
    path('<int:pollid>/<int:voterid>',
         vote_detail_view, name='vote_detail'),

    path('new', poll_create_view, name='poll_create'),
    path('<int:pollid>', poll_detail_view, name='poll_detail'),

    path('', HomePageView.as_view(), name='homepage')

]
