from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
    path('dashbaord', views.DashboardView.as_view(), name='administration-dashboard'),
    path('user/list', views.UserListView.as_view(), name='list-users'),
    path('user/<int:pk>/edit', views.UpdateUserView.as_view(), name='update-user'),
    # Subjects
    path('list/subject', views.SubjectListView.as_view(), name='subject-list'),
    path('create/subject', views.SubjectCreateView.as_view(), name='create-subject'),
    path('update/<slug:slug>/subject', views.SubjectUpdateView.as_view(), name='update-subject'),
    path('delete/<slug:slug>/subject', views.SubjectDeleteView.as_view(), name='delete-subject'),
]
