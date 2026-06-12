from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout as auth_logout
import numpy as np
import joblib
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm
import base64
from io import BytesIO
from django.http import JsonResponse

from django.shortcuts import render
import numpy as np




def home(request):
    return render(request, 'users/home.html')

@login_required(login_url='users-register')


def index(request):
    return render(request, 'app/index.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

from .models import Profile

def profile(request):
    user = request.user
    # Ensure the user has a profile
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user)
    
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})







from django.shortcuts import render
from django.http import JsonResponse
# import random
# import json
import numpy as np
# from nltk.tokenize import word_tokenize
# from nltk.stem import WordNetLemmatizer
#from .models import Response, models
# from Chatbot.processor import chatbot_response
# Remove the comments to download additional nltk packages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@require_POST
@csrf_exempt
def chatbot_response_view(request):
    if request.method == 'POST':
        the_question = request.POST.get('question', '')
        # Chatbot temporarily disabled - requires TensorFlow/Keras
        response = "Chatbot is currently unavailable. Please install TensorFlow and Keras (requires 64-bit Python)."
        print(response)
        return JsonResponse({"response": response})
    else:
        return JsonResponse({"message": "This endpoint only accepts POST requests."})
 



def logout_view(request):  
    auth_logout(request)
    return redirect('/')





from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CaseForm
from .models import Case

@login_required
def register_case(request):
    if request.method == 'POST':
        form = CaseForm(request.POST, request.FILES)
        if form.is_valid():
            case = form.save(commit=False)
            case.user = request.user
            case.save()
            return redirect('user_dashboard')
    else:
        form = CaseForm()

    return render(request, 'app/register_case.html', {'form': form})


@login_required
def user_dashboard(request):
    case_type = request.GET.get('type')  # Get filter from URL

    if case_type:
        cases = Case.objects.filter(user=request.user, case_type=case_type)
    else:
        cases = Case.objects.filter(user=request.user)

    return render(request, 'app/dashboard.html', {'cases': cases})



from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def delete_case(request, case_id):
    case = get_object_or_404(Case, id=case_id, user=request.user)
    case.delete()
    return redirect('user_dashboard')
































from django.shortcuts import render, redirect
from django.contrib import messages
from .models import AdminUser
from .forms import AdminRegisterForm, AdminLoginForm

def admin_register(request):
    if request.method == 'POST':
        form = AdminRegisterForm(request.POST)
        if form.is_valid():
            # Save new admin
            admin_user = form.save(commit=False)
            admin_user.password = form.cleaned_data['password']
            admin_user.save()
            messages.success(request, "Admin account created successfully.")
            return redirect('admin-login')
    else:
        form = AdminRegisterForm()
    return render(request, 'admin_templates/admin_register.html', {'form': form})


def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                admin_user = AdminUser.objects.get(username=username, password=password)
                request.session['admin_user_id'] = admin_user.id
                
                return redirect('admin-dashboard')
            except AdminUser.DoesNotExist:
                messages.error(request, "Invalid username or password.")
    else:
        form = AdminLoginForm()
    return render(request, 'admin_templates/admin_login.html', {'form': form})


def admin_logout(request):
    if 'admin_user_id' in request.session:
        del request.session['admin_user_id']
    messages.success(request, "Admin logged out successfully.")
    return redirect('/')



def admin_dashboard(request):
    if 'admin_user_id' not in request.session:
        return redirect('admin-login')

    cases = Case.objects.all().order_by('-created_at')
    return render(request, 'admin_templates/admin_dashboard.html', {'cases': cases})








def start_Detection(request):
    return render(request, 'admin_templates/detect_stream.html')
































# from django.shortcuts import render, redirect
# from django.conf import settings
# from django.core.mail import EmailMessage
# from django.http import HttpResponse
# from twilio.rest import Client

# import os
# import cv2
# import uuid
# # import face_recognition  # Requires dlib and CMake
# import geocoder
# import numpy as np

# def detect_person(request):
#     from django.http import HttpResponse
#     return HttpResponse("Face recognition feature requires 'face-recognition' package. Please install CMake and Visual Studio Build Tools first.")

#     if 'admin_user_id' not in request.session:
#         return redirect('admin-login')

#     cases = Case.objects.filter(status='Pending')

#     known_encodings = []
#     known_case_ids = []

