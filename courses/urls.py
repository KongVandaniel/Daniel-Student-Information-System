# student_system/courses/urls.py

# import path from django.urls module for URL reversal
from django.urls import path
# import views from the current module for view functions
from . import views

# set the application name for URL reversal
app_name = 'courses'

# define the URL patterns for the courses app
urlpatterns = [
    # FBV URLs
    # path('') creates a URL pattern for the root URL
    # views.course_list is the view function that will be called when the URL is accessed
    # name='course_list' is the name of the URL pattern
    path('', views.course_list, name='course_list'),
    # path('<int:pk>/', ...) creates a URL pattern for a specific course by its primary key
    # views.course_detail is the view function that will be called when the URL is accessed
    # name='course_detail' is the name of the URL pattern
    path('<int:pk>/', views.course_detail, name='course_detail'),
    # path('create/', ...) creates a URL pattern for creating a new course
    # views.course_create is the view function that will be called when the URL is accessed
    # name='course_create' is the name of the URL pattern
    path('create/', views.course_create, name='course_create'),
    # path('<int:pk>/update/', ...) creates a URL pattern for updating a specific course by its primary key
    # views.course_update is the view function that will be called when the URL is accessed
    # name='course_update' is the name of the URL pattern
    path('<int:pk>/update/', views.course_update, name='course_update'),
    # path('<int:pk>/delete/', ...) creates a URL pattern for deleting a specific course by its primary key
    # views.course_delete is the view function that will be called when the URL is accessed
    # name='course_delete' is the name of the URL pattern
    path('<int:pk>/delete/', views.course_delete, name='course_delete'),
    
    # CBV URLs
    # path('cbv/list/', ...) creates a URL pattern for the root URL
    # views.CourseListView.as_view() is the view function that will be called when the URL is accessed
    # name='course_list_cbv' is the name of the URL pattern
    path('cbv/list/', views.CourseListView.as_view(), name='course_list_cbv'),
    # path('cbv/<int:pk>/', ...) creates a URL pattern for a specific course by its primary key
    # views.CourseDetailView.as_view() is the view function that will be called when the URL is accessed
    # name='course_detail_cbv' is the name of the URL pattern
    path('cbv/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail_cbv'),
    # path('cbv/create/', ...) creates a URL pattern for creating a new course
    # views.CourseCreateView.as_view() is the view function that will be called when the URL is accessed
    # name='course_create_cbv' is the name of the URL pattern
    path('cbv/create/', views.CourseCreateView.as_view(), name='course_create_cbv'),
    # path('cbv/<int:pk>/update/', ...) creates a URL pattern for updating a specific course by its primary key
    # views.CourseUpdateView.as_view() is the view function that will be called when the URL is accessed
    # name='course_update_cbv' is the name of the URL pattern
    path('cbv/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update_cbv'),
    # path('cbv/<int:pk>/delete/', ...) creates a URL pattern for deleting a specific course by its primary key
    # views.CourseDeleteView.as_view() is the view function that will be called when the URL is accessed
    # name='course_delete_cbv' is the name of the URL pattern
    path('cbv/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete_cbv'),
]
