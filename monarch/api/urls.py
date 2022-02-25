from django.urls import path

from monarch.api import views

urlpatterns = [
    path('users/', views.UserList.as_view()),
    # path('users/<str:pk>', views.UserDetail.as_view()),
    path('foo/', views.foo),
]
