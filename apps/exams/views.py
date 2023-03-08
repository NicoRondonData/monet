from rest_framework import permissions, viewsets

from apps.exams.models import Answer, Exam, Question, StudentAnswer
from apps.exams.permissions import IsOwner, ReadOnly
from apps.exams.serializers import (
    AnswerSerializer,
    ExamSerializer,
    QuestionSerializer,
    StudentAnswerSerializer,
)


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [ReadOnly]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [ReadOnly]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [ReadOnly]


class StudentAnswerViewSet(viewsets.ModelViewSet):
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated()]
        else:
            return [IsOwner()]
