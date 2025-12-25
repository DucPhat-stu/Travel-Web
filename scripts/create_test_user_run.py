from django.contrib.auth import get_user_model
User = get_user_model()
u = User.objects.filter(email='user@travel.com').first()
if u:
    print('EXISTS')
else:
    User.objects.create_user(email='user@travel.com', password='user123', full_name='Test User', phone='0987654321', address='User Address', role='user')
    print('CREATED')
