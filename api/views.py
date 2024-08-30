from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, permissions, viewsets, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


from .models import Job, JobResult, Command
from .forms import CommandForm
from .filters import JobFilter
from .paginations import DefaulPagination
from .serializers import JobSerializer, JobResultSerializer, RegisterSerializer, VerifyEmailSerializer, LoginSerializer,ProfileUpdateSerializer,CommandSerializer
from accounts.tasks import send_verification_email_task_api, execute_command_task
from django.contrib.auth import get_user_model


from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages


User = get_user_model()

class CommandViewSet(viewsets.ModelViewSet):
    queryset = Command.objects.all()
    serializer_class = CommandSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']
    filterset_class = JobFilter
    pagination_class = DefaulPagination
    search_fields = ['name', 'description', 'stats']
    ordering_fields = ['name', 'price', 'scheduled_time', 'updated_at']

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
        if job.status == 'completed':
            return Response({"detail": "Cannot update a completed job."}, status=400)
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




class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
           
            if not user.is_email_verified:
                send_verification_email_task_api.delay(
                    user_id=user.id,
                    email_subject="Verify Your Email Address",
                    email_template="accounts/email/verification_email_api.html",
                    host="localhost:8000"  # Ensure this is correct and consistent
                    )
                return Response({"detail": "Verification email sent successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Email is already verified."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)      
        
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


def all_jobs(request):
    all_jobs = Job.objects.all()
    context = {
        'jobs': all_jobs
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


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all() 
    serializer_class = RegisterSerializer 
    
class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileUpdateSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.delete()

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist, OverflowError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        messages.success(request, "Congratulations, your account is activated.")
        return redirect("login")
    else:
        messages.error(request, "Invalid Activation link.")
        return redirect("register")


