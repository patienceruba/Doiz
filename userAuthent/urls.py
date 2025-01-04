from django.urls import path
from . import views
from .views import password_reset_request, password_reset_confirm
from django.contrib.auth import views as auth_views  # Import built-in views



urlpatterns = [
	path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path("password-reset/", views.password_reset_request, name="password_reset_request"),
    path("password-reset/done/", views.password_reset_done, name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", views.password_reset_confirm, name="password_reset_confirm"),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  # Add this line

]