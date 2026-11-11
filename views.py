from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Enrollment, Question, Choice, Submission

def submit(request, course_id):
    """
    Creates a Submission linked to the learner's Enrollment in the course,
    saves all selected choices, and redirects to the result view.
    """
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
    # Get the enrollment for the current user and course
    enrollment = Enrollment.objects.get(user=user, course=course)

    # Create a new submission linked to this enrollment
    submission = Submission.objects.create(enrollment=enrollment)

    # Collect all selected choice IDs from the POST request
    selected_choice_ids = []
    for key, value in request.POST.items():
        if key.startswith('choice_') or key.isdigit():
            selected_choice_ids.append(value)

    # Get the choice objects and add them to the submission (ManyToMany)
    selected_choices = Choice.objects.filter(id__in=selected_choice_ids)
    submission.choices.set(selected_choices)

    # Redirect to the result view with course_id and submission_id
    return HttpResponseRedirect(
        reverse('show_exam_result', args=(course_id, submission.id))
    )

def show_exam_result(request, course_id, submission_id):
    """
    Retrieves the specific submission, calculates the score per question,
    and passes the selected choice IDs to the template.
    """
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, id=submission_id)

    # Get all choices selected in this submission
    selected_choices = submission.choices.all()
    # Extract the selected choice IDs for the template
    selected_ids = selected_choices.values_list('id', flat=True)

    # Calculate score per question
    total_score = 0
    for choice in selected_choices:
        if choice.is_correct:
            total_score += choice.question.grade

    context = {
        'course': course,
        'submission': submission,
        'selected_ids': selected_ids,   # Pass selected choice IDs to template
        'grade': total_score,           # Score calculated per question
        'choices': selected_choices,
    }
    return render(request, 'exam_result_bootstrap.html', context)
