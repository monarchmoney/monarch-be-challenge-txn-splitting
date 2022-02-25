from django.http import HttpResponse, JsonResponse


def foo(request):
    return HttpResponse('FOO')
