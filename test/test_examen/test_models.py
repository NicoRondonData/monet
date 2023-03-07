import pytest

from apps.exams.models import Answer, Exam, Question


@pytest.mark.django_db
def test_exam():
    exam = Exam(name="English Exam", description="This is a hard exam")
    exam.save()
    assert exam.name == "English Exam"
    assert exam.description == "This is a hard exam"


@pytest.mark.django_db
def test_question():
    exam = Exam(name="English Exam", description="This is a hard exam")
    exam.save()
    question = Question.objects.create(text="Primera pregunta", exam_id=exam.id)
    assert question.text == "Primera pregunta"
    assert question.exam_id == exam.id


@pytest.mark.django_db
def test_answer():
    exam = Exam(name="English Exam", description="This is a hard exam")
    exam.save()
    question = Question.objects.create(text="Primera pregunta", exam_id=exam.id)
    answer = Answer.objects.create(text="1", question_id=question.id, is_correct=True)
    assert answer.is_correct is True
