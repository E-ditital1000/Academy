from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Avg, Max, Min, Count
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.core.paginator import Paginator
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from accounts.models import User, Student
from app.models import Session, Semester
from result.models import TakenCourse
from accounts.decorators import lecturer_required, student_required
from .forms import (
    ProgramForm, CourseAddForm, CourseAllocationForm, 
    EditCourseAllocationForm, UploadFormFile, UploadFormVideo
)
from .models import Program, Course, CourseAllocation, Upload, UploadVideo


# Program views
@login_required
def program_view(request):
    programs = Program.objects.all()

    program_filter = request.GET.get('program_filter')
    if program_filter:
        programs = Program.objects.filter(title__icontains=program_filter)

    return render(request, 'course/program_list.html', {
        'title': "Programs | DjangoSMS",
        'programs': programs,
    })


@login_required
@lecturer_required
def program_add(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'{request.POST.get("title")} program has been created.')
            return redirect('programs')
        else:
            messages.error(request, 'Correct the error(s) below.')
    else:
        form = ProgramForm()

    return render(request, 'course/program_add.html', {
        'title': "Add Program | DjangoSMS",
        'form': form,
    })


@login_required
def program_detail(request, pk):
    program = Program.objects.get(pk=pk)
    courses = Course.objects.filter(program_id=pk).order_by('-year')
    credits = Course.objects.aggregate(Sum('credit'))

    paginator = Paginator(courses, 10)
    page = request.GET.get('page')

    courses = paginator.get_page(page)

    return render(request, 'course/program_single.html', {
        'title': program.title,
        'program': program, 'courses': courses, 'credits': credits
    })


@login_required
@lecturer_required
def program_edit(request, pk):
    program = Program.objects.get(pk=pk)

    if request.method == 'POST':
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, f'{request.POST.get("title")} program has been updated.')
            return redirect('programs')
    else:
        form = ProgramForm(instance=program)

    return render(request, 'course/program_add.html', {
        'title': "Edit Program | DjangoSMS",
        'form': form
    })


@login_required
@lecturer_required
def program_delete(request, pk):
    program = Program.objects.get(pk=pk)
    title = program.title
    program.delete()
    messages.success(request, f'Program {title} has been deleted.')

    return redirect('programs')


# Course views
@login_required
def course_single(request, slug):
    course = Course.objects.get(slug=slug)
    files = Upload.objects.filter(course__slug=slug)
    videos = UploadVideo.objects.filter(course__slug=slug)

    lecturers = User.objects.filter(allocated_lecturer__pk=course.id)
    lecturers = CourseAllocation.objects.filter(courses__pk=course.id)

    return render(request, 'course/course_single.html', {
        'title': course.title,
        'course': course,
        'files': files,
        'videos': videos,
        'lecturers': lecturers,
        'media_url': settings.MEDIA_ROOT,
    })


@login_required
@lecturer_required
def course_add(request, pk):
    users = User.objects.all()
    if request.method == 'POST':
        form = CourseAddForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.program = Program.objects.get(pk=pk)
            course.save()
            messages.success(request, f'{course.title} ({course.code}) has been created.')
            return redirect('program_detail', pk=pk)
        else:
            messages.error(request, 'Correct the error(s) below.')
    else:
        form = CourseAddForm(initial={'program': Program.objects.get(pk=pk)})

    return render(request, 'course/course_add.html', {
        'title': "Add Course | DjangoSMS",
        'form': form, 'program': pk, 'users': users
    })


@login_required
@lecturer_required
def course_edit(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        form = CourseAddForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'{course.title} ({course.code}) has been updated.')
            return redirect('program_detail', pk=course.program.pk)
        else:
            messages.error(request, 'Correct the error(s) below.')
    else:
        form = CourseAddForm(instance=course)

    return render(request, 'course/course_add.html', {
        'title': "Edit Course | DjangoSMS",
        'form': form, 'course': course
    })


