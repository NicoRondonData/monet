from django.contrib import admin

from .models import Answer, Exam, Question, StudentAnswer


class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ("student", "question", "get_selected_answer", "exam")
    list_filter = ["student", "exam__name"]
    search_fields = ["student__name"]

    def get_selected_answer(self, obj):
        return obj.answer.text

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.is_authenticated:
            return qs.filter(student=request.user)
        else:
            return qs.none()

    get_selected_answer.short_description = "Selected Answer"


admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(StudentAnswer, StudentAnswerAdmin)
