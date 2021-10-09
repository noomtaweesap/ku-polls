"""Views for polls."""
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Choice, Question
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.utils import timezone
from django.contrib import messages


class IndexView(generic.ListView):
    """Class for display index view."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions.

        (not including those set to be published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """Class for display detail view."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Class for display results view."""

    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """Vote for selected choice.

    Arguments:
        question_id - is id of the question.
    Returns:
        If the choice is valid redirect to results page.
        If the choice is invalid render the detail page.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))


def get_queryset(self):
    """Return the last five published questions.

    (not including those set to be published in the future).
    """
    return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]


def detail(request, question_id=None):
    """View for detail page."""
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, "Voting is not allowed")
        return HttpResponseRedirect(reverse('polls:index'))
    else:
        return render(request, 'polls/detail.html', {'question': question})
