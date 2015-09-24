from openaid.projects.models import Initiative


def run():

    for i in Initiative.objects.all():

        i.grant_amount_approved, i.loan_amount_approved = i.loan_amount_approved, i.grant_amount_approved
        i.save()