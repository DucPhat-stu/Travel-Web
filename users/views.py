from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .forms import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm, ProfileEditForm, UserPostForm
from .models import User, UserPost
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
                
                # Tự động đăng nhập sau khi đăng ký thành công
                SessionService.create_session(request, user)
                
                # Trigger signal
                user_logged_in.send(sender=user.__class__, user=user, request=request)
                
                messages.success(request, f'Đăng ký thành công! Chào mừng {user.full_name}!')
                return redirect('core:home')
                
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
    
    return render(request, 'register.html', {'form': form})


@csrf_protect
@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    U02: Đăng nhập
    POST /users/login
    """
    # Nếu đã đăng nhập rồi thì redirect
    if SessionService.is_authenticated(request):
        # Kiểm tra tham số next để redirect về URL ban đầu
        next_url = request.GET.get('next') or request.POST.get('next')
        # Tránh redirect loop: không redirect về login page hoặc về chính nó
        if next_url and '/users/login' not in next_url and next_url != request.path:
            # Kiểm tra xem next_url có hợp lệ không (không phải là login)
            try:
                return redirect(next_url)
            except:
                pass  # Nếu redirect fail, tiếp tục logic bên dưới
        
        # Nếu không có next hoặc next không hợp lệ, redirect theo role
        if SessionService.is_admin(request):
            return redirect('admin_panel:dashboard')
        return redirect('core:home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            admin_confirm = request.POST.get('admin_confirm') == 'on'
            
            # Sử dụng UserService để authenticate
            user = UserService.authenticate_user(email, password)
            
            if user:
                # Tạo session
                SessionService.create_session(request, user)
                
                # Debug: In ra session để kiểm tra
                print(f"DEBUG - Session created for user: {user.email}")
                print(f"DEBUG - Session data: user_id={request.session.get('user_id')}, user_role={request.session.get('user_role')}")
                
                # Trigger signal
                user_logged_in.send(sender=user.__class__, user=user, request=request)
                
                # Kiểm tra tham số next để redirect về URL ban đầu
                next_url = request.GET.get('next') or request.POST.get('next')
                
                # Tránh redirect loop: kiểm tra kỹ next_url
                if next_url:
                    # Loại bỏ các URL không hợp lệ
                    invalid_urls = ['/users/login', '/accounts/login', request.path]
                    if not any(invalid in next_url for invalid in invalid_urls):
                        # Redirect theo role hoặc next URL
                        if user.is_admin():
                            messages.success(request, f'Đăng nhập thành công! Chào mừng Admin {user.full_name}!')
                            try:
                                return redirect(next_url)
                            except:
                                pass  # Nếu redirect fail, tiếp tục
                        else:
                            messages.success(request, f'Đăng nhập thành công! Chào mừng {user.full_name}!')
                            try:
                                return redirect(next_url)
                            except:
                                pass  # Nếu redirect fail, tiếp tục
                
                # Nếu không có next hoặc next không hợp lệ, redirect theo role
                if user.is_admin():
                    messages.success(request, f'Đăng nhập thành công! Chào mừng Admin {user.full_name}!')
                    return redirect('admin_panel:dashboard')
                else:
                    messages.success(request, f'Đăng nhập thành công! Chào mừng {user.full_name}!')
                    return redirect('core:home')
            else:
                messages.error(request, 'Email hoặc mật khẩu không đúng!')
        else:
            messages.error(request, 'Vui lòng nhập đầy đủ thông tin!')
    else:
        form = LoginForm()
    
    return render(request, 'log-in.html', {'form': form})


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


# =========================
# PROFILE VIEWS
# =========================

@require_http_methods(["GET"])
def profile_view(request, user_id=None):
    """
    Xem profile của user
    GET /users/profile/ hoặc /users/profile/<user_id>/
    """
    # Nếu không có user_id, xem profile của chính mình
    if user_id is None:
        if not SessionService.is_authenticated(request):
            messages.error(request, 'Vui lòng đăng nhập để xem profile!')
            return redirect('users:login')
        user = SessionService.get_current_user(request)
    else:
        user = get_object_or_404(User, user_id=user_id)
    
    # Lấy các bài đăng của user
    posts = UserPost.objects.filter(user=user).order_by('-created_at')
    
    # Kiểm tra xem có phải profile của mình không
    is_own_profile = False
    if SessionService.is_authenticated(request):
        current_user = SessionService.get_current_user(request)
        is_own_profile = current_user and current_user.user_id == user.user_id
    
    context = {
        'profile_user': user,
        'posts': posts,
        'is_own_profile': is_own_profile,
        'posts_count': posts.count(),
    }
    
    return render(request, 'users/profile.html', context)


from .forms import RegisterForm, LoginForm, ForgetPasswordForm, ResetPasswordForm, ProfileEditForm, UserPostForm, ChangePasswordForm
@csrf_protect
@require_http_methods(["GET", "POST"])
def edit_profile_view(request):
    """
    Chỉnh sửa profile, đổi mật khẩu và đăng bài
    GET/POST /users/profile/edit/
    """
    if not SessionService.is_authenticated(request):
        messages.error(request, 'Vui lòng đăng nhập!')
        return redirect('users:login')

    user = SessionService.get_current_user(request)
    
    # Khởi tạo các form
    profile_form = ProfileEditForm(instance=user)
    password_form = ChangePasswordForm()
    post_form = UserPostForm()

    if request.method == 'POST':
        # Xác định form nào được submit
        form_type = request.POST.get('form_type')

        if form_type == 'profile':
            profile_form = ProfileEditForm(request.POST, request.FILES, instance=user)
            if profile_form.is_valid():
                try:
                    profile_form.save()
                    SessionService.create_session(request, user)  # Cập nhật session
                    messages.success(request, 'Cập nhật profile thành công!')
                    return redirect('users:edit_profile')
                except Exception as e:
                    messages.error(request, f'Lỗi: {str(e)}')

        elif form_type == 'password':
            password_form = ChangePasswordForm(request.POST)
            if password_form.is_valid():
                old_password = password_form.cleaned_data['old_password']
                new_password = password_form.cleaned_data['new_password']
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    user_password_changed.send(sender=user.__class__, user=user)
                    messages.success(request, 'Đổi mật khẩu thành công! Vui lòng đăng nhập lại.')
                    return redirect('users:login')
                else:
                    messages.error(request, 'Mật khẩu cũ không đúng!')
        
        elif form_type == 'post':
            post_form = UserPostForm(request.POST, request.FILES)
            if post_form.is_valid():
                try:
                    post = post_form.save(commit=False)
                    post.user = user
                    post.save()
                    messages.success(request, 'Đăng bài thành công!')
                    return redirect('users:edit_profile')
                except Exception as e:
                    messages.error(request, f'Lỗi: {str(e)}')

    # GET request hoặc nếu form không valid
    posts = UserPost.objects.filter(user=user).order_by('-created_at')
    context = {
        'profile_form': profile_form,
        'password_form': password_form,
        'post_form': post_form,
        'user': user,
        'posts': posts,
    }
    return render(request, 'users/edit_profile.html', context)



@csrf_protect
@require_http_methods(["GET", "POST"])
def create_post_view(request):
    """
    Tạo bài đăng mới
    GET/POST /users/post/create/
    """
    if not SessionService.is_authenticated(request):
        messages.error(request, 'Vui lòng đăng nhập!')
        return redirect('users:login')
    
    user = SessionService.get_current_user(request)
    
    if request.method == 'POST':
        form = UserPostForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.user = user
                post.save()
                
                messages.success(request, 'Đăng bài thành công!')
                return redirect('users:profile')
                
            except Exception as e:
                messages.error(request, f'Lỗi: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = UserPostForm()
    
    return render(request, 'users/create_post.html', {'form': form})


@require_http_methods(["POST"])
def delete_post_view(request, post_id):
    """
    Xóa bài đăng
    POST /users/post/<post_id>/delete/
    """
    if not SessionService.is_authenticated(request):
        messages.error(request, 'Vui lòng đăng nhập!')
        return redirect('users:login')
    
    user = SessionService.get_current_user(request)
    post = get_object_or_404(UserPost, post_id=post_id)
    
    # Chỉ cho phép xóa bài của chính mình
    if post.user.user_id != user.user_id:
        messages.error(request, 'Bạn không có quyền xóa bài này!')
        return redirect('users:profile')
    
    post.delete()
    messages.success(request, 'Đã xóa bài đăng!')
    return redirect('users:profile')


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
    
    return render(request, 'forgot-password.html', {'form': form})


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
    
    return render(request, 'forgot-password.html', {
        'form': form,
        'token': token,
        'email': email
    })