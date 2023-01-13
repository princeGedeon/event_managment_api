from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers


from rest_framework.exceptions import ValidationError

from accounts.utils import Util

from accounts.models import User

from events.models import Guest


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':"password"},write_only=True)
    class Meta:
        model= User
        fields=['email',"nom","prenom","password","password2"]
        extra_kwargs={
            'password':{'write_only':True}
        }
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password!=password2:
            raise serializers.ValidationError('Password and Confirm Password doesn\'t match')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email',"password"]



class UserProfileSerializer(serializers.ModelSerializer):
    picture_url = serializers.CharField(source='picture.url', read_only=True)
    class Meta:
        model=User
        fields=['id',"email","nom","prenom","profile","longitude","latitude","number_phone","picture_url"]

class UserChangePasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':"password"},write_only=True)
    password2= serializers.CharField(max_length=255, style={'input_type': "password"}, write_only=True)
    class Meta:
        fields=['password',"password2"]

    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password!=password2:
            raise serializers.ValidationError('Password and Confirm Password doesn\'t match')
        user.set_password(password)
        user.save()
        return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        fields=['email',]

    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)

            uid=urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded uuid')
            token=PasswordResetTokenGenerator().make_token(user)
            print("Password Reset Token",token)
            link="http://localhost:9000/api/user/reset-password/"+uid+'/'+token
            print("Password Reset Link",link)
            # EMail sen0
            body='Click Following Link to Reset your password '+link
            data={
                'subject':"Reset Yout Password",
                "body":body,
                "to_email":user.email
            }
            Util.send_mail(data)
            return attrs
        else:
            raise ValidationError("You are not a Registered User")

class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': "password"}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': "password"}, write_only=True)

    class Meta:
        fields = ['password', "password2"]

    def validate(self, attrs):
       try:
           password = attrs.get('password')
           password2 = attrs.get('password2')
           uid = self.context.get('uid')
           token = self.context.get('token')

           if password != password2:
               raise serializers.ValidationError('Password and Confirm Password doesn\'t match')
           id = smart_str(urlsafe_base64_decode(uid))
           user = User.objects.get(id=id)
           if not PasswordResetTokenGenerator().check_token(user, token):
               raise ValidationError('Token is not valid or expired')

           user.set_password(password)
           user.save()
           return attrs

       except DjangoUnicodeDecodeError as identifier:
           PasswordResetTokenGenerator().check_token(user,token)
           raise ValidationError('Token is not valid')

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["nom","prenom","number_phone","longitude","latitude"]

class UpdateProfilePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['picture']

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ('id', 'event', 'user', 'status','feedback','rating','created_at')
        read_only_fields = ('event', 'user', 'created_at')