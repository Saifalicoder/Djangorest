
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .serializer import UserSerializer as Userserializer
from .serializer import BookSerializer
from django.http import JsonResponse
import json
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import Book
User = get_user_model()


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        serializer = Userserializer(data=request.data)
        if not (first_name and last_name and email and password):
            return JsonResponse({'error': 'All fields are required.'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'A user with that email already exists.'})
        if serializer.is_valid():
            user = User.objects.create_user(username=first_name+'_'+last_name,
                                            email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
            return JsonResponse({'message': 'User created successfully.'})
        else:
            return Response(serializer.errors, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'})


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('username')
        password = data.get('password')
        # print("hello")
        print(email)
        print(password)
        if email and password:
            print("hello")
            user = authenticate(username=email, password=password)
            serializer = Userserializer(user, many=False)
            print(serializer.data)
            if user:
                refresh = RefreshToken.for_user(user)
                print(refresh)
                return JsonResponse(
                    {'user': serializer.data,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                     }
                )


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/user',
        'GET /api/books',
        'GET /api/user/:id',
        'GET /api/book/:id',
        'POST /api/users/login',
        'POST /api/signup',

    ]
    return Response(routes)


@api_view(['GET'])
def getUsers(request):
    user = User.objects.all()
    print(user)
    serializer = Userserializer(user, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUser(request, pk):
    user = User.objects.get(id=pk)
    print(user)
    serializer = Userserializer(user, many=False)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBooks(request):
    book = Book.objects.all()
    print(book)
    serializer = BookSerializer(book, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBook(request, pk):
    book = Book.objects.get(id=pk)
    print(book)
    serializer = BookSerializer(book, many=False)
    return Response(serializer.data)
