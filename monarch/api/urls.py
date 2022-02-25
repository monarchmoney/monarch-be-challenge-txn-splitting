from django.urls import path, include

# from monarch.api.user import urls as user_urls

urlpatterns = [
    path('', include('monarch.api.user.urls')),
]
