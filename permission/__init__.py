def monkey_patch_user():
    from django.contrib.auth import get_user_model
    from permission.utils import get_anonymous_user, evict_object_perms_cache
    from permission.utils import get_user_object_perms_model
    UserObjectPermission = get_user_object_perms_model()
    User = get_user_model()
    setattr(User, 'get_anonymous', staticmethod(lambda: get_anonymous_user()))
    setattr(User, 'add_obj_perm', lambda self, perm, obj: UserObjectPermission.objects.assign_perm(perm, self, obj))
    setattr(User, 'del_obj_perm', lambda self, perm, obj: UserObjectPermission.objects.remove_perm(perm, self, obj))
    setattr(User, 'evict_obj_perms_cache', evict_object_perms_cache)


def monkey_patch_group():
    from django.contrib.auth.models import Group
    from permission.utils import get_group_object_perms_model
    GroupObjectPermission = get_group_object_perms_model()
    setattr(Group, 'add_obj_perm', lambda self, perm, obj: GroupObjectPermission.objects.assign_perm(perm, self, obj))
    setattr(Group, 'del_obj_perm', lambda self, perm, obj: GroupObjectPermission.objects.remove_perm(perm, self, obj))