#     for case in cases:
#         image_path = os.path.join(settings.MEDIA_ROOT, str(case.image))
#         if os.path.exists(image_path):
#             img = face_recognition.load_image_file(image_path)
#             encodings = face_recognition.face_encodings(img)
#             if encodings:
#                 known_encodings.append(encodings[0])
#                 known_case_ids.append(case.id)

#     cap = cv2.VideoCapture(0)

#     if not cap.isOpened():
#         return HttpResponse("Camera not accessible")

#     while True:
#         success, frame = cap.read()
#         if not success:
#             break

#         rgb_frame = frame[:, :, ::-1]

#         face_locations = face_recognition.face_locations(rgb_frame)
#         face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#         for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

       
#             face_crop = frame[top:bottom, left:right]

#             if (bottom - top) < 100 or (right - left) < 100:
#                 continue

#             gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)

   
#             blur_value = cv2.Laplacian(gray, cv2.CV_64F).var()
#             if blur_value < 100:
#                 continue

     
#             brightness = np.mean(gray)
#             if brightness < 50:
#                 continue
   

#             if len(known_encodings) == 0:
#                 continue

#             face_distances = face_recognition.face_distance(known_encodings, face_encoding)

#             best_match_index = np.argmin(face_distances)

#             if face_distances[best_match_index] < 0.45:

#                 case = Case.objects.get(id=known_case_ids[best_match_index])

#                 if case.status == "Pending":

#                     filename = f"{uuid.uuid4().hex}.jpg"
#                     save_path = os.path.join(settings.MEDIA_ROOT, "detected", filename)
#                     os.makedirs(os.path.dirname(save_path), exist_ok=True)

#                     cv2.imwrite(save_path, face_crop)
#                     case.detected_image = f"detected/{filename}"

              
#                     g = geocoder.ip('me')
#                     if g.ok:
#                         case.latitude, case.longitude = g.latlng

#                     if case.case_type == "Missing":
#                         case.status = "Found"
#                     elif case.case_type == "Criminal":
#                         case.status = "Arrested"

#                     case.save()

          
#                     subject = f"{case.case_type} Case Update - {case.name}"
#                     message = f"""
# Hello,

# Good News!

# The person named {case.name} has been {case.status}.

# Location:
# Latitude: {case.latitude}
# Longitude: {case.longitude}

# Thank you,
# Missing & Criminal Detection System
# """

#                     email = EmailMessage(
#                         subject,
#                         message,
#                         settings.EMAIL_HOST_USER,
#                         [case.email],
#                     )

#                     image_path = os.path.join(settings.MEDIA_ROOT, str(case.detected_image))
#                     if os.path.exists(image_path):
#                         email.attach_file(image_path)

#                     email.send(fail_silently=False)

#                     # ================= SMS =================
#                     try:
#                         account_sid = "AC31546f4317a2633553e3e4bf1dbfe44e"
#                         auth_token = "3729e9c4fc7db2e3f05fdc3eb8fac189"
#                         twilio_number = "+12184195652"

#                         client = Client(account_sid, auth_token)

#                         phone_number = case.phone
#                         if not phone_number.startswith("+"):
#                             phone_number = "+" + phone_number

#                         sms_message = f"""
# ALERT!

# {case.name} has been {case.status}.

# Location:
# Lat: {case.latitude}
# Lng: {case.longitude}
# """

#                         client.messages.create(
#                             body=sms_message,
#                             from_=twilio_number,
#                             to=phone_number
#                         )

#                     except Exception as e:
#                         print("SMS Error:", e)

           
#                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#                 cv2.putText(frame, case.name, (left, top - 10),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

#         cv2.imshow("Missing & Criminal Detection", frame)

#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     cap.release()
#     cv2.destroyAllWindows()

#     return redirect('admin-dashboard')



from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from twilio.rest import Client
from .models import Case

import os
import cv2
import uuid
import face_recognition
import geocoder
import numpy as np


