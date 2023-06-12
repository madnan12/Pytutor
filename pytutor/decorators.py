from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			role = None
			if request.user.user_type:
				role = request.user.user_type

			else:
				raise PermissionDenied()

			if role in allowed_roles:
				return view_func(request, *args, **kwargs)
			
			else:
				raise PermissionDenied()
				
		return wrapper_func
	return decorator