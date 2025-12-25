import requests
from bs4 import BeautifulSoup

BASE = 'http://127.0.0.1:8000'

s = requests.Session()

# 1) Get CSRF token from login page
r = s.get(BASE + '/users/login/')
if r.status_code != 200:
    print('Login page not reachable', r.status_code)
    exit(1)

soup = BeautifulSoup(r.text, 'html.parser')
csrf = None
el = soup.find('input', attrs={'name':'csrfmiddlewaretoken'})
if el:
    csrf = el.get('value')

# 2) Login
login_data = {
    'email': 'user@travel.com',
    'password': 'user123',
}
if csrf:
    login_data['csrfmiddlewaretoken'] = csrf

r = s.post(BASE + '/users/login/', data=login_data, allow_redirects=True)
print('Login status', r.status_code, '->', r.url)

# Check auth by fetching profile
rp = s.get(BASE + '/users/profile/')
print('Profile fetch:', rp.status_code, 'url:', rp.url)
if 'Logout' in rp.text or 'Đăng xuất' in rp.text or rp.status_code == 200:
    print('Likely logged in')
else:
    print('Not logged in; profile page content length', len(rp.text))

# 3) Create preview (assumes there's a tour with id 1)
# First fetch a page to get CSRF
r = s.get(BASE + '/')
soup = BeautifulSoup(r.text, 'html.parser')
el = soup.find('input', attrs={'name':'csrfmiddlewaretoken'})
if el:
    csrf = el.get('value')

create_data = {
    'tour_id': '1009',
    'package_id': '',
    'number_of_people': '1',
    'name': 'Test User',
    'email': 'user@travel.com',
}
if csrf:
    create_data['csrfmiddlewaretoken'] = csrf

r = s.post(BASE + '/bookings/create-ticket-from-tour/', data=create_data, allow_redirects=True)
print('Create preview status', r.status_code)
print('Create preview response snippet:\n', r.text[:500])

# 4) Submit payment POST for preview
# Fetch payment page first to get CSRF
r = s.get(BASE + '/bookings/payment/preview/')
soup = BeautifulSoup(r.text, 'html.parser')
el = soup.find('input', attrs={'name':'csrfmiddlewaretoken'})
if el:
    csrf = el.get('value')

pay_data = {
    'payment_method': 'banking'
}
if csrf:
    pay_data['csrfmiddlewaretoken'] = csrf

r = s.post(BASE + '/bookings/payment/preview/', data=pay_data, allow_redirects=True)
print('Payment POST status', r.status_code)
print('Payment response snippet:\n', r.text[:500])
with open('scripts/payment_response.html', 'w', encoding='utf-8') as f:
    f.write(r.text)

# 5) Fetch preview ticket page and save HTML
r = s.get(BASE + '/bookings/ticket/preview/')
with open('scripts/preview_result.html', 'w', encoding='utf-8') as f:
    f.write(r.text)

if 'Đã thanh toán' in r.text:
    print('Preview shows paid status')
else:
    print('Preview does NOT show paid status')

print('Saved HTML to scripts/preview_result.html')
