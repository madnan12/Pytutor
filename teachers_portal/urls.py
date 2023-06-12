from django.urls import path
from . import views

app_name = 'teachers_portal'

urlpatterns = [
    path('dashbaord', views.DashboardView.as_view(), name='teachers-dashboard'),
    path('list/course', views.CourseListView.as_view(), name='course-list'),
    path('create/course', views.CourseCreateView.as_view(), name='create-course'),
    path('update/<slug:slug>/course', views.CourseUpdateView.as_view(), name='update-course'),
    path('delete/<slug:slug>/course', views.CourseDeleteView.as_view(), name='delete-course'),
    # Topic
    path('list/topic', views.TopicListView.as_view(), name='topic-list'),
    path('create/topic', views.TopicCreateView.as_view(), name='create-topic'),
    path('update/<slug:slug>/topic', views.TopicUpdateView.as_view(), name='update-topic'),
    path('delete/<slug:slug>/topic', views.TopicDeleteView.as_view(), name='delete-topic'),
    # Quiz
    path('list/quiz', views.QuizListView.as_view(), name='quiz-list'),
    path('create/quiz', views.QuizCreateView.as_view(), name='create-quiz'),
    path('update/<slug:slug>/quiz', views.QuizUpdateView.as_view(), name='update-quiz'),
    path('delete/<slug:slug>/quiz', views.QuizDeleteView.as_view(), name='delete-quiz'),
    # Enrollment
    path('enrollment/list/student', views.EnrolledStudentsListView.as_view(), name='list-students'),
    path('enrollment/<int:pk>/student', views.EnrolledStudentDetailView.as_view(), name='enrolled-student-detail'),
    path('students/<int:pk>/quiz/', views.TeacherQuizView.as_view(), name='quiz'),
    path('students/<int:pk>/quiz-answers/', views.TeacherQuizAnswersView.as_view(), name='all-quiz-answers'),
    path('students/<int:pk>/edit_answer/', views.TeacherEditAnswerView.as_view(), name='edit-quiz-answers'),

]
