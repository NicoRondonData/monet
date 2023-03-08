from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.exams.models import StudentAnswer


@login_required
def my_answers(request):
    student_answers = StudentAnswer.objects.filter(student__user=request.user)
    context = {"student_answers": student_answers}
    return render(request, "my_answers.html", context)
