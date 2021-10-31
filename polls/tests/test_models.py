import datetime

from django.test import TestCase
from django.utils import timezone
from ..models import Question
from django.urls import reverse


def create_question(question_text, days):
    """
    Create a question.

    with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    """Test question models."""

    def test_was_published_recently_with_future_question(self):
        """Check was_published_recently() function.

        Returns False for questions whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Check was_published_recently() function.

        Returns False for questions whose pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Check was_published_recently() function.

        Returns True for questions whose pub_date is within the last day.
        """
        time = timezone.now() -\
            datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """Check is_published() function.

        Returns False for questions whose pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(hours=24)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_old_question(self):
        """
        Check is_published() function.

        Returns True for questions whose pub_date is older than 1 day.

        """
        time = timezone.now() - datetime.timedelta(days=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.is_published(), True)

    def test_can_vote_with_expired_question(self):
        """can_vote() returns False if the question is expired."""
        pub_date = timezone.now() - datetime.timedelta(days=10)
        end_date = timezone.now() - datetime.timedelta(seconds=1)
        expired_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(expired_question.can_vote(), False)

    def test_can_vote_with_future_question(self):
        """can_vote() returns False if the question is not published yet."""
        pub_date = timezone.now() + datetime.timedelta(days=10)
        end_date = timezone.now() + datetime.timedelta(days=20)
        future_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(future_question.can_vote(), False)
