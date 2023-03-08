from rest_framework.routers import DefaultRouter

from apps.exams.views import (
    AnswerViewSet,
    ExamViewSet,
    QuestionViewSet,
    StudentAnswerViewSet,
)

router = DefaultRouter()

router.register("exams", ExamViewSet)
router.register("questions", QuestionViewSet)
router.register("answers", AnswerViewSet)
router.register("student_answers", StudentAnswerViewSet)

urlpatterns = [] + router.urls
