from rest_framework import serializers
from .models import Book,User

#using Serializer
class BookSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    section=serializers.CharField(max_length=100)
    name=serializers.CharField(max_length=100)
    nfp=serializers.IntegerField()
    cat=serializers.CharField()

    #field level validation 
    def validate_id(self,value):
        if value>=500:
            raise serializers.ValidationError('No place to accomodate more books')
        return value

    

    def create(self, validate_data):
        return Book.objects.create(**validate_data)

    def update(self,instance,validate_data):
        instance.section = validate_data.get('section', instance.section)
        instance.name = validate_data.get('name', instance.name)
        instance.nfp = validate_data.get('nfp', instance.nfp)

        instance.save()
        return instance

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=50,min_length=8,write_only=True)

    class Meta:
        model=User
        fields=['email','username','password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('The username should contain alphanumeric characters')
        return attrs
    
    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class EmailVerficationSerializer(serializers.ModelSerializer):
    token=serializers.CharField(max_length=555)

    class Meta:
        model=User
        fields = ['token']


#using ModelSerializer
# class BookSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Book
#         fields=['id','section','name','nfp']