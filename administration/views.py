from django.shortcuts import render, redirect
from django.views.generic import ListView, View, CreateView, DeleteView
from users.models import CustomUser
from django.utils.decorators import method_decorator
from pytutor.decorators import allowed_users
from django.db.models.functions import TruncMonth
from datetime import datetime
from django.views.generic.edit import UpdateView
from .forms import UserForm, SubjectForm
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Subject
from django.contrib.messages.views import SuccessMessageMixin

@method_decorator(allowed_users(allowed_roles=['Administration']), name='dispatch')
class DashboardView(View):
	template_name = 'administration_dashboard.html'

	def get(self, request):
		users = CustomUser.objects.all()
		active_users_count = CustomUser.objects.filter(is_active=True).count()
		inactive_users_count = CustomUser.objects.filter(is_active=False).count()
		# Getting percentage value for users joined compared to last month
		current_month_users = CustomUser.objects.filter(date_joined__month=datetime.now().month).count()
		previous_month_users = CustomUser.objects.filter(date_joined__month=datetime.now().month-1).count()

		try:
			joined_user_percentage = ((current_month_users - previous_month_users) / previous_month_users) * 100
		
		except ZeroDivisionError:
			joined_user_percentage = 100

		context = {
			'title'		: 'Dashboard',
			'users'		: users,
			'joined_user_percentage'	: joined_user_percentage,
			'active_users_count'		: active_users_count,
			'inactive_users_count'		: inactive_users_count,
		}
		return render(request, self.template_name, context)

@method_decorator(allowed_users(allowed_roles=['Administration']), name='dispatch')
class UserListView(ListView):
	model = CustomUser
	template_name = 'list_template.html'
	ordering = ['pk']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'User List'
		return context

@method_decorator(allowed_users(allowed_roles=['Administration']), name='dispatch')
class UpdateUserView(View):
	template_name = 'create_template.html'
	model = CustomUser
	form = UserForm
	success_url = reverse_lazy('administration:list-users')

	def get(self, request, pk):
		try:
			user_obj = CustomUser.objects.get(pk=pk)

		except CustomUser.DoesNotExist:
			messages.error(request, f"User not fond")
			return redirect(request.META.get('HTTP_REFERER'))

		form = UserForm(instance=user_obj)
		context = {
			'title'		: 'Edit User Details',
			'form'		: form,
		}
		return render(request, self.template_name, context)


	def post(self, request, pk):
		try:
			user_obj = CustomUser.objects.get(pk=pk)

		except CustomUser.DoesNotExist:
			messages.error(request, f"User not fond")
			return redirect(request.META.get('HTTP_REFERER'))
			
		form = UserForm(request.POST, instance=user_obj)

		if form.is_valid():
			form.save()

		else:
			context = {
				'title'		: 'Edit User Details',
				'form'		: form,
			}
			messages.error(request, "Please fix the issues mentioed below")
			return render(request, self.template_name, context)

		messages.success(request, 'User information updated successfuly')
		return redirect(request.META.get('HTTP_REFERER'))

@method_decorator(allowed_users(allowed_roles=['Administration']), name='dispatch')
class SubjectListView(ListView):
	template_name = 'subject_list.html'
	model = Subject
	ordering = ['pk']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Subject List'
		return context

@method_decorator(allowed_users(allowed_roles=['Administration']), name='dispatch')
class SubjectCreateView(SuccessMessageMixin, CreateView):
	model = Subject
	template_name = 'create_template.html'
	form_class = SubjectForm
	success_url = reverse_lazy('administration:subject-list')
	success_message = "Subject was created successfully"


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Create Subject'
		return context

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super().form_valid(form)

@method_decorator(allowed_users(allowed_roles=['Administration']), name='dispatch')
class SubjectUpdateView(SuccessMessageMixin, UpdateView):
	model = Subject
	template_name = 'create_template.html'
	form_class = SubjectForm
	success_url = reverse_lazy('administration:subject-list')
	success_message = "Subject was updated successfully"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Update Subject'
		return context

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super().form_valid(form)

@method_decorator(allowed_users(allowed_roles=['Administration']), name='dispatch')
class SubjectDeleteView(SuccessMessageMixin, DeleteView):
	template_name = 'confirm_delete.html'
	model = Subject
	success_url = reverse_lazy('administration:subject-list')
	success_message = "Subject was deleted successfully"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Delete Subject'
		context["subject"] = 'subject'
		return context
