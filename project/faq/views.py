from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, CreateView, TemplateView, ListView
from faq.forms import SubmitFAQForm
from faq.models import Question
from django.utils.translation import ugettext_lazy as _

class QuestionList(ListView):
    model = Question
    template_name = "question_list.html"
    allow_empty = True
    context_object_name = "questions"

    def get_queryset(self):
        return Question.objects.active()


class QuestionDetail(DetailView):
    queryset = Question.objects.active()
    template_name = "question_detail.html"

    def get_queryset(self):
        # Careful here not to hardcode a base queryset. This lets
        # subclassing users re-use this view on a subset of questions, or
        # even on a new model.
        # FIXME: similar logic as above. This should push down into managers.
        qs = super(QuestionDetail, self).get_queryset()
        if self.request.user.is_anonymous():
            qs = qs.exclude(protected=True)

        return qs

class SubmitFAQ(CreateView):
    model = Question
    form_class = SubmitFAQForm
    template_name = "submit_question.html"
    success_view_name = "faq_submit_thanks"

    def get_form_kwargs(self):
        kwargs = super(SubmitFAQ, self).get_form_kwargs()
        kwargs['instance'] = Question()
        if self.request.user.is_authenticated():
            kwargs['instance'].created_by = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super(SubmitFAQ, self).form_valid(form)
        messages.success(self.request,
            _("Your question was submitted and will be reviewed by for inclusion in the FAQ."),
            fail_silently=True,
        )
        return response

    def get_success_url(self):
        # The superclass version raises ImproperlyConfigered if self.success_url
        # isn't set. Instead of that, we'll try to redirect to a named view.
        if self.success_url:
            return self.success_url
        else:
            return reverse(self.success_view_name)

class SubmitFAQThanks(TemplateView):
    template_name = "submit_thanks.html"