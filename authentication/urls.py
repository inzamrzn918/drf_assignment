from django.urls import path

from authentication.views import CSRFTokenView, UserRegistrationView, UserLoginView, \
    UserLogoutView, UserDetailsView, OTPVerificationView

urlpatterns = [
    path('csrf-token/', CSRFTokenView.as_view(), name='csrf_token'),
    path('register/', UserRegistrationView.as_view(), name='user_register'),
    path('verify-otp/', OTPVerificationView.as_view(), name='verify_otp'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('me/', UserDetailsView.as_view(), name='user_details'),

]