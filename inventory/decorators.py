from django.shortcuts import redirect


def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('/shop/')

        return wrapper_func

    return decorator
