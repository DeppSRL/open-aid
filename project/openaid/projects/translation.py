from modeltranslation.translator import translator, TranslationOptions
from . import models


class ProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'description', )

translator.register(models.Project, ProjectTranslationOptions)


class ActivityTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'long_description', )

translator.register(models.Activity, ActivityTranslationOptions)


class ReportTranslationOptions(TranslationOptions):
    fields = ('description', )

translator.register(models.Report, ReportTranslationOptions)


class ProblemTranslationOptions(TranslationOptions):
    fields = ('event', 'impact', 'actions')

translator.register(models.Problem, ProblemTranslationOptions)


class NewProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'description', )

translator.register(models.NewProject, NewProjectTranslationOptions)

