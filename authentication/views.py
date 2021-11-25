import json

# Django dependencies
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
from authentication.authTokenRotary import CsrfExemptTokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

# Models 
from authentication.models import CustomUser, Profile
# Serializers
from authentication.serializer import MembersSerializer, RegisterSerializer, UserProfileSerializer, UserSerializer

class LoginView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptTokenAuthentication,)
    serializer_class = UserSerializer
    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is not None:
            try:
                token = Token.objects.get(user_id=user.id)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            login(request, user)
            token_dict = {
            'token': str(token.key),  # None
            }
            resp = UserSerializer(user, context=self.get_serializer_context()).data
            resp.update(token_dict)
            return Response(
                resp,
                status=status.HTTP_200_OK)
        else:
            print("No existe el usuario")
            # No backend authenticated the credentials
            return Response([{'error':'Credenciales inválidas'}],status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    authentication_classes = (CsrfExemptTokenAuthentication,)

    def post(self, request):
        # Borramos de la request la información de sesión
        email = request.data.get('email')
        user = CustomUser.objects.get(email=email)
        try:
            token = Token.objects.get(user_id=user.id)
            token.delete()
        except:
            return Response([{'msg':'No existe un token para el usuario'}], status=status.HTTP_401_UNAUTHORIZED)
        # Devolvemos la respuesta al cliente
        return Response([{'msg':'Sesión cerrada correctamente'}], status=status.HTTP_200_OK)


class SignUpView(generics.GenericAPIView):
    authentication_classes = (CsrfExemptTokenAuthentication,)
    serializer_class = RegisterSerializer
    
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Usuario creado correctamente. Ahora puedes iniciar sesión",
        })

        
from django.core.files.base import ContentFile

def upload_photo(request):
    print(request.POST)
    responseData = {"msg":f"Photo has been uploaded"}
    return HttpResponse(json.dumps(responseData), content_type="application/json")

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import parser_classes

@parser_classes((MultiPartParser, ))
class UploadFileAndJson(APIView):

    def post(self, request, format=None):
        thumbnail = request.FILES["file"]
        user = CustomUser.objects.filter(pk = request.POST['id_user']).update(picture=thumbnail)
        print(thumbnail)
        print(user)
        return HttpResponse(json.dumps({"msg":"ok"}))

class CustomUserView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

class MembersView(ModelViewSet):
    serializer_class = MembersSerializer
    queryset = CustomUser.objects.all()

class UserProfileView(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = Profile.objects.all()

class ProfilePictureView(APIView):
    def get(self, request, id):
        print(request.data)
        profile = Profile.objects.get(user_id=id)
        id_user = profile.user_id
        pic = profile.profile_picture
        print(pic)
        #serializer = PhotoProfileSerializer(profile, many=True)
        return Response({
            "id_user" : id_user,
            "picture": str(pic)
        })
    
    def post(self, request, id):
        picture = request.data['file']
        profile = Profile.objects.get(user_id=id)
        profile.profile_picture = picture
        profile.save()
        new_picture = Profile.objects.get(user_id=id)
        url_image = new_picture.profile_picture
        return Response({
            "msg":"Imagen actualizada correctamente",
            "url_picture": str(url_image)
        })

class UpdateProfileView(APIView):
    def post(self, request):
        id_user = request.data['id']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        email = request.data['email']
        phone = request.data['phone']
        user = CustomUser.objects.get(pk=id_user)
        profile = Profile.objects.get(user_id=user.pk)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone = phone
        user.save()
        profile.save()
        return Response({
            "code": 200,
            "msg":"Perfil actualizado correctamente",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone": user.phone,
        })



        

