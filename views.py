from django.shortcuts import get_object_or_404, render, redirect
from .models import Question, Choice, Submission

def submit(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('choice_') or key.isdigit():
                try:
                    choice = Choice.objects.get(pk=value)
                    Submission.objects.create(question=choice.question, selected_choice=choice)
                except Choice.DoesNotExist:
                    continue
        return redirect('show_exam_result')
    return redirect('home')

def show_exam_result(request):
    submissions = Submission.objects.all().order_by('-submitted_at')
    total_questions = Question.objects.count()
    correct_answers = sum(1 for sub in submissions if sub.selected_choice.is_correct)
    context = {
        'submissions': submissions,
        'correct_answers': correct_answers,
        'total_questions': total_questions,
    }
    return render(request, 'exam_result.html', context)
