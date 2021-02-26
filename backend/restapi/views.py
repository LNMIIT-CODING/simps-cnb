from django.http.response import JsonResponse
from django.http.request import HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view

from .models import User, Client
from .serializers import UserSerializer, ClientSerializer


@api_view(['GET'])
def exists(request: HttpRequest, choice: int):
    try:
        if choice == 0:
            User.objects.get(mobile_num=request.data['mobile_num'])
        elif choice == 1:
            Client.objects.get(mobile_num=request.data['mobile_num'])
        return JsonResponse({'report': 'exists'}, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return JsonResponse({'report': 'does not exist'}, status=status.HTTP_200_OK)
    except KeyError:
        return JsonResponse({'error': 'incomplete request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def user(request: HttpRequest):
    if request.method == 'GET':
        try:
            user_object = User.objects.get(mobile_num=request.data['mobile_num'])
            user_serializer = UserSerializer(user_object)
            if 123 == request.data['OTP']:
                return JsonResponse(user_serializer.data, status=status.HTTP_200_OK)
            return JsonResponse({'error': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            return JsonResponse({'error': 'incomplete request'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        try:
            User.objects.get(mobile_num=request.data['mobile_num'])
            return JsonResponse({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            user_serializer = UserSerializer(data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def client(request: HttpRequest):
    if request.method == 'GET':
        try:
            client_object = Client.objects.get(mobile_num=request.data['mobile_num'])
            client_serializer = ClientSerializer(client_object)
            if 123 == request.data['OTP']:
                return JsonResponse(client_serializer.data, status=status.HTTP_200_OK)
            return JsonResponse({'error': 'unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except KeyError:
            return JsonResponse({'error': 'incomplete request'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'client does not exist'}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        try:
            Client.objects.get(mobile_num=request.data['mobile_num'])
            return JsonResponse({'error': 'client already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            client_serializer = ClientSerializer(data=request.data)
            if client_serializer.is_valid():
                client_serializer.save()
                return JsonResponse(client_serializer.data, status=status.HTTP_201_CREATED)
            return JsonResponse(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'POST'])
# def post(request: HttpRequest):
#     if request.method == 'GET':
#         return JsonResponse({})
#     elif request.method == 'POST':
#         return JsonResponse({})


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
        lst.append(
            [pow(pow(user_location['latitude'] - latitude, 2) + pow(user_location['longitude'] - longitude, 2), 0.5),
             user_serializer.data['mobile_num']])
    lst.sort()
    return JsonResponse({'report': lst}, status=status.HTTP_200_OK)
