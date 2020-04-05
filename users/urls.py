from django.urls import path
from users.views import user_vote_view, HomePageView, SignupPageView


urlpatterns = [
    path('<int:userid>/vote', user_vote_view, name='user_vote'),
    path('', HomePageView.as_view(), name='homepage'),
    path('signup', SignupPageView.as_view(), name='signup')
]
