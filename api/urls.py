"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from stock import views
from rest_framework.authtoken.views import obtain_auth_token
from stock.views import MyTokenObtainPairView

#for swaggger docs
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import(
    #TokenObtainPairView,
    TokenRefreshView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="User Registration and Book API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.ourapp.com/policies/terms/",
        contact=openapi.Contact(email="muchhaladeepika@gmail.com"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    #path('',views.display_api),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('email-verify/',views.VerifyEmail.as_view(),name='verifyemail'),
    path('crud/',views.crud_operations),
    path('crud/<int:pk>',views.crud_operations),

    path('token/',MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name="token_refresh_view"),

    path('filter',views.BookList.as_view()),
    #urls for session authentication
    path('auth/',include('rest_framework.urls',namespace='rest_framework')),

    #urls for mixins
    # path('crud/',views.BookList1.as_view()),
    # path('crud/<int:pk>',views.BookList2.as_view())

    #url to generate token using obtain_auth
    #path('gettoken/',obtain_auth_token)

    #url to generate view using signals 

    #urls for swagger docs 
    path('', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),

]
