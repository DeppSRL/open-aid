from modeltranslation.translator import translator, TranslationOptions
from .models import Question

__author__ = 'guglielmo'

class QuestionTranslationOptions(TranslationOptions):
    fields = ('text', 'answer', )

translator.register(Question, QuestionTranslationOptions)
