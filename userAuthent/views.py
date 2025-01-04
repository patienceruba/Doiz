from django.utils import timezone
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test,login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.dispatch import receiver
from django.db.models.signals import post_save


def login_view(request):
    user = None  # Initialize user variable

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Or any other page after login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Stay on the login page

    return render(request, 'todo/login.html')



def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('f-name')
        last_name = request.POST.get('l-name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')
        profile_picture = request.FILES.get('profile_picture')  # Handling the image upload

        if password != password1:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # Create UserProfile instance
        user_profile = UserProfile(user=user, profile_picture=profile_picture)
        user_profile.save()

        messages.success(request, "Registration successful! You can now log in.")
        return redirect('login')
    
    return render(request, 'todo/register.html')


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')



# Request password reset


# Password Reset Request
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            subject = "Password Reset Request"
            context = {
                "email": user.email,
                "domain": request.get_host(),
                "protocol": "http",
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            }
            email_content = render_to_string("todo/password_reset_email.html", context)
            email_message = EmailMessage(
                subject=subject,
                body=email_content,
                from_email="admin@example.com",
                to=[user.email],
            )
            email_message.content_subtype = "html"
            email_message.send()
        messages.success(request, "If an account exists with the provided email, a reset link has been sent.")
        return redirect("password_reset_done")
    return render(request, "todo/password_reset_request.html")


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            password = request.POST.get("password")
            password1 = request.POST.get("password1")
            if password == password1:
                user.set_password(password)
                user.save()
                messages.success(request, "Your password has been reset successfully.")
                return redirect("login")
            else:
                messages.error(request, "Passwords do not match.")
        return render(request, "todo/password_reset_confirm.html")
    else:
        messages.error(request, "The reset link is invalid or has expired.")
        return redirect("password_reset_request")

def password_reset_done(request):
    return render(request, "todo/password_reset_done.html")



