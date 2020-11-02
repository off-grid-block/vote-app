from django.urls import path
from vote.views import (
    vote_create_view,
    vote_detail_view,
    poll_create_view,
    poll_detail_view,
    register_view,
    HomePageView,
)


urlpatterns = [

    path('<uuid:pollid>/new', vote_create_view, name='vote_create'),
    path('<uuid:pollid>/<uuid:voterid>',
         vote_detail_view, name='vote_detail'),

    path('new', poll_create_view, name='poll_create'),
    path('<uuid:pollid>', poll_detail_view, name='poll_detail'),
    path('register', register_view, name='register'),

    path('', HomePageView.as_view(), name='homepage')

]
