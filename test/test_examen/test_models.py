import pytest

from apps.exams.models import Exam


@pytest.mark.django_db
def test_exam():
    exam = Exam(name="English Exam", description="This is a hard exam")
    exam.save()
    assert exam.name == "English Exam"
    assert exam.description == "This is a hard exam"
