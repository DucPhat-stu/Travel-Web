from django import forms
from .models import User, UserPost
import re
from captcha.fields import CaptchaField

class RegisterForm(forms.Form):
    """Form đăng ký tài khoản"""
    
    full_name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập họ tên đầy đủ'
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'email@example.com'
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '0xxxxxxxxx'
        })
    )
    
    password = forms.CharField(
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mật khẩu (tối thiểu 8 ký tự)'
        })
    )
    
    confirm_password = forms.CharField(
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập lại mật khẩu'
        })
    )
    
    address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Địa chỉ (không bắt buộc)'
        })
    )
    
    def clean_email(self):
        """Kiểm tra email đã tồn tại chưa"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email đã được sử dụng!')
        return email
    
    def clean_phone(self):
        """Kiểm tra định dạng số điện thoại"""
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^(0|\+84)[0-9]{9,10}$', phone):
            raise forms.ValidationError('Số điện thoại không hợp lệ!')
        return phone
    
    def clean(self):
        """Kiểm tra password và confirm_password khớp nhau"""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError('Mật khẩu không khớp!')
        
        return cleaned_data


class LoginForm(forms.Form):
    """Form đăng nhập"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mật khẩu'
        })
    )


class ForgetPasswordForm(forms.Form):
    """Form quên mật khẩu - gửi link reset"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập email đã đăng ký'
        })
    )
    
    def clean_email(self):
        """Kiểm tra email có tồn tại không"""
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email không tồn tại trong hệ thống!')
        return email


class ResetPasswordForm(forms.Form):
    """Form reset mật khẩu mới"""
    
    new_password = forms.CharField(
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mật khẩu mới (tối thiểu 8 ký tự)'
        })
    )
    
    confirm_password = forms.CharField(
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Xác nhận mật khẩu mới'
        })
    )
    
    def clean(self):
        """Kiểm tra password và confirm_password khớp nhau"""
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError('Mật khẩu không khớp!')
        
        return cleaned_data


class ProfileEditForm(forms.ModelForm):
    """Form chỉnh sửa profile"""
    
    class Meta:
        model = User
        fields = ['full_name', 'phone', 'address', 'bio', 'date_of_birth', 'gender', 'avatar']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Họ tên đầy đủ'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0xxxxxxxxx'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Địa chỉ'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Giới thiệu về bản thân...',
                'rows': 3
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[('', 'Chọn giới tính'), ('Nam', 'Nam'), ('Nữ', 'Nữ'), ('Khác', 'Khác')]),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
    
    def clean_phone(self):
        """Kiểm tra định dạng số điện thoại"""
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^(0|\+84)[0-9]{9,10}$', phone):
            raise forms.ValidationError('Số điện thoại không hợp lệ!')
        return phone


from captcha.fields import CaptchaField


class ChangePasswordForm(forms.Form):
    """Form thay đổi mật khẩu"""

    old_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật khẩu cũ'})
    )
    new_password = forms.CharField(
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mật khẩu mới (tối thiểu 8 ký tự)'})
    )
    confirm_password = forms.CharField(
        min_length=8,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Xác nhận mật khẩu mới'})
    )
    captcha = CaptchaField(help_text="Nhập các ký tự trong ảnh")

    def clean(self):
        """Kiểm tra password và confirm_password khớp nhau"""
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise forms.ValidationError('Mật khẩu không khớp!')

        return cleaned_data


class UserPostForm(forms.ModelForm):
    """Form đăng bài/hình ảnh trải nghiệm"""
    
    class Meta:
        model = UserPost
        fields = ['image', 'caption', 'location', 'rating', 'comment']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'required': True
            }),
            'caption': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Chia sẻ trải nghiệm của bạn...',
                'rows': 3
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Địa điểm (vd: Đà Lạt, Việt Nam)'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-control'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Bình luận của bạn...',
                'rows': 2
            })
        }