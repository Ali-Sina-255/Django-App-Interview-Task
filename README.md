# Django-App-Interview-Task
### Task: Build a REST API for a "Job Processing System" where users can register
using their email, verify their email using an OTP, and submit jobs that are
processed asynchronously. The system should handle job creation, scheduling,
and processing through a queue, and include reporting on job statuses and
results.
User should be able to comment on a job, another field to propose a deadline and
field to offer his fee for the task (For example: I can complete this job very well,
2024/8/25, 80$). The poster should be able to select a bidder. The user should be
able to see his assigned jobs.
The OTP email should be sent in the background so the user must not be kept
waiting.

## Installation
To run the app locally, follow these steps:
Clone the repository:
# Install the required libraries:
Ensure you have Python installed. Then, install the necessary packages using pip:
### git clone https://github.com/Ali-Sina-255/
### cd Weather-Forecast
### python3 - m venv venv 
### source venv/bin/activate
#### pip install -r requirements.txt

#### Requirements
1. User Authentication with Email Verification:
Implement user registration using email.
Generate and send a One-Time Password (OTP) to the user's email upon
registration.
Implement an endpoint for OTP verification.
Users cannot perform any job-related operations until their email is
verified.
2. Models:
User : Extend the default Django User model or use a custom model to
include fields like is_email_verified .
OTP : Model to store OTPs with fields like user , otp_code , created_at , and
is_used .
Django App Interview Task
1Job : Represents a job with fields like name, description, created_at,
scheduled_time, status (e.g., pending, in-progress, completed, failed), and
result.
JobResult : Represents the result of a job, including details like job (foreign
key to Job ), output, error_message (if any), and completed_at.
3. Queue and Scheduling:
Use Celery or RQ (Redis Queue) for asynchronous job processing.
Implement scheduling using Django’s management commands or Celery’s
periodic tasks.
Jobs should be placed in a queue and processed at their scheduled time.
4. Endpoints:
Authentication:
POST /api/register/
- Register a new user by providing an email.
POST /api/verify-email/
POST /api/login/
- Verify the user's email with the OTP sent.
- Login and obtain a token (only if the email is verified).
### Job Management:
GET /api/jobs/
- List all jobs for the authenticated user (only for verified
users).
POST /api/jobs/
- Create a new job with a scheduled time.
GET /api/jobs/<id>/
- Retrieve details of a specific job.
DELETE /api/jobs/<id>/
- Cancel a job if it hasn’t been processed yet.
Job Results:
GET /api/jobs/<id>/result/
- Retrieve the result of a completed job.
5. Permissions:
Only authenticated and email-verified users can access job-related
endpoints.
Users can only view and manage their own jobs and results.
Django App Interview Task
26. Validation:
Validate that jobs scheduled in the past cannot be created.
Ensure that results are only available for completed jobs.
Validate OTP expiration and uniqueness.
7. Testing (Optional):
Write unit tests for the API views, focusing on permissions, validations,
OTP verification, and job management.
Include tests for job scheduling, queueing, and processing.
8. Bonus:
Implement job retry logic if a job fails.
Add filtering and sorting for jobs based on status, scheduled time, or
creation date.
Include a dashboard view that summarizes job statuses (e.g., how many
are pending, in-progress, completed, failed).
Instructions for Candidates
1. Setup: Provide a Django project setup with necessary dependencies
(including Celery or RQ, Redis, etc.).
2. Time Limit: Allocate 8-10 days for completion.
### 3. Expectations:
Properly structured views, serializers, models, and OTP handling.
Email OTP sending mechanism (using a library like Django’s send_mail or
third-party services).
Robust authentication flow with email verification.
Handling of asynchronous task processing, queueing, and scheduling.
Comprehensive unit tests.
### 4. Submission: Ask for a GitHub repository submission with clear setup
instructions.
