from rest_framework import serializers
from .models import CustomUser,Package,PackageSelection,Comments,Blogs,Review,UserPayment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ObjectDoesNotExist


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # adding custom claims
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user.is_superuser==False:
            data["is_superuser"] = user.is_superuser
            data["username"] = user.username
            return data
        else:
            raise serializers.ValidationError("Only common users are allowed to log in here.")
        
    
class AdminTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # adding custom claims
        token['username'] = user.username
        token['is_superuser'] = user.is_superuser
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        if user.is_superuser==True:
                data["is_superuser"] = user.is_superuser
                data["username"] = user.username
                return data
        else:
            raise serializers.ValidationError(" Only administrators are allowed to log in here.")
        
        

class CustomUserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    image=serializers.ImageField(max_length=None,use_url=True,required=False)
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone', 'place', 'image', 'password','password_confirmation')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        try:
            CustomUser.objects.get(email=data['email'])
            raise serializers.ValidationError({'email':'Email already exists.'})
        except ObjectDoesNotExist:
            pass

        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({'password_confirmation':"Passwords do not match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation', None)
        user = CustomUser.objects.create_user(**validated_data)
        return user

class CustomUserupdateSerializer(serializers.ModelSerializer):
    image=serializers.ImageField(max_length=None,use_url=True,required=False)
    class Meta:
        model = CustomUser
        fields = ['username','image','phone','place','email']
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email__iexact=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("This email address is already in use.")
        return value
    

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        exclude = ['admin']

class PackagelistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"

class PackageSelectionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    package = PackageSerializer()

    class Meta:
        model = PackageSelection
        fields = '__all__'        

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['comment']

class CommentlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        exclude = ['user']

class BloglistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogs
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        
class ReviewlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPayment
        fields = "__all__"