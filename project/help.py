from openaid.projects.models import Activity
from django.db.models import Q
def empties(field, lang='it'):
    return Q(**{'%s_%s__isnull' % (field, lang): True}) | Q(**{'%s_%s' % (field, lang): ''})

def build_dict(reader):
    result = {}
    for row in reader:

        number = row['projectnumber'].strip()

        if not number:
            continue

        result[number] = {
            'title': row['title'],
            'description': row['description'].strip().replace('(vuoto)', ''),
        }
    return result


def print_stats(activities=None, lang='it'):

    activity_count = activities.count()
    print 'Found %d activities' % activity_count
    empty_title_activity_count =  activities.filter(empties('title', lang=lang)).count()
    print 'Empty titles: ',  empty_title_activity_count
    empty_description_activity_count =  activities.filter(empties('description', lang=lang)).count()
    print 'Empty descriptions: ',  empty_description_activity_count


def update_titles(translations):
    activities = Activity.objects.filter(number__in=translations.keys())
    print_stats(activities)

    x = 0
    for number, item in translations.items():
        x += Activity.objects.filter(number=number).update(title_it=item['title'], description_it=item['description'])

    print 'Update %d activities' % x
    print '-' * 8
    print_stats(translations)
