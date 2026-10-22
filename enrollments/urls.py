from django.urls import path
from . import views

app_name = 'enrollments'

urlpatterns = [
    # FBV URLs
    path('', views.enrollment_list, name='enrollment_list'),
    path('<int:pk>/', views.enrollment_detail, name='enrollment_detail'),
    path('create/', views.enrollment_create, name='enrollment_create'),
    path('<int:pk>/update/', views.enrollment_update, name='enrollment_update'),
    path('<int:pk>/delete/', views.enrollment_delete, name='enrollment_delete'),
    path('<int:pk>/grade/', views.add_grade, name='add_grade'),
    path('transcript/<str:student_id>/', views.student_transcript, name='student_transcript'),
    
    # CBV URLs
    path('cbv/list/', views.EnrollmentListView.as_view(), name='enrollment_list_cbv'),
    path('cbv/<int:pk>/', views.EnrollmentDetailView.as_view(), name='enrollment_detail_cbv'),
    path('cbv/create/', views.EnrollmentCreateView.as_view(), name='enrollment_create_cbv'),
    path('cbv/<int:pk>/update/', views.EnrollmentUpdateView.as_view(), name='enrollment_update_cbv'),
    path('cbv/<int:pk>/delete/', views.EnrollmentDeleteView.as_view(), name='enrollment_delete_cbv'),
]
