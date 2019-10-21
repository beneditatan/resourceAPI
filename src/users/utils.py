from django.contrib.auth.models import Group, User

def is_member_of(username, group):
    user = User.objects.get(username=username)
    group = Group.objects.get(name=group)
    members = group.user_set.all()
    
    if user in members:
        return True
    else:
        return False