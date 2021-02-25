from django.http.response import JsonResponse
from django.http.request import HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view

from .models import User
from .serializers import UserSerializer


@api_view(['GET', 'POST'])
def user(request: HttpRequest):
    if request.method == 'GET':
        try:
            user_object = User.objects.get(username=request.data['username'])
            user_serializer = UserSerializer(user_object)
            if user_serializer.data['password'] == request.data['password']:
                return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)
            return JsonResponse({'error': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            return JsonResponse({'error': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        try:
            User.objects.get(username=request.data['username'])
            return JsonResponse({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def scan(request: HttpRequest):
    try:
        longitude = request.data['location']['longitude']
        latitude = request.data['location']['latitude']
    except KeyError:
        return JsonResponse({"error": "location data not found"}, status=status.HTTP_400_BAD_REQUEST)
    lst = []
    users = User.objects.all()
    for user in users:
        user_serializer = UserSerializer(user)
        user_location = user_serializer.data['location']
        lst.append([pow(pow(user_location['latitude'] - latitude, 2) + pow(user_location['longitude'] - longitude, 2), 0.5), user_serializer.data['username']])
    lst.sort()
    return JsonResponse({'report': lst}, status=status.HTTP_200_OK)
