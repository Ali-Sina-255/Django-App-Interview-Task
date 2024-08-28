from django.urls import path

from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('register', views.user_registration, name='register_user'),
    path('login/', views.login_view, name='login-user'),
    path('otp/', views.otp_views, name='otp'),
    path('logout/', views.logout_view, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate_view, name='reset_password_validate'),
    path('rest_password', views.reset_password_view, name='reset_password'),

]
