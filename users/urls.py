from django.urls import path, include
from users.views import UserProfileView

urlpatterns = [

    path('profile/',UserProfileView.as_view(), name='user-profile')
]
