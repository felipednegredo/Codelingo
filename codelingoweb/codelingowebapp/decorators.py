from django.core.exceptions import PermissionDenied

def aluno_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_student:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

def professor_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_teacher:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func