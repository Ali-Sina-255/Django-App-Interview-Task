
from django.contrib.auth  import get_user_model
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Job
from . forms import CommandForm
from .filters import JobFilter
from .serializers import JobSerializer, JobResultSerializer, RegisterSerializer, VerifyEmailSerializer,LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics,status
from accounts.tasks import send_verification_email_task , execute_command_task



class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status'] 
    filterset_class = JobFilter
    search_fields = ['name','description','stats']
    ordering_fields = ['name','price','scheduled_time','updated_at']
    
    def get_queryset(self):
        if not self.request.user.is_email_verified:
            raise PermissionDenied("User not verified.")
        return Job.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class JobDetailView(generics.RetrieveDestroyAPIView):
	serializer_class = JobSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_queryset(self):
		return Job.objects.filter(user=self.request.user)

	def delete(self, request, *args, **kwargs):
		job = self.get_object()
		if job.status != 'completed':
			job.cancel()
			return Response({"detail": "Job canceled successfully."}, status=204)
		return Response({"detail": "Cannot cancel a completed job."}, status=400)



class JobUpdateView(generics.UpdateAPIView):
	serializer_class = JobSerializer
	permission_classes = [permissions.IsAuthenticated]
	authentication_classes = [JWTAuthentication]

	def get_queryset(self):
		return Job.objects.filter(user=self.request.user)

	def update(self, request, *args, **kwargs):
		job = self.get_object()

		# Check if the job status is 'completed'
		if job.status == 'completed':
			return Response({"detail": "Cannot update a completed job."}, status=400)
		
		# If not completed, proceed with the update
		return super().update(request, *args, **kwargs)



class JobResultView(generics.RetrieveAPIView):
	serializer_class = JobResultSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_object(self):
		job = Job.objects.filter(user=self.request.user, pk=self.kwargs['pk']).first()
		if not job or not job.is_completed():
			raise NotFound("Job not found or not completed yet.")
		try:
			return job.jobresult  
		except JobResult.DoesNotExist:
			raise NotFound("Job result not available.")



class RegisterView(generics.CreateAPIView):
	User = get_user_model()
	queryset = User.objects.all()
	serializer_class = RegisterSerializer


class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    User = get_user_model()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')

        try:
            user = self.User.objects.get(email=email)
            if not user.is_email_verified:
                # Send verification email
                send_verification_email_task.delay(
                    user_id=user.id,
                    email_subject="Verify Your Email Address",
                    email_template="accounts/email/verification_email.html",
                    domain="localhost://8000"  
                )

                return Response({"detail": "Verification email sent successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Email is already verified."}, status=status.HTTP_200_OK)

        except self.User.DoesNotExist:
            return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)


class LoginView(TokenObtainPairView):
	serializer_class = LoginSerializer


def all_jobs(request):
	all_jobs = Job.objects.all()
	context = {
		'jobs':all_jobs
	}
	return render(request, 'job/job_list.html', context)


@login_required
def job_detail_view(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    if request.method == 'POST':
        form = CommandForm(request.POST)
        if form.is_valid():
            command = form.save(commit=False)
            command.job = job
            command.owner = request.user.profile
            command.save()
            
            execute_command_task.delay(command.id)
            
            return redirect('job-detail-list', pk=pk)
    else:
        form = CommandForm()
    
    return render(request, 'job/job_detail.html', {'job': job, 'form': form})
