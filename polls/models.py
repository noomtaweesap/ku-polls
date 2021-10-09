"""Create models for polls."""
import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Create question model.

    Args:
        models : Question details (question_text, pub_date, end_date)
    """

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('Expiration date', null=True)

    def __str__(self):
        """Return the question text.

        Returns:
            string : question text
        """
        return self.question_text

    def was_published_recently(self):
        """Return true when the question was published recently.

        Returns:
            bool : true if the question was published recently.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def is_published(self):
        """Return true if question is published.

        Returns:
              bool : true if the question is published.
        """
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """Return true if polls still in period.

        Returns:
            bool : true if polls still in period
        """
        now = timezone.now()
        return self.end_date >= now >= self.pub_date


class Choice(models.Model):
    """Create choice model.

    Args:
        models : Choice details (question, choice_text, votes)
    """

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return the choice text.

        Returns:
            string : the choice text
        """
        return self.choice_text
