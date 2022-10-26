# DRF Dependencies
from rest_framework import  serializers

# Models
from authentication.models import CustomUser, Profile, WorkerType

# Serializers
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id','email','password','first_name', 'last_name', 'phone', 'job_title')
        extra_kwargs = {
            'password':{'write_only': True},
        }
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
               username = validated_data['first_name'].lower() + "" + validated_data['last_name'].lower(),
               email = validated_data['email'],
               password = validated_data['password'],
               first_name=validated_data['first_name'],  
               last_name=validated_data['last_name'],
               phone = validated_data['phone'],
               job_title = validated_data['job_title']
               )
        return user
    

# User serializer
class UserSerializer(serializers.ModelSerializer):
    
    picture = serializers.SerializerMethodField('get_profile_picture')
    class Meta:
        model = CustomUser
        fields = ('pk', 'first_name', 'last_name', 'email', 'phone', 'job_title', 'is_online_in_app', 'picture')
        
    def get_profile_picture(self, CustomUser):
        _id = CustomUser.pk
        try:
            profile = Profile.objects.get(user=_id)
            picture = profile.profile_picture
        except:
            picture = ""
        return str(picture)

class MembersSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField('get_full_name')
    user_name = serializers.SerializerMethodField('get_username')
    picture = serializers.SerializerMethodField('get_profile_picture')
    class Meta:
        model = CustomUser
        fields = ['pk','first_name', 'last_name', 'full_name','user_name','email','phone','picture']

    def get_full_name(self, CustomUser):
        full_name = CustomUser.get_full_name_user()
        return full_name['full_name']
    
    def get_username(self,CustomUser):
        user_name = CustomUser.get_username()
        return user_name

    def get_profile_picture(self, CustomUser):
        _id = CustomUser.pk
        profile = Profile.objects.get(user=_id)
        picture = profile.profile_picture
        return str(picture)

class UserProfileSerializer(serializers.ModelSerializer):

    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'

class PhotoProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class WorkerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkerType
        fields = '__all__'
        
