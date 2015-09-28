# coding=utf-8
import logging
from pprint import pprint
from datetime import datetime
from django.core.management.base import BaseCommand
from openaid.projects.models import Activity


class Command(BaseCommand):

    help = 'Fixes activity dates removing Hours and minutes, fixing timezone'
    logger = logging.getLogger('openaid')

    def set_hour_minute_to_zero(self, date):
        if date is None:
            return date
        return date.replace(hour=0,minute=0)


    def handle(self, *args, **options):

        # loop over activity, fix hour and minute

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
        self.logger.info("Finished ")
