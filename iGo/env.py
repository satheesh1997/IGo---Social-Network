from django.contrib.auth.models import User

users = User.objects.all()

content = {
    'title': 'i Go',
    'site_name': 'Network',
    'description': '',
    'first_site_name': 'i',
    'last_site_name': 'Go',
    'url': 'http://jokertest.pythonanywhere.com',
    'tag_line': 'Go a step ahead',
    'color': 'orangered',
    'users_list': users
}
