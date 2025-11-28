def user_context(request):
    """
    Context processor để thêm thông tin user vào tất cả templates
    
    Sử dụng trong template:
    {{ current_user.name }}
    {{ current_user.email }}
    {{ current_user.is_admin }}
    {{ current_user.is_authenticated }}
    """
    
    user_id = request.session.get('user_id')
    
    if user_id:
        return {
            'current_user': {
                'id': user_id,
                'name': request.session.get('user_name', ''),
                'email': request.session.get('user_email', ''),
                'role': request.session.get('user_role', 'user'),
                'is_admin': request.session.get('user_role') == 'admin',
                'is_authenticated': True,
            }
        }
    
    return {
        'current_user': {
            'is_authenticated': False,
        }
    }