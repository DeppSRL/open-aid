import csvkit


def run():
    from openaid.projects.models import Initiative, Project
    for i, row in enumerate(csvkit.DictReader(open('initiatives.csv')), start=1):

        initiative, created = Initiative.objects.get_or_create(
            code=row['code'].zfill(6),
            defaults={
                'title_it': row['title'],
                'country': row['country'] if row['country'] != '(vuoto)' else '',
            }
        )

        projects = 0

        if created:
            projects = Project.objects.filter(number__startswith=initiative.code).update(initiative=initiative)

        print '%d] Created %s%s' % (i, repr(initiative), (' associated with %d projects' % projects) if projects else '')