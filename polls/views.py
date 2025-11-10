from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    # template인 index.html 로 넘겨줄 argument 명을 직접 정의
    context_object_name = "lastest_question_list"

    def get_queryset(self):
        # lastest_question_list 로 전달할 value
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    # template 명은 <app_name>/<model_name>_detail.html 로 자동으로 찾음
    # 이를 회피하기 위해 명시적으로 지정
    template_name = "polls/detail.html"


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoestNotExist):
        return render(
            "polls/detail.html", {
                "question": question,
                "error_message": "You didn't select a choice",
            },
        )
    else:
        # Increase choice's db data votes by 1
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

        # redirect url -> /polls/<question.id>/results/
        return HttpResponseRedirect(
            reverse("polls:results", args=(question.id,))
        )
