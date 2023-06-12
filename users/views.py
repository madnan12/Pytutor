from django.shortcuts import render, redirect, reverse
from django.contrib.auth.views import LoginView
from django.views.generic import View
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .forms import CreateUserForm, UserUpdateForm
from .tokens import account_activation_token
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from .models import CustomUser
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator

class LoginView(LoginView):
	template_name = 'login.html'

	def get_context_data(self, **kwargs):                                               # used to send additional context
		context = super().get_context_data(**kwargs)
		context["title"] = 'Login'
		return context

	def get_success_url(self):
		# Getting next url for redirect
		redirect_to = self.request.GET.get('next')
		if self.request.user.user_type == 'Administration':
			return reverse('administration:administration-dashboard')

		elif self.request.user.user_type == 'Teacher':
			return reverse('teachers_portal:teachers-dashboard')

		elif self.request.user.user_type == 'Student':
			return reverse('students_portal:students-dashboard')

		else:
			raise PermissionDenied()

		# Redirecting user
		return redirect_to or reverse('core:homepage')

class RegistrationView(View):
	template_name = 'register.html'

	def get(self, request):
		form = CreateUserForm()
		context = {
			'title'	: 'Registration',
			'form'	: form,
		}
		return render(request, 'register.html', context)

	def post(self, request):
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			current_site = get_current_site(request)
			subject = 'Activate Your PyTutor-OM Account'
			message = render_to_string('extra_templates/account_activation_email.html', {
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token': account_activation_token.make_token(user),
				}
			)
			# user.email_user(subject, message)
			send_mail(
                subject,  # Subject of message
                message,  # Message
                '',  # From Email
                [user.email],  # To Email

                fail_silently=True
            )
			messages.success(request, f"Account created successfuly")
			return redirect('users:activate-email-sent')

		else:
			messages.error(request, f"Please make sure all fields are filled")
			context = {
				'title'	: 'Registration',
				'form'	: form,
			}
			return render(request, 'register.html', context)

def AccuntActivationSent(request):
	context = {
		'title'	: 'Account Created Successfuly',
		'valid'	: True,
	}
	return render(request, 'extra_templates/account_validation.html', context)

class ActivateAccount(View):
	
	def get(self, request, uidb64, token):
		try:
			uid = force_str(urlsafe_base64_decode(uidb64))
			user = CustomUser.objects.get(pk=uid)
		except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
			user = None

		if user is not None and account_activation_token.check_token(user, token):
			user.is_active = True
			user.save()
			login(request, user)
			messages.success(request, f"Account activate successfuly")
			# Redirecting user to their dashboard based on user type
			if user.user_type == 'Teacher':
				return redirect('teachers_portal:teachers-dashboard')

			elif user.user_type == 'Student':
				return redirect('students_portal:students-dashboard')
			
			else:
				return redirect('core:homepage')

		else:
			context = {
				'title'	: 'Invalid URL',
				'valid'	: False,
			}
			return render(request, 'extra_templates/account_validation.html', context)

class PasswordResetView(View):
	template_name = "password_reset/password_reset.html"
	
	def get(self, request):
		password_reset_form = PasswordResetForm()
		context = {
			"form"	: password_reset_form
		}
		return render(request, self.template_name, context)

	def post(self, request):
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = CustomUser.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset/password_reset_email.html"
					c = {
						"email": user.email,
						'domain': get_current_site(request),
						'site_name': 'PyTutor-OM',
						"uid": urlsafe_base64_encode(force_bytes(user.pk)),
						"user": user,
						'token': default_token_generator.make_token(user),
						'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@pytutor.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ('users:password-reset-done')

			else:
				context = {
					"form"	: password_reset_form
				}
				messages.error(request, f"No account linked with the '{data}'. Please provide a valid email linked with your account")
				return render(request, self.template_name, context)

		else:
			context = {
				"form"	: password_reset_form
			}
			messages.error(request, 'Please provide valid email address linked to your account')
			return render(request, self.template_name, context)

class ProfileView(View):
	template_name = 'profile/profile.html'

	def get(self, request):
		context = {
			'title'		: 'Profile',
			'form'		: UserUpdateForm(instance=request.user),
		}
		return render(request, self.template_name, context)

	def post(self, request):
		form = UserUpdateForm(request.POST, instance=request.user)

		if form.is_valid():
			form.save()

		else:
			messages.error(request, "Please fix the issues mentioned below")
			context = {
				'title'		: 'Profile',
				'form'		: form,
			}
			return render(request, self.template_name, context)

		messages.success(request, 'Profile information updated successfuly')
		return redirect('users:profile')