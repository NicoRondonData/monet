from django.db import models

from apps.students.models import Student


# Create your models here.
class Exam(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.CharField(max_length=255)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return f"{self.text} | {self.exam.name}"


class Answer(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("student", "question")

    def __str__(self):
        return f"{self.student.name} - {self.question.text} ({self.answer.text})"
