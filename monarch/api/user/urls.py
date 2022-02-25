from django.urls import path
from monarch.api.user import views

urlpatterns = [
    # path('users/', views.snippet_list),
    path('foo/', views.foo),
    # path('snippets/<int:pk>/', views.snippet_detail),
]