def detect_person(request):

    if 'admin_user_id' not in request.session:
        return redirect('admin-login')

    cases = Case.objects.filter(status='Pending')

    known_encodings = []
    known_case_ids = []

    for case in cases:
        image_path = os.path.join(settings.MEDIA_ROOT, str(case.image))
        if os.path.exists(image_path):
            img = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(img)
            if encodings:
                known_encodings.append(encodings[0])
                known_case_ids.append(case.id)

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return HttpResponse("Camera not accessible")

    while True:
        success, frame = cap.read()
        if not success:
            break

        rgb_frame = frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

            face_crop = frame[top:bottom, left:right]

            if (bottom - top) < 100 or (right - left) < 100:
                continue

            gray = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)

            blur_value = cv2.Laplacian(gray, cv2.CV_64F).var()
            if blur_value < 100:
                continue

            brightness = np.mean(gray)
            if brightness < 50:
                continue

            if len(known_encodings) == 0:
                continue

            face_distances = face_recognition.face_distance(known_encodings, face_encoding)

            best_match_index = np.argmin(face_distances)

            if face_distances[best_match_index] < 0.45:

                case = Case.objects.get(id=known_case_ids[best_match_index])

                if case.status == "Pending":

                    filename = f"{uuid.uuid4().hex}.jpg"
                    save_path = os.path.join(settings.MEDIA_ROOT, "detected", filename)
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)

                    cv2.imwrite(save_path, face_crop)
                    case.detected_image = f"detected/{filename}"

                    g = geocoder.ip('me')
                    if g.ok:
                        case.latitude, case.longitude = g.latlng

                    if case.case_type == "Missing":
                        case.status = "Found"
                    elif case.case_type == "Criminal":
                        case.status = "Found"

                    case.save()

                    subject = f"{case.case_type} Case Update - {case.name}"
                    message = f"""
Hello,

Good News!

The person named {case.name} has been {case.status}.

Location:
Latitude: {case.latitude}
Longitude: {case.longitude}

Thank you,
Missing & Criminal Detection System
"""

                    email = EmailMessage(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [case.email],
                    )

                    image_path = os.path.join(settings.MEDIA_ROOT, str(case.detected_image))
                    if os.path.exists(image_path):
                        email.attach_file(image_path)

                    email.send(fail_silently=False)

                

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, case.name, (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Missing & Criminal Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return redirect('admin-dashboard')

from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from .models import Case

import os
import cv2
import uuid
import geocoder
import numpy as np
import threading

# Safe import
try:
    import face_recognition
except ImportError:
    face_recognition = None


def process_video(video_path):

    if face_recognition is None:
        return

    # ================= Load Known Faces =================
    cases = Case.objects.filter(status='Pending')

    known_encodings = []
    known_case_ids = []

    for case in cases:

        image_path = os.path.join(settings.MEDIA_ROOT, str(case.image))

        if os.path.exists(image_path):

            img = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(img)

            if len(encodings) > 0:
                known_encodings.append(encodings[0])
                known_case_ids.append(case.id)

    if len(known_encodings) == 0:
        return

    # ================= Video Processing =================
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return

    frame_count = 0

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame_count += 1

        # Skip frames to improve speed
        if frame_count % 2 != 0:
            continue

        # Resize frame for performance
        frame = cv2.resize(frame, (640, 480))

        rgb_frame = frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

            face_distances = face_recognition.face_distance(known_encodings, face_encoding)

            best_match_index = np.argmin(face_distances)

            if face_distances[best_match_index] < 0.45:

                case = Case.objects.get(id=known_case_ids[best_match_index])

                if case.status == "Pending":

                    face_crop = frame[top:bottom, left:right]

                    filename = f"{uuid.uuid4().hex}.jpg"

                    detected_folder = os.path.join(settings.MEDIA_ROOT, "detected")
                    os.makedirs(detected_folder, exist_ok=True)

                    save_path = os.path.join(detected_folder, filename)

                    cv2.imwrite(save_path, face_crop)

                    case.detected_image = f"detected/{filename}"

                    # Get location
                    g = geocoder.ip('me')
                    if g.ok:
                        case.latitude, case.longitude = g.latlng

                    # Update case status
                    if case.case_type == "Missing":
                        case.status = "Found"

                    elif case.case_type == "Criminal":
                        case.status = "Found"

                    case.save()

                    print("Detected:", case.name)

    cap.release()


def detect_from_video(request):

    if 'admin_user_id' not in request.session:
        return redirect('admin-login')

    if face_recognition is None:
        return HttpResponse(
            "Face recognition feature requires 'face-recognition' package. "
            "Please install CMake and Visual Studio Build Tools first."
        )

    if request.method == "POST":

        if 'video' not in request.FILES:
            return HttpResponse("No video uploaded")

        video = request.FILES['video']

        video_folder = os.path.join(settings.MEDIA_ROOT, "videos")
        os.makedirs(video_folder, exist_ok=True)

        # Unique filename
        video_name = f"{uuid.uuid4().hex}_{video.name}"
        video_path = os.path.join(video_folder, video_name)

        # Save video
        with open(video_path, 'wb+') as destination:
            for chunk in video.chunks():
                destination.write(chunk)

        # Run video processing in background thread
        threading.Thread(target=process_video, args=(video_path,)).start()

        return HttpResponse("Video uploaded successfully. Detection running in background.")

    return render(request, "admin_templates/upload_video.html")


# ==================== PERFORMANCE METRICS ====================
from django.db.models import Count, Avg, Q
from django.db.models.functions import TruncDate
from datetime import datetime, timedelta
from django.utils import timezone

def performance_metrics(request):
    if 'admin_user_id' not in request.session:
        return redirect('admin-login')
    
    # Overall Statistics
    total_cases = Case.objects.count()
    pending_cases = Case.objects.filter(status='Pending').count()
    found_cases = Case.objects.filter(status='Found').count()
    arrested_cases = Case.objects.filter(status='Captured').count()
    resolved_cases = found_cases + arrested_cases
    
    # Case Type Distribution
    missing_cases = Case.objects.filter(case_type='Missing').count()
    criminal_cases = Case.objects.filter(case_type='Criminal').count()
    
    # Resolution Rate
    resolution_rate = (resolved_cases / total_cases * 100) if total_cases > 0 else 0
    
    # Average Resolution Time (in days)
    resolved_case_objects = Case.objects.filter(Q(status='Found') | Q(status='Captured'))
    avg_resolution_time = 0
    if resolved_case_objects.exists():
        total_time = 0
        count = 0
        for case in resolved_case_objects:
            if case.created_at:
                # Assuming resolution time is from creation to now (you can modify this)
                time_diff = (timezone.now() - case.created_at).days
                total_time += time_diff
                count += 1
        avg_resolution_time = total_time / count if count > 0 else 0
    
    # Cases by Status (Last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_cases = Case.objects.filter(created_at__gte=thirty_days_ago)
    
    # Daily case registration trend (Last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    daily_cases = Case.objects.filter(created_at__gte=seven_days_ago).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(count=Count('id')).order_by('date')
    
    # Monthly Statistics
    current_month = timezone.now().month
    current_year = timezone.now().year
    monthly_cases = Case.objects.filter(
        created_at__month=current_month,
        created_at__year=current_year
    ).count()
    
    monthly_resolved = Case.objects.filter(
        created_at__month=current_month,
        created_at__year=current_year
    ).filter(Q(status='Found') | Q(status='Arrested')).count()
    
    # Detection Success Rate (cases with detected images)
    cases_with_detection = Case.objects.exclude(detected_image='').count()
    detection_success_rate = (cases_with_detection / total_cases * 100) if total_cases > 0 else 0
    
    # User Engagement
    total_users = User.objects.count()
    active_users = Case.objects.values('user').distinct().count()
    
    context = {
        'total_cases': total_cases,
        'pending_cases': pending_cases,
        'found_cases': found_cases,
        'arrested_cases': arrested_cases,
        'resolved_cases': resolved_cases,
        'missing_cases': missing_cases,
        'criminal_cases': criminal_cases,
        'resolution_rate': round(resolution_rate, 2),
        'avg_resolution_time': round(avg_resolution_time, 2),
        'monthly_cases': monthly_cases,
        'monthly_resolved': monthly_resolved,
        'detection_success_rate': round(detection_success_rate, 2),
        'total_users': total_users,
        'active_users': active_users,
        'daily_cases': list(daily_cases),
    }
    
    return render(request, 'admin_templates/performance_metrics.html', context)


def export_metrics_csv(request):
    import csv
    from django.http import HttpResponse
    
    if 'admin_user_id' not in request.session:
        return redirect('admin-login')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="performance_metrics.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Metric', 'Value'])
    
    total_cases = Case.objects.count()
    pending_cases = Case.objects.filter(status='Pending').count()
    resolved_cases = Case.objects.filter(Q(status='Found') | Q(status='Arrested')).count()
    resolution_rate = (resolved_cases / total_cases * 100) if total_cases > 0 else 0
    
    writer.writerow(['Total Cases', total_cases])
    writer.writerow(['Pending Cases', pending_cases])
    writer.writerow(['Resolved Cases', resolved_cases])
    writer.writerow(['Resolution Rate (%)', round(resolution_rate, 2)])
    writer.writerow(['Missing Cases', Case.objects.filter(case_type='Missing').count()])
    writer.writerow(['Criminal Cases', Case.objects.filter(case_type='Criminal').count()])
    
    return response
