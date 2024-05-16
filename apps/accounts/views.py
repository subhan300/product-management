from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth import authenticate, login, get_user_model, update_session_auth_hash, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.maintenance.models import Image

CustomUser = get_user_model()

class UserLoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET.get("next", "dashboard"))

        error_message = 'Invalid username or password. Please try again.'
        messages.error(request, error_message)
        return render(request, self.template_name)

class ForgotPasswordView(View):
    template_name = "accounts/forget-password.html"

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        form = PasswordResetForm(request.POST)

        if form.is_valid():
            messages.success(request, 'Password reset link sent to your email.')
            return redirect('forgot_password')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)

        return render(request, self.template_name)

class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request, key=None):
        if key == "pw":
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password has been successfully changed.')
            else:
                for field, errors in password_form.errors.items():
                    for error in errors:
                        messages.error(request, error)

        if key == "pf":
            user = CustomUser.objects.get(id=request.user.id)
            user_data = {
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'phone': request.POST.get('phone'),
                'username': request.POST.get('username'),
                'bio': request.POST.get('bio'),
            }
            # user.email = request.POST.get('email')  # Uncomment if you intend to update the email
            for key, value in user_data.items():
                setattr(user, key, value)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your profile has been successfully changed.')

        if key == "pf_image":
            request.user.profile_image = Image.objects.create(image=request.FILES.get('profile_image'), company=request.user.company)
            request.user.save()

        return redirect("profile")

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('login')