@login_required
@lecturer_required
def course_delete(request, slug):
    course = Course.objects.get(slug=slug)
    course_name = course.title
    course.delete()
    messages.success(request, f'Course {course_name} has been deleted.')

    return redirect('program_detail', pk=course.program.pk)


# Course Allocation
@method_decorator([login_required], name='dispatch')
class CourseAllocationFormView(CreateView):
    form_class = CourseAllocationForm
    template_name = 'course/course_allocation_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        lecturer = form.cleaned_data['lecturer']
        selected_courses = form.cleaned_data['courses']
        courses = []
        for course in selected_courses:
            courses.append(course.pk)
        print(courses)

        try:
            a = CourseAllocation.objects.get(lecturer=lecturer)
        except CourseAllocation.DoesNotExist:
            a = CourseAllocation.objects.create(lecturer=lecturer)
        for course_pk in courses:
            course = Course.objects.get(pk=course_pk)
            a.courses.add(course)
            a.save()
        return redirect('course_allocation_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Assign Course | DjangoSMS"
        return context


@login_required
def course_allocation_view(request):
    allocated_courses = CourseAllocation.objects.all()
    return render(request, 'course/course_allocation_view.html', {
        'title': "Course Allocations | DjangoSMS",
        "allocated_courses": allocated_courses
    })


@login_required
@lecturer_required
def edit_allocated_course(request, pk):
    allocated = get_object_or_404(CourseAllocation, pk=pk)
    if request.method == 'POST':
        form = EditCourseAllocationForm(request.POST, instance=allocated)
        if form.is_valid():
            form.save()
            messages.success(request, 'Allocated course has been updated.')
            return redirect('course_allocation_view')
    else:
        form = EditCourseAllocationForm(instance=allocated)

    return render(request, 'course/course_allocation_form.html', {
        'title': "Edit Course Allocated | DjangoSMS",
        'form': form, 'allocated': pk
    })


@login_required
@lecturer_required
def deallocate_course(request, pk):
    course = CourseAllocation.objects.get(pk=pk)
    course.delete()
    messages.success(request, 'Successfully deallocated!')
    return redirect("course_allocation_view")


# File Upload views
@login_required
@lecturer_required
def handle_file_upload(request, slug):
    course = Course.objects.get(slug=slug)
    if request.method == 'POST':
        form = UploadFormFile(request.POST, request.FILES, {'course': course})
        if form.is_valid():
            form.save()
            messages.success(request, f'{request.POST.get("title")} has been uploaded.')
            return redirect('course_single', slug=slug)
    else:
        form = UploadFormFile()
    return render(request, 'upload/upload_file_form.html', {
        'title': "File Upload | DjangoSMS",
        'form': form, 'course': course
    })


@login_required
@lecturer_required
def handle_file_edit(request, slug, file_id):
    course = Course.objects.get(slug=slug)
    instance = get_object_or_404(Upload, pk=file_id)
    if request.method == 'POST':
        form = UploadFormFile(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f'{request.POST.get("title")} has been updated.')
            return redirect('course_single', slug=slug)
    else:
        form = UploadFormFile(instance=instance)

    return render(request, 'upload/upload_file_form.html', {
        'title': instance.title,
        'form': form, 'course': course})


def handle_file_delete(request, slug, file_id):
    file = Upload.objects.get(pk=file_id)
    file_name = file.name
    file.delete()

    messages.success(request, f'{file.title} has been deleted.')
    return redirect('course_single', slug=slug)


# Video Upload views
@login_required
@lecturer_required
def handle_video_upload(request, slug):
    course = Course.objects.get(slug=slug)
    if request.method == 'POST':
        form = UploadFormVideo(request.POST, request.FILES, {'course': course})
        if form.is_valid():
            form.save()
            messages.success(request, f'{request.POST.get("title")} has been uploaded.')
            return redirect('course_single', slug=slug)
    else:
        form = UploadFormVideo()
    return render(request, 'upload/upload_video_form.html', {
        'title': "Video Upload | DjangoSMS",
        'form': form, 'course': course
    })


@login_required
@lecturer_required
def handle_video_single(request, slug, video_slug):
    course = get_object_or_404(Course, slug=slug)
    video = get_object_or_404(UploadVideo, slug=video_slug)
    return render(request, 'upload/video_single.html', {'video': video})


@login_required
@lecturer_required
def handle_video_edit(request, slug, video_slug):
    course = Course.objects.get(slug=slug)
    instance = get_object_or_404(UploadVideo, slug=video_slug)
    if request.method == 'POST':
        form = UploadFormVideo(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, f'{request.POST.get("title")} has been updated.')
            return redirect('course_single', slug=slug)
    else:
        form = UploadFormVideo(instance=instance)

    return render(request, 'upload/upload_video_form.html', {
        'title': instance.title,
        'form': form, 'course': course})


def handle_video_delete(request, slug, video_slug):
    video = get_object_or_404(UploadVideo, slug=video_slug)
    video.delete()

    messages.success(request, f'{video.title} has been deleted.')
    return redirect('course_single', slug=slug)


# Course Registration
@login_required
@student_required
def course_registration(request):
    if request.method == 'POST':
        course_ids = request.POST.getlist('course_ids')
        student = get_object_or_404(Student, student=request.user)
        
        for course_id in course_ids:
            course = get_object_or_404(Course, pk=course_id)
            TakenCourse.objects.create(student=student, course=course)
        
        messages.success(request, 'Courses registered successfully!')
        return redirect('course_registration')
    else:
        student = get_object_or_404(Student, student=request.user)
        current_semester = Semester.objects.get(is_current_semester=True)
        
        taken_courses = TakenCourse.objects.filter(student=student)
        registered_course_ids = taken_courses.values_list('course__id', flat=True)
        
        courses = Course.objects.filter(program=student.department, level=student.level, semester=current_semester).exclude(id__in=registered_course_ids).order_by('year')
        all_courses = Course.objects.filter(level=student.level, program=student.department)
        
        total_first_semester_credit = courses.filter(semester='First').aggregate(Sum('credit'))['credit__sum'] or 0
        total_sec_semester_credit = courses.filter(semester='Second').aggregate(Sum('credit'))['credit__sum'] or 0
        total_registered_credit = taken_courses.aggregate(Sum('course__credit'))['course__credit__sum'] or 0
        
        no_course_is_registered = taken_courses.count() == 0
        all_courses_are_registered = registered_course_ids.count() == all_courses.count()
        
        context = {
            'is_calender_on': True,
            'all_courses_are_registered': all_courses_are_registered,
            'no_course_is_registered': no_course_is_registered,
            'current_semester': current_semester,
            'courses': courses,
            'total_first_semester_credit': total_first_semester_credit,
            'total_sec_semester_credit': total_sec_semester_credit,
            'registered_courses': taken_courses,
            'total_registered_credit': total_registered_credit,
            'student': student,
        }
        
        return render(request, 'course/course_registration.html', context)


@login_required
@student_required
def course_drop(request):
    if request.method == 'POST':
        course_ids = request.POST.getlist('course_ids')
        student = get_object_or_404(Student, student=request.user)
        
        TakenCourse.objects.filter(student=student, course__id__in=course_ids).delete()
        
        messages.success(request, 'Courses dropped successfully!')
        
    return redirect('course_registration')


@login_required
def user_course_list(request):
    if request.user.is_lecturer:
        courses = Course.objects.filter(allocated_course__lecturer=request.user)

        return render(request, 'course/user_course_list.html', {'courses': courses})

    elif request.user.is_student:
        student = get_object_or_404(Student, student=request.user)
        taken_courses = TakenCourse.objects.filter(student=student)
        courses = Course.objects.filter(level=student.level, program=student.department)

        return render(request, 'course/user_course_list.html', {
            'student': student,
            'taken_courses': taken_courses,
            'courses': courses
        })

    else:
        return render(request, 'course/user_course_list.html')
