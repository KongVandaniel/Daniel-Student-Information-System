from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.urls import reverse_lazy
from .models import Enrollment
from .forms import EnrollmentForm, GradeForm, EnrollmentFilterForm

def staff_required(view_func):
    """Allow only staff members and superusers to manage enrollments."""
    from django.contrib.auth.decorators import user_passes_test

    return user_passes_test(
        lambda user: user.is_authenticated
        and (user.is_staff or user.is_superuser)
    )(view_func)


def get_accessible_enrollment(request, pk):
    """Allow staff to access any enrollment and students only their own."""
    enrollment = Enrollment.objects.select_related('student', 'course')

    if request.user.is_staff or request.user.is_superuser:
        return get_object_or_404(enrollment, pk=pk)

    return get_object_or_404(
        enrollment,
        pk=pk,
        student__user=request.user
    )

# Function-Based Views (FBV)

@login_required
def enrollment_list(request):
    """List enrollments accessible to the current user."""
    enrollments = Enrollment.objects.select_related('student', 'course')

    if not (request.user.is_staff or request.user.is_superuser):
        enrollments = enrollments.filter(student__user=request.user)

    form = EnrollmentFilterForm(request.GET or None)
    
    # Apply filters
    if form.is_valid():
        if form.cleaned_data.get('status'):
            enrollments = enrollments.filter(status=form.cleaned_data['status'])
        
        if form.cleaned_data.get('student'):
            enrollments = enrollments.filter(
                student__student_id__icontains=form.cleaned_data['student']
            )
        
        if form.cleaned_data.get('course'):
            enrollments = enrollments.filter(
                course__code__icontains=form.cleaned_data['course']
            )
    
    context = {
        'enrollments': enrollments,
        'form': form,
    }
    return render(request, 'enrollments/enrollment_list.html', context)

@login_required
def enrollment_detail(request, pk):
    """Display an enrollment accessible to the current user."""
    enrollment = get_accessible_enrollment(request, pk)

    context = {'enrollment': enrollment}
    return render(request, 'enrollments/enrollment_detail.html', context)

@staff_required
def enrollment_create(request):
    """Allow only staff and superusers to create enrollments."""
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save()
            return redirect(
                'enrollments:enrollment_detail',
                pk=enrollment.pk
            )
    else:
        form = EnrollmentForm()

    context = {'form': form, 'title': 'Create Enrollment'}
    return render(request, 'enrollments/enrollment_form.html', context)

@staff_required
def enrollment_update(request, pk):
    """Allow only staff and superusers to update enrollments."""
    enrollment = get_object_or_404(Enrollment, pk=pk)

    if request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect(
                'enrollments:enrollment_detail',
                pk=enrollment.pk
            )
    else:
        form = EnrollmentForm(instance=enrollment)

    context = {
        'form': form,
        'enrollment': enrollment,
        'title': 'Update Enrollment'
    }
    return render(request, 'enrollments/enrollment_form.html', context)

@staff_required
def enrollment_delete(request, pk):
    """Allow only staff and superusers to delete enrollments."""
    enrollment = get_object_or_404(Enrollment, pk=pk)

    if request.method == 'POST':
        enrollment.delete()
        return redirect('enrollments:enrollment_list')

    context = {'enrollment': enrollment}
    return render(
        request,
        'enrollments/enrollment_confirm_delete.html',
        context
    )

@staff_required
def add_grade(request, pk):
    """Allow only staff and superusers to manage grades."""
    enrollment = get_object_or_404(Enrollment, pk=pk)

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect(
                'enrollments:enrollment_detail',
                pk=enrollment.pk
            )
    else:
        form = GradeForm(instance=enrollment)

    context = {
        'form': form,
        'enrollment': enrollment
    }
    return render(request, 'enrollments/add_grade.html', context)

@login_required
def student_transcript(request, student_id):
    """Display a student's transcript with appropriate access control."""
    from students.models import Student

    student = Student.objects.filter(student_id=student_id).first()

    if not student and str(student_id).isdigit():
        student = Student.objects.filter(pk=int(student_id)).first()

    if not student:
        raise Http404("Student not found")

    if not (request.user.is_staff or request.user.is_superuser):
        if student.user_id != request.user.id:
            raise Http404("Student not found")

    enrollments = student.enrollments.all()

    completed_courses = enrollments.filter(
        status='COMPLETED',
        score__isnull=False
    )

    average_score = completed_courses.aggregate(
        Avg('score')
    )['score__avg']

    context = {
        'student': student,
        'enrollments': enrollments,
        'average_score': round(average_score, 2) if average_score else 0,
        'total_courses': enrollments.count(),
        'completed_courses': completed_courses.count(),
    }

    return render(
        request,
        'enrollments/student_transcript.html',
        context
    )

# Class-Based Views (CBV)

class EnrollmentListView(LoginRequiredMixin, ListView):
    """List enrollments accessible to the current user."""
    model = Enrollment
    template_name = 'enrollments/enrollment_list.html'
    context_object_name = 'enrollments'
    paginate_by = 20

    def get_queryset(self):
        queryset = Enrollment.objects.select_related(
            'student', 'course'
        )

        if not (
            self.request.user.is_staff
            or self.request.user.is_superuser
        ):
            queryset = queryset.filter(
                student__user=self.request.user
            )

        return queryset.order_by('-enrollment_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = EnrollmentFilterForm(
            self.request.GET or None
        )
        return context

class EnrollmentDetailView(LoginRequiredMixin, DetailView):
    """Display an enrollment accessible to the current user."""
    model = Enrollment
    template_name = 'enrollments/enrollment_detail.html'
    context_object_name = 'enrollment'

    def get_queryset(self):
        queryset = Enrollment.objects.select_related('student', 'course')

        if not (
            self.request.user.is_staff
            or self.request.user.is_superuser
        ):
            queryset = queryset.filter(
                student__user=self.request.user
            )

        return queryset


class EnrollmentCreateView(
    LoginRequiredMixin, UserPassesTestMixin, CreateView
):
    """Allow only staff and superusers to create enrollments."""
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'enrollments/enrollment_form.html'
    success_url = reverse_lazy('enrollments:enrollment_list')

    def test_func(self):
        return (
            self.request.user.is_staff
            or self.request.user.is_superuser
        )

class EnrollmentUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    """Allow only staff and superusers to update enrollments."""
    model = Enrollment
    form_class = EnrollmentForm
    template_name = 'enrollments/enrollment_form.html'
    success_url = reverse_lazy('enrollments:enrollment_list')

    def test_func(self):
        return (
            self.request.user.is_staff
            or self.request.user.is_superuser
        )


class EnrollmentDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, DeleteView
):
    """Allow only staff and superusers to delete enrollments."""
    model = Enrollment
    template_name = 'enrollments/enrollment_confirm_delete.html'
    success_url = reverse_lazy('enrollments:enrollment_list')

    def test_func(self):
        return (
            self.request.user.is_staff
            or self.request.user.is_superuser
        )
