import re

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from quizapp.mixins import TitleMixin, AuthorizedOnlyDispatchMixin
from quizapp.models import QuestionSet, Question


class MainPageView(ListView, TitleMixin):
    """View for the sets of tests page."""
    model = QuestionSet
    template_name = 'index.html'
    title = 'Наборы тестов'

    def get_queryset(self):
        """
        Returns a queryset of test question sets marked as active
        and containing at least 1 question.
        When the user gets to the main page, the session context is deleted
        (incomplete or interrupted tests are forcibly terminated).
        """
        if 'context' in self.request.session:
            del self.request.session['context']
        return QuestionSet.objects.filter(is_active=True).exclude(questions__isnull=True)


class TestProcessView(DetailView, AuthorizedOnlyDispatchMixin):
    """View for consistently get the current question from the set and its possible answers.
    """
    model = QuestionSet
    template_name = 'test_body.html'

    def get(self, request, *args, **kwargs):
        """
        Forms the starting context with the initial data.
        Stores it in the session for the current user.
        Retrieves test progress data from the session when switching
        to a new question and updates stored data.
        """
        if 'context' not in request.session:
            question_set = get_object_or_404(QuestionSet, slug=self.kwargs.get('slug'))
            id_list = [question.id for question in question_set.questions.all()]
            context = {
                'title': f'{question_set.title}',
                'counter': 0,
                'quantity': len(id_list),
                'right_ans': 0,
                'wrong_ans': 0,
                'percent_right': 0,
                'question_set_slug': question_set.slug,
            }
            request.session['context'] = context

        else:
            context = request.session['context']
            id_list = context['question_set']

        if len(id_list) > 0:
            request.session['context']['question_set'] = id_list
            request.session['context']['counter'] += 1
            request.session.modified = True
            context_current = context.copy()
            context_current['current_question'] = Question.objects.get(id=id_list.pop())
            return render(request, 'test_body.html', context=context_current)
        else:
            del request.session['context']
            context['current_question'] = 'Stop'
            return render(request, 'test_body.html', context=context)


class AnswerQuestion(DetailView, AuthorizedOnlyDispatchMixin):
    """View to check the correctness of the answer and the number
    of his correct and incorrect answers stored in the session."""
    model = Question
    template_name = 'answers.html'

    def get(self, request, guessed=False, *args, **kwargs):
        """Checks the correctness of this answer and the number of his correct and
        incorrect answers stored in the session.

        Args:

            * request: standard parameter.
            * guessed(bool): information about whether the question has been guessed;
            * ``*args``: standard parameter.
            * ``**kwargs``: standard parameter.

        """
        chosen_answers = list(request.GET.values())[1:]

        question = Question.objects.get(id=kwargs['question_id'])
        right_answers_numbers = re.findall(r'\d+', question.right_answers)
        right_answers_numbers = [int(item) for item in right_answers_numbers]

        answers_map = {
            1: question.answer_01,
            2: question.answer_02,
            3: question.answer_03,
            4: question.answer_04,
        }

        chosen_answers_numbers = [key for key, value in answers_map.items() if value in chosen_answers]
        right_answers_text = [value for key, value in answers_map.items() if key in right_answers_numbers]

        right_answers_numbers.sort()
        chosen_answers_numbers.sort()

        if right_answers_numbers == chosen_answers_numbers:
            guessed = True
            request.session['context']['right_ans'] += 1

            quantity = request.session['context']['quantity']
            right_ans = request.session['context']['right_ans']
            request.session['context']['percent_right'] = 100 / quantity * right_ans
        else:
            request.session['context']['wrong_ans'] += 1
        request.session.modified = True
        context = {
            'title': f'Ответ на вопрос {question.text}',
            'question_set_title': request.session['context']['title'],
            'current_question': question,
            'chosen_answers': chosen_answers,
            'right_answers': right_answers_text,
            'guessed': guessed,
            'question_set_slug': request.session['context']['question_set_slug'],
        }
        return render(request, 'answers.html', context)
