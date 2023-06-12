from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from pytutor.decorators import allowed_users
from users.models import CustomUser
from datetime import datetime
from .models import (
	Course,
	Topic,
	Quiz,
	QuizQuestion,
	QuestionChoices,
	TeacherEnrollment,
)
from .forms import (
	CourseForm,
	TopicForm,
	AnswerForm,
)
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from students_portal.models import(
	Answer,
	Enrollment,
	QuizProgress,
)
from django.db.models import Count
from django.http import Http404

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class DashboardView(View):
	template_name = 'teachers_dashboard.html'

	def get(self, request):
		# Getting total enrollments for your courses
		teacher_courses = Course.objects.filter(created_by=request.user)
		total_enrollments = Enrollment.objects.filter(course__in=teacher_courses)

		# Getting percentage value for new enrollments compared to last month
		current_month_enrollment_count = total_enrollments.filter(enroll_date__month=datetime.now().month).count()
		previous_month_enrollment_count = total_enrollments.filter(enroll_date__month=datetime.now().month-1).count()

		try:
			joined_enrollment_percentage = ((current_month_enrollment_count - previous_month_enrollment_count) / previous_month_enrollment_count) * 100
		
		except ZeroDivisionError:
			joined_enrollment_percentage = 100

		# Getting total students count who enrolled for your courses
		enrolled_students = total_enrollments.values('student').distinct()
		total_students = enrolled_students.count()

		# Getting percentage value for students joined compared to last month
		current_month_student_count = enrolled_students.filter(enroll_date__month=datetime.now().month).count()
		previous_month_student_count = enrolled_students.filter(enroll_date__month=datetime.now().month-1).count()

		try:
			joined_students_percentage = ((current_month_student_count - previous_month_student_count) / previous_month_student_count) * 100
		
		except ZeroDivisionError:
			joined_students_percentage = 100

		# Getting total course count
		total_course_count = teacher_courses.count()
		# Getting percentage value for courses created compared to last month
		current_month_course_count = Course.objects.filter(created_on__month=datetime.now().month).count()
		previous_month_course_count = Course.objects.filter(created_on__month=datetime.now().month-1).count()

		try:
			created_course_percentage = ((current_month_course_count - previous_month_course_count) / previous_month_course_count) * 100
		
		except ZeroDivisionError:
			created_course_percentage = 100

		context = {
			'title'				: 'Dashboard',
			'total_students'	: total_students,
			'joined_students_percentage'		: joined_students_percentage,
			'total_enrollments'					: total_enrollments,
			'joined_enrollment_percentage'		: joined_enrollment_percentage,
			'total_course_count'				: total_course_count,
			'created_course_percentage'			: created_course_percentage,
		}
		return render(request, self.template_name, context)

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class CourseListView(ListView):
	template_name = 'course_list.html'
	model = Course
	ordering = ['pk']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Course List'
		context["page"] = 'Course List'
		return context

	def get_queryset(self) :
		queryset = Course.objects.filter(created_by=self.request.user)
		return queryset

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class CourseCreateView(SuccessMessageMixin, CreateView):
	model = Course
	template_name = 'teachers_create_template.html'
	form_class = CourseForm
	success_url = reverse_lazy('teachers_portal:course-list')
	success_message = "Course was created successfully"


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Create Course'
		return context

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super().form_valid(form)

	def get_queryset(self):
		return super().get_queryset().filter(created_by=self.request.user)

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class CourseUpdateView(SuccessMessageMixin, UpdateView):
	model = Course
	template_name = 'teachers_create_template.html'
	form_class = CourseForm
	success_url = reverse_lazy('teachers_portal:course-list')
	success_message = "Course was updated successfully"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Update Course'
		return context

	def get_object(self, queryset=None):
		obj = super().get_object(queryset=queryset)
		if obj.created_by != self.request.user:
			raise Http404()
		return obj
		return queryset

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super().form_valid(form)

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class CourseDeleteView(SuccessMessageMixin, DeleteView):
	template_name = 'confirm_delete.html'
	model = Course
	success_url = reverse_lazy('teachers_portal:course-list')
	success_message = "Course was deleted successfully"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Delete Course'
		context["subject"] = 'course'
		return context

	def get_object(self, queryset=None):
		obj = super().get_object(queryset=queryset)
		if obj.created_by != self.request.user:
			raise Http404()
		return obj
		return queryset

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class TopicListView(ListView):
	template_name = 'course_list.html'
	model = Topic
	ordering = ['pk']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Topic List'
		context["page"] = 'Subject List'
		return context

	def get_queryset(self) :
		queryset = Topic.objects.filter(created_by=self.request.user)
		return queryset

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class TopicCreateView(SuccessMessageMixin, CreateView):
	model = Topic
	template_name = 'teachers_create_template.html'
	form_class = TopicForm
	success_url = reverse_lazy('teachers_portal:course-list')
	success_message = "Topic was created successfully"


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Create Topic'
		return context

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super().form_valid(form)

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class TopicUpdateView(SuccessMessageMixin, UpdateView):
	model = Topic
	template_name = 'teachers_create_template.html'
	form_class = TopicForm
	success_url = reverse_lazy('teachers_portal:course-list')
	success_message = "Topic was updated successfully"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Update Topic'
		return context

	def get_object(self, queryset=None):
		obj = super().get_object(queryset=queryset)
		if obj.created_by != self.request.user:
			raise Http404()
		return obj
		return queryset

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super().form_valid(form)

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class TopicDeleteView(SuccessMessageMixin, DeleteView):
	template_name = 'confirm_delete.html'
	model = Topic
	success_url = reverse_lazy('teachers_portal:course-list')
	success_message = "Topic was deleted successfully"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Delete Topic'
		context["subject"] = 'course'
		return context

	def get_object(self, queryset=None):
		obj = super().get_object(queryset=queryset)
		if obj.created_by != self.request.user:
			raise Http404()
		return obj
		return queryset

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class QuizListView(ListView):
	template_name = 'course_list.html'
	model = Quiz
	ordering = ['pk']

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Quiz List'
		context["page"] = 'Quiz List'
		return context

	def get_queryset(self) :
		queryset = Quiz.objects.filter(created_by=self.request.user)
		return queryset

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class QuizCreateView(SuccessMessageMixin, CreateView):
	template_name = 'create_quiz.html'

	def get(self, request):
		topics = Topic.objects.filter(created_by=request.user)
		context = {
			'title'		: 'Create Quiz',
			'topics'	: topics,
		}
		return render(request, self.template_name, context)

	def post(self, request):
		title = request.POST.get('quiz-title')
		description = request.POST.get('quiz-description')
		topic = request.POST.get('quiz-topic')
		questions_order = request.POST.get('quiz-questions-order')

		current_user = request.user

		quiz_obj = Quiz(
			title = title,
			description = description,
			topic_id = int(topic),
			created_by = current_user,
			questions_order = questions_order
		)
		quiz_obj.save()

		# Getting questions information
		total_number_of_forms = int(request.POST.get('form-TOTAL_FORMS'))
		for count in range(total_number_of_forms):
			question_statement = request.POST.get(f'form-{count}-question')
			question_type = request.POST.get(f'form-{count}-question_type')
			is_required = request.POST.get(f'form-{count}-question_required')
			number_of_choices = request.POST.get(f'form-{count}-number_of_options', None)
			if question_type == 'checkbox':
				correct_answer = request.POST.getlist(f'form-{count}-question_answer', None)
			else:
				correct_answer = request.POST.get(f'form-{count}-question_answer', None)

			hint_text = request.POST.get(f'form-{count}-question_hint')

			correct_choice = ''
			
			question_obj = QuizQuestion(
				quiz = quiz_obj, question = question_statement,
				question_type = question_type, hint_text = hint_text,
				is_required = is_required, created_by = current_user
			)
			question_obj.save()

			if number_of_choices and int(number_of_choices) >= 1:
				for choice_num in range(int(number_of_choices)):
					choice_statement = request.POST.get(f'form-{count}-question_choice-{choice_num}')
					choice_obj = QuestionChoices(
						quiz = quiz_obj,
						question = question_obj,
						choice_statement = choice_statement
					)
					choice_obj.save()

					if question_type == 'checkbox' and f'Choice {choice_num}' in correct_answer:
						if len(correct_choice) == 0:
							correct_choice = choice_statement
						else:
							correct_choice = f"{correct_choice},{choice_statement}"
					
					elif question_type == 'radio' and f'Choice {choice_num}' == correct_answer:
						correct_choice = choice_statement

			if question_type == 'checkbox' or question_type == 'radio':
				question_obj.correct_answer = correct_choice
				question_obj.save()

			else:
				question.correct_answer = correct_answer
				question_obj.save()

		messages.success(request, f"Quiz created successfuly")
		return redirect('teachers_portal:quiz-list')

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class QuizUpdateView(SuccessMessageMixin, UpdateView):
	template_name = 'edit_quiz.html'
	
	def get(self, request, slug):
		try:
			quiz_obj = Quiz.objects.get(slug=slug)

		except Exception as exc:
			messages.error(request, f"Quiz doesn't exist")

		topics = Topic.objects.filter(created_by=request.user)
		context = {
			'title'		: 'Edit Quiz',
			'topics'	: topics,
			'quiz'	: quiz_obj,
		}
		return render(request, self.template_name, context)

	def post(self, request, slug):
		quiz_obj = Quiz.objects.get(slug=slug)

		title = request.POST.get('quiz-title')
		description = request.POST.get('quiz-description')
		topic = request.POST.get('quiz-topic')
		current_user = request.user
		questions_order = request.POST.get('quiz-questions-order')

		quiz_obj.title = title
		quiz_obj.description = description
		quiz_obj.topic_id = int(topic)
		quiz_obj.questions_order = questions_order
		quiz_obj.save()

		for question in quiz_obj.get_questions_list():
			question_statement = request.POST.get(f'form-{question.pk}-question')
			question_type = request.POST.get(f'form-{question.pk}-question_type')
			is_required = request.POST.get(f'form-{question.pk}-question_required')
			number_of_choices = request.POST.get(f'form-{question.pk}-number_of_options', None)
			
			if question_type == 'checkbox':
				correct_answer = request.POST.get(f'form-{question.pk}-question_answer')
			else:
				correct_answer = request.POST.get(f'form-{question.pk}-question_answer')

			hint_text = request.POST.get(f'form-{question.pk}-question_hint')

			correct_choice = ''

			question.question = question_statement
			question.question_type = question_type
			question.is_required = is_required
			question.correct_answer = correct_answer
			question.hint_text = hint_text
			question.save()

			if number_of_choices and int(number_of_choices) >= 1:
				for choice in question.get_question_choices():
					choice_statement = request.POST.get(f'form-{question.pk}-question_choice-{choice.pk}')
					
					choice_obj = QuestionChoices.objects.get(pk=choice.pk)
					choice_obj.choice_statement = choice_statement
					choice_obj.save()

					if question_type == 'checkbox' and choice_statement in correct_answer:
						if len(correct_choice) == 0:
							correct_choice = choice_statement
						else:
							correct_choice = f"{correct_choice},{choice_statement}"
					
					elif question_type == 'radio' and choice_statement == correct_answer:
						correct_choice = choice_statement

			if question_type == 'checkbox' or question_type == 'radio':
				question.correct_answer = correct_choice
				question.save()

			else:
				question.correct_answer = correct_answer
				question.save()

		messages.success(request, f"Quiz updated successfuly")
		return redirect('teachers_portal:quiz-list')

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class QuizDeleteView(SuccessMessageMixin, DeleteView):
	template_name = 'confirm_delete.html'
	model = Quiz
	success_url = reverse_lazy('teachers_portal:quiz-list')
	success_message = "Quiz was deleted successfully"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Delete Quiz'
		context["subject"] = 'quiz'
		return context

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class EnrolledStudentsListView(View):
	template_name = 'student_list.html'

	def get(self, request):
		# Getting total students count who enrolled for your courses
		teacher_courses = Course.objects.filter(created_by=request.user)
		enrollment_obj = Enrollment.objects.filter(course__in=teacher_courses)
		enrolled_students = get_object_or_404(TeacherEnrollment, teacher=request.user)

		context = {
			'title'		: 'Enrollment List',
			'enrollment_obj'	: enrollment_obj,
			'students'	: enrolled_students,
		}
		return render(request, self.template_name, context)

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class EnrolledStudentDetailView(View):
	template_name = 'enrollment_details.html'

	def get(self, request, pk):
		teacher_courses = Course.objects.filter(created_by=request.user)
		student_enrollments = Enrollment.objects.filter(course__in=teacher_courses, student=pk)
		student_id = pk
  
		context = {
			'title'		: 'Student Course Details',
			'student_enrollments'	: student_enrollments,
   			'student_id'	: student_id
		}
		return render(request, self.template_name, context)

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class TeacherQuizView(View):
	template_name = 'teacher_quiz.html'

	def get(self, request):
		teacher_quiz = Quiz.objects.filter(created_by=request.user)
		context = {
			'teacher_quiz': teacher_quiz,
		}
		return render(request, self.template_name, context)

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class TeacherQuizView(View):
	template_name = 'teacher_quiz.html'

	def get(self, request, pk):
		teacher_quiz = Quiz.objects.filter(created_by=request.user)
		student_id = pk
		context = {
			'teacher_quiz': teacher_quiz,
			'student_id': student_id,
		}
		return render(request, self.template_name, context)

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class TeacherQuizAnswersView(View):
	template_name = 'teacher_quiz_answers.html'

	def get(self, request, pk):
		teacher_quiz =  get_object_or_404(Quiz, created_by=request.user)
		quiz_answers = Answer.objects.filter(quiz=teacher_quiz, student=pk)
		context = {
			'quiz_answers': quiz_answers,
   			'teacher_quiz': teacher_quiz
		}
		return render(request, self.template_name, context)

@method_decorator(allowed_users(allowed_roles=['Teacher']), name='dispatch')
class TeacherEditAnswerView(SuccessMessageMixin, UpdateView):

	model = Answer
	template_name = 'edit_quiz_answer.html'
	form_class = AnswerForm
	success_message = "Answer was updated successfully"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["title"] = 'Update Answer'
		return context

	def get_object(self, queryset=None):
		obj = super().get_object(queryset=queryset)
		return obj

	def form_valid(self, form):
		form.instance = form.save(commit=False)
		form.instance.save()
		return super().form_valid(form)

	def get_success_url(self):
		return reverse_lazy('teachers_portal:all-quiz-answers', kwargs={'pk': self.object.student.id})
