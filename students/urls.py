from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # FBV URLs
    path('', views.student_list, name='student_list'),
    path('register/', views.register_student, name='register'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
    path('<int:pk>/update/', views.student_update, name='student_update'),
    path('<int:pk>/delete/', views.student_delete, name='student_delete'),
    
    # CBV URLs
    path('cbv/list/', views.StudentListView.as_view(), name='student_list_cbv'),
    path('cbv/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail_cbv'),
    path('cbv/create/', views.StudentCreateView.as_view(), name='student_create_cbv'),
    path('cbv/<int:pk>/update/', views.StudentUpdateView.as_view(), name='student_update_cbv'),
    path('cbv/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete_cbv'),
]
