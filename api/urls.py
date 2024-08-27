from django.urls import path
from . import views


urlpatterns = [
	path('', views.all_jobs,  name='job-list'),
	path('job/detail/<int:pk>/', views.job_detail,  name='job-detail-list'),
	path('job-create', views.JobListCreateView.as_view(),  name='job-create'),
	path('register/', views.RegisterView.as_view(), name='register'),
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('login/', views.LoginView.as_view(), name='login'),
	path('jobs/<int:pk>/', views.JobDetailView.as_view(), name='job-detail'),
	path('jobs/<int:pk>/update/', views.JobUpdateView.as_view(), name='job-update'),
	path('jobs/<int:pk>/result/', views.JobResultView.as_view(), name='job-result'),

]
