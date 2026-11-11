from django.db import models

class Question(models.Model):
    text = models.TextField(verbose_name="نص السؤال")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    def __str__(self):
        return self.text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices', verbose_name="السؤال")
    text = models.CharField(max_length=255, verbose_name="نص الخيار")
    is_correct = models.BooleanField(default=False, verbose_name="هل الخيار صحيح؟")

    def __str__(self):
        return f"{self.text} ({'صحيح' if self.is_correct else 'خطأ'})"

class Submission(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="السؤال")
    selected_choice = models.ForeignKey(Choice, on_delete=models.CASCADE, verbose_name="الخيار المُختار")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="وقت الإرسال")

    def __str__(self):
        return f"إجابة على السؤال: {self.question.text[:30]}"
