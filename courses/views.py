# courses/views.py

# import render, get_object_or_404, redirect from django.shortcuts module for view functions
# render is used to render a template
# get_object_or_404 is used to get an object or return a 404 error
# redirect is used to redirect to another URL
from django.shortcuts import render, get_object_or_404, redirect
# import ListView, DetailView, CreateView, UpdateView, DeleteView from django.views.generic module for view functions
# ListView is used to display a list of objects
# DetailView is used to display detail of a single object
# CreateView is used to create a new object
# UpdateView is used to update an object
# DeleteView is used to delete an object
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# import LoginRequiredMixin, UserPassesTestMixin from django.contrib.auth.mixins module for view functions
# LoginRequiredMixin is used to require login to access a view
# UserPassesTestMixin is used to require a user to pass a test to access a view
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# import login_required from django.contrib.auth.decorators module for view functions
# login_required is used to require login to access a view
from django.contrib.auth.decorators import login_required
# import Q, Count from django.db.models module for view functions
# Q is used to perform complex queries
# Count is used to count the number of objects
from django.db.models import Q, Count
# import reverse_lazy from django.urls module for view functions
# reverse_lazy is used to reverse a URL
from django.urls import reverse_lazy
# import Course model from .models module for view functions
from .models import Course
# import CourseForm, CourseFilterForm from .forms module for view functions
from .forms import CourseForm, CourseFilterForm

# Function-Based Views (FBV)
# Function-Based Views are views that are defined as functions
# FBV is more concise and easier to understand than CBV
# FBV is less flexible than CBV
# FBV is not as reusable as CBV
# FBV is not as maintainable as CBV

# FBV for listing courses with pagination
# request is a parameter that is passed to the view function
# it is a HttpRequest object that contains information about the request
# it has the following attributes: method, GET, POST, COOKIES, session, user, etc.
# it has the following methods: is_ajax(), is_secure(), etc.
def course_list(request):
    """List all courses with filtering options"""
    # Get all courses
    courses = Course.objects.all()
    # Get the filter form
    form = CourseFilterForm(request.GET or None)
    # Apply filters
    if form.is_valid(): # form.is_valid() is a method that returns True if the form is valid according to the validation rules
        # Filter by level
        if form.cleaned_data.get('level'): # form.cleaned_data is a dictionary that contains the form data
            courses = courses.filter(level=form.cleaned_data['level'])
        # Filter by status
        if form.cleaned_data.get('status'): # form.cleaned_data.get() is a method that returns the value of the specified key
            courses = courses.filter(status=form.cleaned_data['status'])
        # Filter by search
        if form.cleaned_data.get('search'): # form.cleaned_data.get() is a method that returns the value of the specified key
            search = form.cleaned_data['search'] # search is a variable that contains the search term
            # __icontains is used to perform a case-insensitive search
            # | is used to perform an OR operation
            # Q() is used to perform complex queries
            courses = courses.filter(
                Q(code__icontains=search) |
                Q(title__icontains=search)
            )
    # Context for the template
    context = {
        'courses': courses,
        'form': form,
    }
    # Render the template
    return render(request, 'courses/course_list.html', context)

def course_detail(request, pk):
    """Display detailed information about a course"""
    # Get the course by primary key
    course = get_object_or_404(Course, pk=pk)
    # Get all enrollments for the course
    enrollments = course.enrollments.all()
    # Get the total number of students
    total_students = enrollments.count()
    # Context for the template
    context = {
        'course': course,
        'enrollments': enrollments,
        'total_students': total_students,
    }
    # Render the template
    return render(request, 'courses/course_detail.html', context)

#@login_required is a decorator that requires login to access a view
@login_required
# Course Creation View
def course_create(request):
    """Create a new course"""
    # Check if the request method is POST
    if request.method == 'POST':
        # Create a new form with the POST data
        form = CourseForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            # Save the form
            form.save()
            # Redirect to the course list
            return redirect('courses:course_list')
    else:
        # Create a new form
        form = CourseForm()
    # Context for the template
    context = {'form': form, 'title': 'Create Course'}
    # Render the template
    return render(request, 'courses/course_form.html', context)

@login_required
# Course Update View
def course_update(request, pk):
    """Update course information"""
    # Get the course by primary key
    course = get_object_or_404(Course, pk=pk)
    # Check if the request method is POST
    if request.method == 'POST':
        # Create a new form with the POST data
        form = CourseForm(request.POST, instance=course)
        # Check if the form is valid
        if form.is_valid():
            # Save the form
            form.save()
            # Redirect to the course detail
            return redirect('courses:course_detail', pk=course.pk)
    else:
        # Create a new form with the instance
        form = CourseForm(instance=course)
    # Context for the template
    context = {'form': form, 'course': course, 'title': 'Update Course'}
    # Render the template
    return render(request, 'courses/course_form.html', context)

@login_required
# Course Deletion View
def course_delete(request, pk):
    """Delete a course"""
    # Get the course by primary key
    course = get_object_or_404(Course, pk=pk)
    # Check if the request method is POST
    if request.method == 'POST':
        # Delete the course
        course.delete()
        # Redirect to the course list
        return redirect('courses:course_list')
    # Context for the template
    context = {'course': course}
    # Render the template
    return render(request, 'courses/course_confirm_delete.html', context)

# Class-Based Views (CBV)
# CBV is a view that is defined as a class
# CBV is more concise and easier to understand than FBV
# CBV is more flexible than FBV
# CBV is more reusable than FBV
# CBV is more maintainable than FBV

# Class-Based View for listing courses with pagination
# ListView is a generic view that is used to display a list of objects
class CourseListView(ListView):
    """Class-based view for listing courses with pagination"""
    # Specify the model to use for the view
    model = Course
    # Specify the template to use for the view
    template_name = 'courses/course_list.html'
    # Specify the context object name to use for the view
    context_object_name = 'courses'
    # Specify the pagination to use for the view
    paginate_by = 10
    
    # get_queryset method is used to get the queryset for the view
    # it is used to get the queryset for the view
    def get_queryset(self):
        queryset = Course.objects.annotate(student_count=Count('enrollments'))
        
        level = self.request.GET.get('level')
        status = self.request.GET.get('status')
        search = self.request.GET.get('search')
        
        if level:
            queryset = queryset.filter(level=level)
        if status:
            queryset = queryset.filter(status=status)
        if search:
            queryset = queryset.filter(
                Q(code__icontains=search) |
                Q(title__icontains=search)
            )
        
        return queryset.order_by('code')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CourseFilterForm(self.request.GET or None)
        return context

class CourseDetailView(DetailView):
    """Class-based view for course details"""
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = self.object.enrollments.all()
        context['total_students'] = self.object.enrollments.count()
        return context

class CourseCreateView(LoginRequiredMixin, CreateView):
    """Class-based view for creating a new course"""
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course_list')

class CourseUpdateView(LoginRequiredMixin, UpdateView):
    """Class-based view for updating course information"""
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course_list')

class CourseDeleteView(LoginRequiredMixin, DeleteView):
    """Class-based view for deleting a course"""
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:course_list')
