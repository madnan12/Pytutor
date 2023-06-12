from django.urls import path
from . import views

app_name = 'students_portal'

urlpatterns = [
    path('dashbaord', views.DashboardView.as_view(), name='students-dashboard'),
    path('explore-courses', views.ExploreCourseView.as_view(), name='explore-courses'),
    path('course/<slug:slug>/detail', views.CourseDetailView.as_view(), name='course-detail'),
    path('course/<slug:slug>/enroll', views.CourseEnrollmentView.as_view(), name='enroll-course'),
    # Enrollment
    path('enrollment/list', views.EnrollmentListView.as_view(), name='list-enrollment'),
    path('enrollment/<int:pk>/drop', views.EnrollmentDropView.as_view(), name='drop-enrollment'),
    path('enrollment/<slug:slug>/detail', views.EnrolledCourseDetailView.as_view(), name='enrolled-course-detail'),
    # Quiz
    path('enrollment/<slug:course_slug>/<slug:topic_slug>/<slug:quiz_slug>', views.TakeQuizView.as_view(), name='take-quiz'),
]
