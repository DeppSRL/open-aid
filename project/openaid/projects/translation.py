from modeltranslation.translator import translator, TranslationOptions
from . import models


class InitiativeTranslationOptions(TranslationOptions):
    fields = ('title', 'description_temp', 'outcome_temp', 'beneficiaries_temp', 'other_financiers_temp',
              'counterpart_authority_temp', 'location_temp' )


class ProjectTranslationOptions(TranslationOptions):
    fields = (
        'title', 'description', 'outcome', 'beneficiaries', 'other_financiers', 'counterpart_authority', 'location')


class ActivityTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'long_description', )


class ReportTranslationOptions(TranslationOptions):
    fields = ('description', )


class ProblemTranslationOptions(TranslationOptions):
    fields = ('event', 'impact', 'actions')


class NewProjectTranslationOptions(TranslationOptions):
    fields = ('title', 'description', )


translator.register(models.Initiative, InitiativeTranslationOptions)
translator.register(models.Project, ProjectTranslationOptions)
translator.register(models.Activity, ActivityTranslationOptions)
translator.register(models.Report, ReportTranslationOptions)
translator.register(models.Problem, ProblemTranslationOptions)
translator.register(models.NewProject, NewProjectTranslationOptions)