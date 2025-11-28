from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .forms import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm
from .services import (
    UserService, 
    PasswordResetService, 
    EmailService,
    SessionService
)
from .signals import user_logged_in, user_logged_out, user_password_changed

# =========================
# AUTHENTICATION VIEWS
# =========================

@csrf_protect
@require_http_methods(["GET", "POST"])
def register_view(request):
    """
    U01: Đăng ký tài khoản
    POST /users/register
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            try:
                # Sử dụng UserService để tạo user
                user = UserService.create_user(
                    full_name=form.cleaned_data['full_name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    password=form.cleaned_data['password'],
                    address=form.cleaned_data.get('address', ''),
                    role='user'
                )
                
                messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
                return redirect('users:login')
                
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f'Lỗi: {str(e)}')
        else:
            # Hiển thị lỗi validation
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})


@csrf_protect
@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    U02: Đăng nhập
    POST /users/login
    """
    # Nếu đã đăng nhập rồi thì redirect
    if SessionService.is_authenticated(request):
        if SessionService.is_admin(request):
            return redirect('admin_panel:dashboard')
        return redirect('core:home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Sử dụng UserService để authenticate
            user = UserService.authenticate_user(email, password)
            
            if user:
                # Tạo session
                SessionService.create_session(request, user)
                
                # Trigger signal
                user_logged_in.send(sender=user.__class__, user=user, request=request)
                
                messages.success(request, f'Chào mừng {user.full_name}!')
                
                # Redirect theo role
                if user.is_admin():
                    return redirect('admin_panel:dashboard')
                else:
                    return redirect('core:home')
            else:
                messages.error(request, 'Email hoặc mật khẩu không đúng!')
        else:
            messages.error(request, 'Vui lòng nhập đầy đủ thông tin!')
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})


@require_http_methods(["GET", "POST"])
def logout_view(request):
    """
    U03: Đăng xuất
    POST /users/logout
    """
    # Lấy user trước khi xóa session
    user = SessionService.get_current_user(request)
    
    # Xóa session
    SessionService.clear_session(request)
    
    # Trigger signal
    if user:
        user_logged_out.send(sender=user.__class__, user=user)
    
    messages.success(request, 'Đã đăng xuất thành công!')
    return redirect('users:login')


@csrf_protect
@require_http_methods(["GET", "POST"])
def forget_password_view(request):
    """
    U04: Quên mật khẩu - gửi link reset
    POST /users/forget
    """
    if request.method == 'POST':
        form = ForgetPasswordForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Sử dụng PasswordResetService
            success, token = PasswordResetService.request_password_reset(email)
            
            if success:
                user = UserService.get_user_by_email(email)
                
                # Tạo link reset
                reset_link = request.build_absolute_uri(
                    f'/users/reset/?token={token}&email={email}'
                )
                
                # Gửi email
                email_sent = EmailService.send_password_reset_email(user, reset_link)
                
                if email_sent:
                    messages.success(
                        request, 
                        'Đã gửi link khôi phục mật khẩu đến email của bạn!'
                    )
                else:
                    # Development mode: in ra console
                    print(f"\n{'='*50}")
                    print(f"RESET PASSWORD LINK:")
                    print(f"{reset_link}")
                    print(f"{'='*50}\n")
                    messages.info(
                        request,
                        'Link khôi phục đã được tạo. Kiểm tra console (demo mode).'
                    )
                
                return redirect('users:login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = ForgetPasswordForm()
    
    return render(request, 'users/forget_password.html', {'form': form})


@csrf_protect
@require_http_methods(["GET", "POST"])
def reset_password_view(request):
    """
    U04: Đặt lại mật khẩu
    POST /users/reset
    """
    token = request.GET.get('token')
    email = request.GET.get('email')
    
    if not token or not email:
        messages.error(request, 'Link không hợp lệ!')
        return redirect('users:forget')
    
    # Verify token
    user = PasswordResetService.verify_reset_token(email, token)
    
    if not user:
        messages.error(request, 'Link đã hết hạn hoặc không hợp lệ!')
        return redirect('users:forget')
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        
        if form.is_valid():
            # Reset password
            PasswordResetService.reset_password(
                user, 
                form.cleaned_data['new_password']
            )
            
            # Trigger signal
            user_password_changed.send(sender=user.__class__, user=user)
            
            messages.success(request, 'Đặt lại mật khẩu thành công! Vui lòng đăng nhập.')
            return redirect('users:login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = ResetPasswordForm()
    
    return render(request, 'users/reset_password.html', {
        'form': form,
        'token': token,
        'email': email
    })