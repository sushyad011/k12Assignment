from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model,authenticate

from .user_serializers import UserRegisterSerializer

class UserRegister(APIView):
    """
    post:
    Register new user
    """

    def post(self, request):

        new_user = UserRegisterSerializer(data=request.data)
        if new_user.is_valid():
            try:
                new_user.validated_data['password'] = make_password(new_user.validated_data['password'])
                created_user = get_user_model().objects.create(**new_user.validated_data)

                return Response(
                    {
                        'status': status.HTTP_201_CREATED,
                        'message': 'User registered successfully',

                    },status=status.HTTP_201_CREATED
                )
            except Exception as e:
                error_msgs = ''
                for key, value in new_user.errors.items():
                    error = {'field': key, 'message': value}
                    error_msgs = str(key ) + ':' + str(value[0]) + ' '
                return Response(
                    {
                        'message' : 'Server error',
                        'error_message' : error_msgs,
                    },status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        error_msg = ''
        for key,value in new_user.errors.items():
            error = {'field' : key, 'message': value}
            if key == 'password':
                error_msg = str(key) + ':' + str(value[0]) + ' '
            else:
                error_msg = str(value[0]) + ' '

        return Response(
            {
                'status': status.HTTP_400_BAD_REQUEST,
                'error': error_msg,
            },status=status.HTTP_400_BAD_REQUEST
        )

class LogInUser(APIView):
    """
    post:
    login API
    """

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if username and password:
            try:
                user  =authenticate(username=username, password=password)
                if user and user.is_active and user.is_staff == False:
                    try:
                        token = Token.objects.get(user=user)
                    except Token.DoesNotExist:
                        toeknn= Token.objects.create(user=user)

                    return Response(
                        {
                            'status': status.HTTP_200_OK,
                            'message': 'Successfully logged in',
                            'token' : str(token),
                        },status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {
                            'message':'Invalid credentials',
                        },status=status.HTTP_401_UNAUTHORIZED
                    )
            except Exception as e:
                return  Response(
                    {
                        'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'error': str(e),
                    },status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'error': 'Email and password are required fields',
                },status=status.HTTP_400_BAD_REQUEST
            )