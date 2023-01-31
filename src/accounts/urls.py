from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
TokenVerifyView
)
from accounts.views import UpdateProfilePictureView,UserPasswordResetView,UpdateUserView,SendPasswordResetEmailView,UserProfileView,UserChangePasswordView,UserRegistrationView,UserLoginView

urlpatterns = [
   path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
   path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   path('register/',UserRegistrationView.as_view(),name='register'),
      path('update/', UpdateUserView.as_view(), name='update_profile'),
   path('update_picture/', UpdateProfilePictureView.as_view(), name='update_profile'),
   path('login/',UserLoginView.as_view(),name="login"),
   path('profile/',UserProfileView.as_view(),name="profile"),
path('changepassword/',UserChangePasswordView.as_view(),name="changepassword"),
   path('send-reset-password-mail/',SendPasswordResetEmailView.as_view(),name="reset_password_email"),
   path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name="reset-password")
]