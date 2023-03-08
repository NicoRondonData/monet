import uuid

from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.exams.models import Answer, Exam, Question, StudentAnswer
from apps.exams.permissions import IsOwner, ReadOnly
from apps.exams.serializers import (
    AnswerSerializer,
    DynamoDbSerializer,
    ExamSerializer,
    QuestionSerializer,
    StudentAnswerSerializer,
)
from utils.aws_dynamodb import AwsDynamodb, ServicesDynamoDb


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

    def create(self, request, *args, **kwargs):
        TABLE_NAME = "MonetDynamo"
        ddb = AwsDynamodb(parti_sql=False).client
        remote_address = request.META.get("REMOTE_ADDR")
        user_agent = request.META.get("HTTP_USER_AGENT")
        device = request.META.get("HTTP_X_DEVICE_TYPE")
        request_time = timezone.now()
        try:
            ddb.create_table(
                TableName=TABLE_NAME,
                KeySchema=[{"AttributeName": "MonetDynamoId", "KeyType": "HASH"}],
                AttributeDefinitions=[
                    {"AttributeName": "MonetDynamoId", "AttributeType": "S"}
                ],
                BillingMode="PAY_PER_REQUEST",
            )
            table = ddb.Table(TABLE_NAME)

        except ddb.meta.client.exceptions.ResourceInUseException:
            table = ddb.Table(TABLE_NAME)

        ServicesDynamoDb.insert_item_to_dynamo_db_table(
            table,
            {
                "MonetDynamoId": str(uuid.uuid4()),
                "remote_address": remote_address,
                "user_agent": user_agent,
                "device": device,
                "time": request_time.strftime("%Y-%m-%d %H:%M:%S"),
                "user_id": int(request.user.id),
            },
        )
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=["get"])
    def request_info(self, request):
        ddb = AwsDynamodb(parti_sql=False).client
        table = ddb.Table("MonetDynamo")

        result = ServicesDynamoDb.scan_table(table, "MonetDynamo")
        serializer = DynamoDbSerializer(data=result, many=True)
        if serializer.is_valid():

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
