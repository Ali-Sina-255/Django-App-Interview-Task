from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('commands', views.CommandViewSet)


urlpatterns = [
 
    path('', include(router.urls)),
	path('jobs/', views.all_jobs,  name='job-list'),
	path('job/detail/<int:pk>/', views.job_detail_view,  name='job-detail-list'),
	path('job-list/', views.JobListCreateView.as_view(),  name='job-create'),
	path('register/', views.RegisterView.as_view(), name='register'),
 	path('activate-api/<uidb64>/<token>/', views.activate_api, name='activate_api'),
	path('register/update/', views.ProfileUpdateView.as_view(), name='profile-update'),
  	path('profile/update/', views.ProfileUpdateView.as_view(), name='profile-update'),
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout-api'),
	path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
	path('jobs/<int:pk>/update/', views.JobUpdateView.as_view(), name='job-update'),
	path('jobs/<int:pk>/result/', views.JobResultView.as_view(), name='job-result'),
 
 
 ]
