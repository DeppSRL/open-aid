# coding=utf-8
from __future__ import unicode_literals
import csvkit
from django.db import IntegrityError, transaction
from django.db.models import Count
from openaid.codelists.models import Agency
from openaid.projects.models import Project, Activity
from collections import Counter


__author__ = 'joke2k'


def update_crsids(filename):
    for row in csvkit.DictReader(open(filename)):
        #print row
        activity_id = row['openaid_id']
        old_crsid = row['crsid']
        new_crsid = row['crsid OK']
        project_number = row.get('projectnumber OK', None)

        updates_markers = False

        try:
            activity = Activity.objects.get(pk=activity_id)
        except Activity.DoesNotExist:
            print '- Impossibile trovare Activity.pk = %s' % activity_id
            continue

        # if activity.crsid != old_crsid:
        #     raise Exception('oldCRSID:%s non corrispondente per questa Activity %s' % (old_crsid, repr(activity)))

        # if activity.agency.code != '4':
        #     raise Exception('Activity %s ha una Agency sbagliata %s' % (repr(activity), activity.agency))

        try:

            new_project = Project.objects.get(crsid=new_crsid, recipient__code=activity.recipient.code)

            try:
                conclict_activity = new_project.activity_set.get(year=activity.year)

                if conclict_activity == activity:
                    continue

                _, updates_markers = conclict_activity.merge(activity, save=False)
                activity, conclict_activity = conclict_activity, activity
                print '- Cancello %s dopo il merge in %s' % (repr(conclict_activity), repr(activity))
                conclict_activity.delete()

            except Activity.DoesNotExist:
                pass

        except Project.DoesNotExist:

            new_project = Project.objects.create(
                crsid=new_crsid,
                recipient=activity.recipient,
                start_year=activity.year,
                end_year=activity.year,
            )

            print ('- Nuovo progetto per Activity %s non trovato con newCRSID:%s' % (
                repr(activity), new_crsid))

        finally:
            activity.crsid = new_crsid
            activity.project = new_project
            if updates_markers:
                activity.markers.save()
            if project_number and activity.number != project_number:
                activity.number = project_number
            activity.save()

            new_project.update_from_activities(save=True)

            #print '- %s aggiornata' % repr(activity)



    # cancello tutti i progetti senza Activity
    qs = Project.objects.annotate(activities=Count('activity')).filter(activities=0)
    print 'Cancello %s Project senza Activity' % (
        qs.count(),
    )
    qs.delete()


def test_csv_row(row):
    problemi = []

    activity = Activity.objects.get(pk=row['openaid_id'], year=row['Year'], crsid=row['crsid'])

    try:
        project = Project.objects.get(
            crsid=row['Crsid def'],
            agency__code='4',
            recipient__code=activity.recipient.code
        )
    except Project.DoesNotExist:
        problemi.append({
            'type': 'new_project',
            'msg': 'Progetto con il CRSID %s e Recipient %s non trovato' % (row['Crsid def'], activity.recipient)
        })
        return problemi

    for project_activity in project.activity_set.filter(year=activity.year):
        if project_activity == activity:
            problemi.append({
                'type': 'duplicate',
                'msg': 'Activity ripetuta %s' % activity
            })
        else:
            problemi.append({
                'type': 'activity_conflict',
                'msg': 'Activity (%s) ha lo stesso anno di %s nel progetto %s' % (
                    activity.__repr__(), project_activity.__repr__(), project.__repr__()
                )
            })

    if activity.project.activity_set.count() == 1:
        problemi.append({
            'type': 'delete_project',
            'msg': 'Project %s non ha piu Activity dopo lo spostamento' % (activity.project.__repr__())
        })

    return problemi


def test_csv(filename):

    stats = Counter()

    for ix, row in enumerate(csvkit.DictReader(open(filename))):
        if row['crsid OK'] == '' or row['crsid'] == row['Crsid def']:
            continue

        problems = test_csv_row(row)
        if len(problems) == 0:
            stats.update(['ok'])
            continue
        stats.update([p['type'] for p in problems])
        if any([p for p in problems if p['type'] in ['duplicate', 'activity_conflict']]):
            print '%d] %s' % (ix, ' | '.join([p['msg'] for p in problems]))




def run(filename='crs_changes.csv'):

    update_crsids(filename)

    # try:
    #     # test_csv(filename)
    #     #with transaction.atomic():
    #     update_crsids(filename)
    # except Exception, e:
    #     print 'DryRun %s' % e


    # for row in csvkit.DictReader(open('crs_changes.csv')):
    #
    #     activity_id = row['openaid_id']
    #     old_crsid = row['crsid']
    #     new_crsid = row['crsid OK']
    #     year = row['Year']
    #
    #     try:
    #         activity = Activity.objects.get(pk=activity_id)
    #
    #         if activity.crsid != old_crsid:
    #             raise Exception('oldCRSID:%s non corrispondente per questa Activity %s' % (old_crsid, activity))
    #
    #     except Activity.DoesNotExist:
    #         raise Exception('Impossibile trovare Activity.pk = %s' % activity_id)


        #
        # for project in Project.objects.filter(crsid=old_crsid):
        #     new_project = Project.objects.filter(crsid=new_crsid)
        #
        # else:
        #     pass
        #
        #
        # p = Project.objects.filter(crsid=old_crsid).update(
        #     crsid=new_crsid
        # )
        # print '%d project updated' % p
        #
        # a = Activity.objects.filter(crsid=old_crsid).update(
        #     crsid=new_crsid
        # )
        # print '%d activities updated' % a