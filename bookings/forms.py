from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking
from tours.models import Tour
from hotels.models import Hotel
from flight.models import Flight


class BookingSearchForm(forms.Form):
    """
    Form tìm kiếm và gợi ý booking
    Người dùng nhập: nơi muốn đi, ngày khởi hành, chi phí dự kiến
    """

    destination = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'destination',
            'placeholder': 'Ví dụ: Paris, Tokyo, Bali...'
        }),
        label='Nơi Muốn Đến',
        required=True
    )

    departure_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'id': 'departure_date',
            'type': 'date'
        }),
        label='Ngày Khởi Hành',
        required=True
    )

    number_of_people = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'number_of_people',
            'placeholder': 'Số người (1-10)'
        }),
        label='Số Người',
        required=True
    )

    expected_total_cost = forms.DecimalField(
        min_value=0,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'expected_total_cost',
            'placeholder': 'Chi phí dự kiến (VND)',
            'step': '100000'
        }),
        label='Chi Phí Tổng Dự Kiến (VND)',
        required=True
    )

    def clean_departure_date(self):
        departure_date = self.cleaned_data.get('departure_date')
        today = timezone.now().date()
        if departure_date < today:
            raise ValidationError('Ngày khởi hành phải là hôm nay hoặc tương lai')
        return departure_date

    def clean(self):
        cleaned_data = super().clean()
        number_of_people = cleaned_data.get('number_of_people')
        expected_total_cost = cleaned_data.get('expected_total_cost')

        if number_of_people and number_of_people < 1:
            raise ValidationError('Số người phải lớn hơn 0')

        if expected_total_cost and expected_total_cost < 0:
            raise ValidationError('Chi phí không thể âm')

        return cleaned_data


class BookingConfirmForm(forms.ModelForm):
    """
    Form xác nhận booking sau khi chọn vé máy bay và khách sạn
    """
    
    class Meta:
        model = Booking
        fields = ['number_of_people']
        widgets = {
            'number_of_people': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '10'
            })
        }
        labels = {
            'number_of_people': 'Số Người'
        }
    
    # Thêm các trường cho vé máy bay và khách sạn
    flight_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False
    )
    
    hotel_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False
    )
    
    tour_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False
    )
    
    def clean(self):
        cleaned_data = super().clean()
        number_of_people = cleaned_data.get('number_of_people')

        if number_of_people and number_of_people < 1:
            raise ValidationError('Số người phải lớn hơn 0')

        return cleaned_data


class ContactBookingForm(forms.Form):
    """
    Form liên hệ đặt tour sau khi chọn gói
    """

    full_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'full_name',
            'placeholder': 'Họ và tên đầy đủ'
        }),
        label='Họ và Tên',
        required=True
    )

    birth_year = forms.IntegerField(
        min_value=1900,
        max_value=timezone.now().year,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'birth_year',
            'placeholder': f'Năm sinh (1900-{timezone.now().year})'
        }),
        label='Năm Sinh',
        required=True
    )

    passport_number = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'passport_number',
            'placeholder': 'Số hộ chiếu (nếu đi nước ngoài)'
        }),
        label='Số Hộ Chiếu',
        help_text='Chỉ bắt buộc nếu đi nước ngoài'
    )

    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'phone_number',
            'placeholder': 'Số điện thoại'
        }),
        label='Số Điện Thoại',
        required=True
    )

    bank_account = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'bank_account',
            'placeholder': 'Số tài khoản ngân hàng'
        }),
        label='Số Tài Khoản Ngân Hàng',
        required=True
    )

    number_of_people = forms.IntegerField(
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'number_of_people',
            'placeholder': 'Số người (1-10)'
        }),
        label='Số Người Đi',
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.is_international = kwargs.pop('is_international', False)
        super().__init__(*args, **kwargs)
        if self.is_international:
            self.fields['passport_number'].required = True
        else:
            self.fields['passport_number'].required = False

    def clean_passport_number(self):
        passport_number = self.cleaned_data.get('passport_number')
        if self.is_international and not passport_number:
            raise ValidationError('Số hộ chiếu là bắt buộc cho chuyến đi quốc tế')
        return passport_number

    def clean(self):
        cleaned_data = super().clean()
        number_of_people = cleaned_data.get('number_of_people')

        if number_of_people and number_of_people < 1:
            raise ValidationError('Số người phải lớn hơn 0')

        return cleaned_data
