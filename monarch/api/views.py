from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from monarch.api.serializers import UserSerializer
from monarch.db.models import User


def foo(request):
    return HttpResponse('FOO')


class UserList(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        data = UserSerializer(users, many=True).data
        return Response(data)
