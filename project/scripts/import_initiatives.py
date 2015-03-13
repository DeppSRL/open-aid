import csvkit


def run():
    from openaid.projects.models import Initiative
    initiatives = []
    for row in csvkit.DictReader(open('initiatives.csv')):
        initiatives.append(
            Initiative(
                code=row['code'].zfill(6),
                title_it=row['title'],
                country=row['country'] if row['country'] != '(vuoto)' else ''
            )
        )
        print 'Created %s' % initiatives[-1]
    Initiative.objects.bulk_create(initiatives)