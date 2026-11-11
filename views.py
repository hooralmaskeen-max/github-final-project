from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Enrollment, Question, Choice, Submission

def submit(request, course_id):
    """
    Creates a Submission for the learner's enrollment in the course,
    and saves all selected choices.
    """
    course = get_object_or_404(Course, pk=course_id)
    user = request.user
 
    enrollment = Enrollment.objects.get(user=user, course=course)
    

    submission = Submission.objects.create(enrollment=enrollment)
    
  
    selected_choice_ids = []
    for key, value in request.POST.items():
        if key.startswith('choice_') or key.isdigit():
            selected_choice_ids.append(value)
  
    selected_choices = Choice.objects.filter(id__in=selected_choice_ids)
    submission.choices.set(selected_choices)
    
 
    return HttpResponseRedirect(
        reverse('show_exam_result', args=(course_id, submission.id))
    )

def show_exam_result(request, course_id, submission_id):
    """
    Retrieves the specific submission and calculates the score
    based on the correct choices selected.
    """
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, id=submission_id)
    
 
    choices = submission.choices.all()
    
    total_score = 0
    for choice in choices:
        if choice.is_correct:
           
            total_score += choice.question.grade
            
    context = {
        'course': course,
        'grade': total_score,
        'choices': choices,
    }
    return render(request, 'exam_result_bootstrap.html', context)
