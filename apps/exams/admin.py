from django.contrib import admin

from .models import Answer, Exam, Question, StudentAnswer

# Register your models here.

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(StudentAnswer)
