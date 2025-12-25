#!/usr/bin/env python
"""
Script tự động cập nhật tất cả template
Thay thế các liên kết hardcoded bằng Django URL tags
"""

import os
import re
from pathlib import Path

# Danh sách các thay thế
REPLACEMENTS = [
    # Logout button
    (r'href=["\']starter-page\.html["\']', 'href="{% url \'users:logout\' %}"'),
    
    # Login button
    (r'href=["\']log-in\.html["\']', 'href="{% url \'users:login\' %}"'),
    (r'href=["\']login\.html["\']', 'href="{% url \'users:login\' %}"'),
    
    # Register button
    (r'href=["\']register\.html["\']', 'href="{% url \'users:register\' %}"'),
    
    # Booking
    (r'href=["\']booking\.html["\']', 'href="{% url \'bookings:booking_list\' %}"'),
    
    # Tours
    (r'href=["\']tours\.html["\']', 'href="{% url \'tours:tour_list\' %}"'),
    (r'href=["\']tour-details\.html["\']', 'href="{% url \'tours:tour_list\' %}"'),
    
    # Destinations
    (r'href=["\']destinations\.html["\']', 'href="{% url \'core:destinations\' %}"'),
    (r'href=["\']destination-details\.html["\']', 'href="{% url \'core:destinations\' %}"'),
    
    # Blog
    (r'href=["\']blog\.html["\']', 'href="{% url \'core:blog\' %}"'),
    (r'href=["\']blog-details\.html["\']', 'href="{% url \'core:blog\' %}"'),
    
    # Flight
    (r'href=["\']flight\.html["\']', 'href="{% url \'flight:flight_list\' %}"'),
    (r'href=["\']flight-details\.html["\']', 'href="{% url \'flight:flight_list\' %}"'),
    
    # Other pages
    (r'href=["\']index\.html["\']', 'href="{% url \'core:home\' %}"'),
    (r'href=["\']about\.html["\']', 'href="{% url \'core:about\' %}"'),
    (r'href=["\']contact\.html["\']', 'href="{% url \'core:contact\' %}"'),
    (r'href=["\']gallery\.html["\']', 'href="{% url \'core:gallery\' %}"'),
    (r'href=["\']testimonials\.html["\']', 'href="{% url \'core:testimonials\' %}"'),
    (r'href=["\']faq\.html["\']', 'href="{% url \'core:faq\' %}"'),
    (r'href=["\']terms\.html["\']', 'href="{% url \'core:terms\' %}"'),
    (r'href=["\']privacy\.html["\']', 'href="{% url \'core:privacy\' %}"'),
    (r'href=["\']chatbot\.html["\']', 'href="{% url \'chatbot:chatbot\' %}"'),
    (r'href=["\']forgot-password\.html["\']', 'href="{% url \'users:forget\' %}"'),
]

def update_template(file_path):
    """Cập nhật một template file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Áp dụng tất cả các thay thế
        for pattern, replacement in REPLACEMENTS:
            content = re.sub(pattern, replacement, content)
        
        # Nếu có thay đổi, lưu file
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Lỗi khi cập nhật {file_path}: {e}")
        return False

def main():
    """Cập nhật tất cả template"""
    templates_dir = Path(__file__).parent.parent / 'templates'
    
    if not templates_dir.exists():
        print(f"Thư mục templates không tồn tại: {templates_dir}")
        return
    
    # Danh sách template cần cập nhật
    templates_to_update = [
        'index.html',
        'about.html',
        'contact.html',
        'gallery.html',
        'tours.html',
        'tour-details.html',
        'booking.html',
        'destinations.html',
        'destination-details.html',
        'blog.html',
        'blog-details.html',
        'testimonials.html',
        'faq.html',
        'terms.html',
        'privacy.html',
        'flight.html',
        'flight-details.html',
        'chatbot.html',
        'log-in.html',
        'register.html',
        'forgot-password.html',
        'starter-page.html',
        'admin-dashboard.html',
        'admin-tour.html',
        'admin-booking.html',
        'admin-blog.html',
        'admin-user.html',
        'admin-setting.html',
        '404.html',
    ]
    
    updated_count = 0
    failed_count = 0
    
    print("=" * 60)
    print("Cập nhật Template")
    print("=" * 60)
    
    for template_name in templates_to_update:
        template_path = templates_dir / template_name
        
        if template_path.exists():
            if update_template(template_path):
                print(f"✅ {template_name} - Cập nhật thành công")
                updated_count += 1
            else:
                print(f"⏭️  {template_name} - Không có thay đổi")
        else:
            print(f"❌ {template_name} - Không tìm thấy")
            failed_count += 1
    
    print("=" * 60)
    print(f"Tóm tắt:")
    print(f"  ✅ Cập nhật: {updated_count}")
    print(f"  ❌ Không tìm thấy: {failed_count}")
    print(f"  ⏭️  Không có thay đổi: {len(templates_to_update) - updated_count - failed_count}")
    print("=" * 60)

if __name__ == '__main__':
    main()
