from functools import wraps

from rest_framework.response import Response
from rest_framework import status


def role_required(allowed_roles):
    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if request.user.role not in allowed_roles:
                return Response(
                    {
                        "error": "You do not have permission to perform this action."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator