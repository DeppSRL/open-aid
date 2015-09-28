# coding=utf-8
from datetime import datetime
import logging
from django.core.management.base import BaseCommand
from openaid.projects.models import Activity


class Command(BaseCommand):

    help = 'Fixes activity dates removing Hours and minutes'
    logger = logging.getLogger('openaid')

    def set_hour_minute_to_zero(self, date):
        if date is None:
            return date
        return date.replace(hour=0,minute=0)

    def check_invalid_date(self, date):
        if date is None:
            return date

        import pytz
        treshold_date = datetime(1970, 1, 1).replace(tzinfo = pytz.utc)
        if date <= treshold_date:
            return None
        else:
            return date


    def handle(self, *args, **options):
        verbosity = options['verbosity']
        if verbosity == '0':
            self.logger.setLevel(logging.ERROR)
        elif verbosity == '1':
            self.logger.setLevel(logging.WARNING)
        elif verbosity == '2':
            self.logger.setLevel(logging.INFO)
        elif verbosity == '3':
            self.logger.setLevel(logging.DEBUG)


        # loop over activity, fix hour and minute setting hour to 00:00
        # then check if the date is valid: if date < 1.1.1970 set date to null

        all_activities = Activity.objects.all().order_by('year')
        for act in all_activities:
            # fix hour minute for
            # expected_start_date
            # completion_date
            # commitment_date
            act.expected_start_date = self.set_hour_minute_to_zero(act.expected_start_date)
            act.completion_date = self.set_hour_minute_to_zero(act.completion_date)
            act.commitment_date = self.set_hour_minute_to_zero(act.commitment_date)
            act.save()
            act.expected_start_date = self.check_invalid_date(act.expected_start_date)
            act.completion_date = self.check_invalid_date(act.completion_date)
            act.commitment_date = self.check_invalid_date(act.commitment_date)
            act.save()
        self.logger.info("Finished ")
