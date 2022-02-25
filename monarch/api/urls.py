from django.urls import path

from monarch.api import views

urlpatterns = [
    path('users/me', views.UserMe.as_view()),
    path('accounts', views.AccountList.as_view()),
    path('accounts/<str:pk>', views.AccountDetail.as_view()),
    path('categories', views.CategoryList.as_view()),
    path('categories/<str:pk>', views.CategoryDetail.as_view()),
]
