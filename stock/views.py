#to create ur api
from django.shortcuts import render
from .models import Book, User #model
from .serializers import BookSerializer,RegisterSerializer,EmailVerficationSerializer #serializer
from django.http import HttpResponse, JsonResponse #return info to the page
import io #convert stream into python data
from rest_framework.parsers import JSONParser #used to convert python data to object 
from rest_framework.renderers import JSONRenderer # used to convert python data to json data 
from django.views.decorators.csrf import csrf_exempt
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

#to add authetication and permission 
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import  BasicAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly

#customizing tokens
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

#to apply searching,ordering and pagination
from rest_framework import generics
from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter,OrderingFilter 


from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt #used to decode the token
from django.conf import settings
from rest_framework import views #this for the token acceptance
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

#To display the api 
def display_api(request):
    book1 = Book.objects.all()
    serializer1 = BookSerializer(book1, many=True)

    return JsonResponse(serializer1.data, safe=False)

class RegisterView(generics.GenericAPIView):
    serializer_class=RegisterSerializer

    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data=serializer.data
        user=User.objects.get(email=user_data['email'])

        token=RefreshToken.for_user(user).access_token
        
        current_site=get_current_site(request).domain
        relativeLink = reverse('verifyemail')
        
        absurl='http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'Hi '+user.username+'\nUse link below to verify your email\n'+absurl
        data={'email_body':email_body,'to_email': user.email,'email_subject':'Verify your email'}
        Util.send_email(data)

        return Response(user_data,status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    serializer_class = EmailVerficationSerializer

    token_param_config = openapi.Parameter('token',in_=openapi.IN_QUERY,description='Description',type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self,request):
        token=request.GET.get('token')
        try:
            payload = jwt.decode(token,settings.SECRET_KEY, options={"verify_signature":False})
            print(payload['user_id'])
            #print(User.objects.filter(id=21))
            # print(User.objects.get(id=1))
            # print(User.objects.filter(id=payload['user_id']))
            #if payload['user_id'] in User.objects.all():
            user=User.objects.get(id=payload['user_id'])
            print(user)
            print("after the user",token)
            print("inside the if statement",token)
            user.is_verified = True
            user.is_active = True
            user.is_staff = True
            user.save()
            return Response({'email':'Successfully activated'},status=status.HTTP_200_OK)
            # else:
            #     print('user doesnt exist')

            #     return Response({'email':"Activation unsuccessful"},status=status.HTTP_400_BAD_REQUEST)

            return Response({'email':'Successfully activated'},status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation Expired'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error':'Invalid token'},status = status.HTTP_400_BAD_REQUEST)
            
        

# class BookList1(ListModelMixin,CreateModelMixin,GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)#list is an built-in function of ListModelMixin
#         #to retrieve the data instead of self.list put self.retrieve

#     def post(self,request,*args,**kwargs):
#         return self.create(request, *args, **kwargs)

# class BookList2(RetrieveModelMixin,UpdateModelMixin, DestroyModelMixin,GenericAPIView):

#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
    
#     def put(self,request,*args,**kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self,request,*args,**kwargs):
#         return self.destroy(request, *args,**kwargs)
    
#     def get(self,request,*args,**kwargs):
#         return self.retrieve(request, *args,**kwargs)


@api_view(['GET','POST','PUT','PATCH','DELETE'])
#Basic authentication
# @authentication_classes([BasicAuthentication])
# @permission_classes([IsAdminUser])

#Session authentication
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])

#Token authentication
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def crud_operations(request,pk=None):
    if request.method=='GET':
        id=pk
        if id is not None:
            book1 = Book.objects.get(id=id)
            serializer = BookSerializer(book1)
            return Response(serializer.data)
        book1=Book.objects.all()
        serializer = BookSerializer(book1, many=True)
        return Response(serializer.data)
    
    if request.method=='POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Data created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method=='PUT':
        book1 = Book.objects.get(id=pk)
        serializer = BookSerializer(book1, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAS_REQUEST)
    
    if request.method=='PATCH':
        book1 = Book.objects.get(id=pk)
        serializer = BookSerializer(book1, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'Complete Data Updated'})
        return Response(serializer.errors, status=status.HTTP_400_BAS_REQUEST)
    
    if request.method=='DELETE':
        book1 = Book.objects.get(id=pk)
        book1.delete()
        return Response({'msg':'Data deleted'})


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

class BookList(generics.ListAPIView):
    # queryset = Book.objects.filter(section='chemistry').values()
    # print(queryset)
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    #class authentication
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields  = ['^name','^section','=name','=section']
    # '^' (start with )--> should start with a particular character
    #'='(exact) --> should be equal to the name 
    ordering_fields = '__all__'
    ordering = ['-section','name']



#to display,update,delete,post
# @csrf_exempt
# def crud_operations(request):
#     if request.method=='GET':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythondata = JSONParser().parse(stream)
#         id = pythondata.get('id', None)
#         if id is not None:
#             book1 = Book.objects.get(id=id)
#             serializer = BookSerializer (book1)
#             return JsonResponse(serializer.data)
#         # res = {'msg':'book not found'}
#         # return JsonResponse(res.data)

#     if request.method=='DELETE':
#         json_data=request.body
#         stream = io.BytesIO(json_data)
#         pythondata = JSONParser().parse(stream)
#         id = pythondata.get('id')
#         book1 = Book.objects.get(id=id)
#         book1.delete()
#         res = {'msg':'data deleted'}
#         return JsonResponse(res)

#     if request.method=='POST':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythondata = JSONParser().parse(stream)
#         serializer1 = BookSerializer(data = pythondata)
#         if serializer1.is_valid():
#             serializer1.save()
#             res = {'msg':'Data created'}
#             return JsonResponse(res)
#         return JsonResponse(serializer1.errors)

#     if request.method=='PUT':
#         json_data = request.body
#         stream = io.BytesIO(json_data)
#         pythondata = JSONParser().parse(stream)
#         id=pythondata.get('id')
#         book1 = Book.objects.get(id=id)
#         serializer1 = BookSerializer(book1, data=pythondata)
#         if serializer1.is_valid():
#             serializer1.save()
#             res={'msg':'Data updated'}
#             return JsonResponse(res)
#         return JsonResponse(serializer1.data)


#     return HttpResponse('Hello')


