from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Student
from .forms import StudentForm, UserForm, StudentRegistrationForm

# Function-Based Views (FBV)

@login_required
def student_list(request):
    """List all students with search functionality and pagination"""
    search_query = request.GET.get('q', '').strip()
    students_qs = Student.objects.select_related('user').all()
    
    if search_query:
        students_qs = students_qs.filter(
            Q(student_id__icontains=search_query) |
            Q(khmer_name__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )
    
    students_qs = students_qs.order_by('student_id')
    paginator = Paginator(students_qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'students': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'students/student_list.html', context)


@login_required
def student_detail(request, pk):
    """Display detailed information about a student"""
    student = get_object_or_404(Student, pk=pk)
    enrollments = student.enrollments.all()
    
    context = {
        'student': student,
        'enrollments': enrollments,
    }
    return render(request, 'students/student_detail.html', context)

@login_required
def student_update(request, pk):
    """Update student information"""
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        student_form = StudentForm(request.POST, request.FILES, instance=student)
        user_form = UserForm(request.POST, instance=student.user)
        
        if student_form.is_valid() and user_form.is_valid():
            student_form.save()
            user_form.save()
            messages.success(request, f"Student {student.student_id} updated successfully!")
            return redirect('students:student_detail', pk=student.pk)
    else:
        student_form = StudentForm(instance=student)
        user_form = UserForm(instance=student.user)
    
    context = {
        'student_form': student_form,
        'user_form': user_form,
        'form': student_form,
        'student': student,
        'title': f'Edit Student: {student.student_id}',
    }
    return render(request, 'students/student_form.html', context)

def register_student(request):
    """Register a new student"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            # Create user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            
            # Create student profile
            student = Student.objects.create(
                user=user,
                student_id=form.cleaned_data['student_id'],
                khmer_name=form.cleaned_data.get('khmer_name', ''),
                date_of_birth=form.cleaned_data['date_of_birth'],
                gender=form.cleaned_data['gender'],
                phone_number=form.cleaned_data.get('phone_number', ''),
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                country=form.cleaned_data['country'],
            )
            
            messages.success(request, f"Welcome {user.first_name}! Your student registration is complete.")
            
            # Auto-login if not already logged in
            if not request.user.is_authenticated:
                login(request, user)
                return redirect('students:student_detail', pk=student.pk)
            
            return redirect('students:student_detail', pk=student.pk)
    else:
        form = StudentRegistrationForm()
    
    context = {'form': form}
    return render(request, 'students/register.html', context)

@login_required
def student_delete(request, pk):
    """Delete a student"""
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        user = student.user
        student.delete()
        user.delete()
        return redirect('students:student_list')
    
    context = {'student': student}
    return render(request, 'students/student_confirm_delete.html', context)

# Class-Based Views (CBV)

class StudentListView(LoginRequiredMixin, ListView):
    """Class-based view for listing students"""
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Student.objects.select_related('user').all()
        search_query = self.request.GET.get('q', '').strip()
        
        if search_query:
            queryset = queryset.filter(
                Q(student_id__icontains=search_query) |
                Q(khmer_name__icontains=search_query) |
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(user__email__icontains=search_query)
            )
        
        return queryset.order_by('student_id')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '').strip()
        return context

class StudentDetailView(LoginRequiredMixin, DetailView):
    """Class-based view for student details"""
    model = Student
    template_name = 'students/student_detail.html'
    context_object_name = 'student'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = self.object.enrollments.all()
        return context

class StudentCreateView(LoginRequiredMixin, CreateView):
    """Class-based view for creating a new student"""
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:student_list')

    def form_valid(self, form):
        if not hasattr(form.instance, 'user') or form.instance.user_id is None:
            if not hasattr(self.request.user, 'student'):
                form.instance.user = self.request.user
            else:
                student_id = form.cleaned_data.get('student_id', '')
                username = f"std_{student_id.lower()}"
                user, _ = User.objects.get_or_create(
                    username=username,
                    defaults={'first_name': form.cleaned_data.get('khmer_name', student_id)}
                )
                form.instance.user = user
        return super().form_valid(form)

class StudentUpdateView(LoginRequiredMixin, UpdateView):
    """Class-based view for updating student information"""
    model = Student
    form_class = StudentForm
    template_name = 'students/student_form.html'
    success_url = reverse_lazy('students:student_list')

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    """Class-based view for deleting a student"""
    model = Student
    template_name = 'students/student_confirm_delete.html'
    success_url = reverse_lazy('students:student_list')
