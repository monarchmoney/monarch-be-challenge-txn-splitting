from django.urls import path, include

urlpatterns = [
    path('', include('monarch.api.user.urls')),
]
