from rest_framework import serializers

from apps.exams.models import Answer, Exam, Question, StudentAnswer


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = "__all__"


class DynamoDbSerializer(serializers.Serializer):
    MonetDynamoId = serializers.CharField()
    remote_address = serializers.IPAddressField(
        required=False,
    )
    time = serializers.DateTimeField(
        required=False,
    )
    device = serializers.CharField(required=False, allow_null=True)
    user_id = serializers.IntegerField(
        required=False,
    )
    user_agent = serializers.CharField(
        required=False,
    )
