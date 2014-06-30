from django.conf.urls import patterns, url
from .views import SubmitFAQ, SubmitFAQThanks,QuestionDetail, QuestionList

urlpatterns = patterns('',
    url(r'^$', QuestionList.as_view(), name='faq_question_list'),
    url(r'^(?P<slug>[\w-]+)$', QuestionDetail.as_view(), name='faq_question_detail'),

    # TODO: anonymous users can submit questions, that need approval from the editors
    # url(r'^submit$', SubmitFAQ.as_view(), 'faq_submit'),
    # url(r'^submit/thanks$', SubmitFAQThanks.as_view(), 'faq_submit_thanks'),
)