from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from pytutor.decorators import allowed_users
from users.models import CustomUser
from datetime import datetime
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from teachers_portal.models import (
	Course,
	Quiz,
	TeacherEnrollment,
)
from administration.models import (
	Subject
)
import random
from .models import (
	Enrollment,
	TopicProgress,
	QuizProgress,
	Answer,
)

@method_decorator(allowed_users(allowed_roles=['Student']), name='dispatch')
class DashboardView(View):
	template_name = 'students_dashboard.html'

	def get(self, request):
		context = {
			'title'		: 'Dashboard',
		}
		return render(request, self.template_name, context)

@method_decorator(allowed_users(allowed_roles=['Student']), name='dispatch')
class ExploreCourseView(View):
	template_name = 'explore_course.html'

	def get(self, request):
		courses = Course.objects.all()
		subject = request.GET.get('subject', None)
		teacher = request.GET.get('teacher', None)

		if subject:
			courses = courses.filter(subject__slug=subject)

		if teacher:
			courses = courses.filter(created_by_id=teacher)

		message_header = f"No courses available!"
		message_body = f"Sorry, there are currently no courses available. Please check back later or contact your administrator for more information."
		
		context = {
			'title'		: 'Explore Course',
			'courses'	: courses,
			'message_body'		: message_body,
			'message_header'	: message_header,
		}
		return render(request, self.template_name, context)

@method_decorator(allowed_users(allowed_roles=['Student']), name='dispatch')
class CourseDetailView(DetailView):
	template_name = 'course_detail.html'
	model = Course

	# override context data
	def get_context_data(self, *args, **kwargs):
		context = super(CourseDetailView, self).get_context_data(*args, **kwargs)

		count = CustomUser.objects.filter(user_type='Teacher', is_active=True).count()
		if count > 5:
			random_index = random.randint(0, count - 5)
			context['teachers'] = CustomUser.objects.filter(user_type='Teacher', is_active=True).order_by('id')[random_index:random_index + 5]

		else:
			context['teachers'] = CustomUser.objects.filter(user_type='Teacher', is_active=True)

		context["title"] = "Course Detail"
		context['subjects'] = Subject.objects.all().values('title', 'slug')
		context['courses'] = Course.objects.all().order_by('-created_on')[:5]
		return context

@method_decorator(allowed_users(allowed_roles=['Student']), name='dispatch')
class CourseEnrollmentView(View):

	def get(self, request, slug):
		course = get_object_or_404(Course, slug=slug)

		# Check if the student is already enrolled in the course
		enrollment_exists = Enrollment.objects.filter(student=request.user, course=course).exists()
		if enrollment_exists:
			messages.warning(request, 'You have already enrolled in this course.')
			return redirect('students_portal:course-detail', slug=course.slug)

		# Create a new enrollment for the student and course
		enrollment = Enrollment(
			student=request.user,
			course=course,
			total_topics=course.get_topics_count(),
			total_quizes=course.get_quizes_count(),
			status='Enrolled'
		)
		enrollment.save()

		# Creating instances for students progress against this enrollment
		for topic in course.get_topics_list():
			TopicProgress.objects.create(
				topic = topic,
				enrollment = enrollment,
			)

			# Creating instances for students progress against this enrollment quizes
			for quiz in topic.get_quizes_list():
				QuizProgress.objects.create(
					quiz = quiz,
					enrollment = enrollment,
				)

		# Adding student in teacher enrollment model
		teacher_enrollment, created = TeacherEnrollment.objects.get_or_create(teacher=course.created_by)
		teacher_enrollment.enrolled_students.add(request.user)

		messages.success(request, f"You have successfully enrolled in '{course.title}'!")
		return redirect('students_portal:course-detail', slug=course.slug)

@method_decorator(allowed_users(allowed_roles=['Student']), name='dispatch')
class EnrollmentListView(ListView):
	template_name = 'students_list_template.html'
	model = Enrollment
	context_object_name = 'object_list'
	queryset = Enrollment.objects.all().exclude(status='Dropped')
	ordering = ['pk']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Enrollment List'
		context["page"] = 'Enrollment List'
		return context

@method_decorator(allowed_users(allowed_roles=['Student']), name='dispatch')
class EnrollmentDropView(View):

	def get(self, request, pk):
		enrollment_obj = get_object_or_404(Enrollment, pk=pk)
		enrollment_obj.status = 'Dropped'
		enrollment_obj.save()
		messages.success(request, f"You have successfully dropped course '{enrollment_obj.course.title}' from enrollment!")
		return redirect('students_portal:list-enrollment')

@method_decorator(allowed_users(allowed_roles=['Student']), name='dispatch')
class EnrolledCourseDetailView(View):
	template_name = 'enrolled_course_detail.html'

	# override context data
	def get(self, request, slug):
		course_obj = get_object_or_404(Course, slug=slug)

		context = {
			'title'		: "Course Detail",
			'course'	: course_obj,
		}
		return render(request, self.template_name, context)

@method_decorator(allowed_users(allowed_roles=['Student']), name='dispatch')
class TakeQuizView(View):
	template_name = 'quiz.html'

	# override context data
	def get(self, request, course_slug, topic_slug, quiz_slug):
		course_obj = get_object_or_404(Course, slug=course_slug)
		quiz_obj = get_object_or_404(Quiz, slug=quiz_slug)
		context = {
			'title'		: "Course Detail",
			'course'	: course_obj,
			'quiz'		: quiz_obj,
		}
		return render(request, self.template_name, context)

	def post(self, request, course_slug, topic_slug, quiz_slug):
		course_obj = get_object_or_404(Course, slug=course_slug)
		quiz_obj = get_object_or_404(Quiz, slug=quiz_slug)

		for question in quiz_obj.get_questions_list():
			question_answer = request.POST.get(f'question_{question.pk}')
			time_taken = request.POST.get(f'question_{question.pk}_time_taken')
			attempts_taken = request.POST.get(f'question_{question.pk}_attempts')
			hint_used = request.POST.get(f'question_{question.pk}_hint_used')

			if question.correct_answer and question.correct_answer == question_answer:
				is_correct = True

			else:
				is_correct = False

			answer_obj = Answer(
				quiz = quiz_obj,
				question = question,
				student = request.user,
				answer_text = question_answer,
				time_taken = time_taken,
				attempt = attempts_taken,
				is_correct = is_correct,
				hint_used = hint_used
			)
			answer_obj.save()

		messages.success(request, f'Quiz submitted successfully')
		return redirect('students_portal:students-dashboard')