import datetime

import tablib

from django.core.management.base import BaseCommand
from juntagrico.entity.depot import Depot
from juntagrico.entity.location import Location
from juntagrico.entity.member import Member, SubscriptionMembership
from juntagrico.entity.subs import Subscription, SubscriptionPart
from juntagrico.entity.subtypes import SubscriptionType, SubscriptionBundle


class Command(BaseCommand):
    help = "Import gmuesabo data"

    def add_arguments(self, parser):
        parser.add_argument('file', help='xlsx file to import')

        parser.add_argument(
            '-c' '--clear',
            action='store_true',
            dest='clear',
            default=False,
            help='Delete existing data before import',
        )

    def handle(self, file, *args, clear=False, **options):
        with open(file, 'rb') as fh:
            imported_data = tablib.Dataset().load(fh)

            if clear:
                count, _ = Subscription.objects.all().delete()
                print('cleared {} subscriptions'.format(count))
                count, _ = Member.objects.filter(user__is_staff=False).delete()
                print('cleared {} members'.format(count))

            sub_types = {
                sub_type.name: sub_type
                for sub_type in SubscriptionType.objects.all()
            }
            print(sub_types)

            depots = {
                depot.name: depot
                for depot in Depot.objects.all()
            }

            count_members = 0
            count_subscription = 0
            for row in imported_data:
                if row[8] is None:
                    break
                if row[8] == 'none@none.ch':
                    print('skipping {}'.format(row[:2]))
                    continue

                notes = ''
                if row[10] is None and row[9] is not None:
                    # store second email address without name
                    notes += "2. E-Mail-Adresse: " + row[9]
                if row[12] is not None:
                    notes += "\n# Bemerkungen Profil\n" + row[12]
                if row[20] is not None:
                    notes += "\n# AbonnentIn seit\n" + str(row[20])
                if row[21] is not None:
                    notes += "\n# Eintritt (Grund, Weg)\n" + row[21]
                if row[22] is not None:
                    notes += "\n# Grund Austritt\n" + row[22]
                if row[38] is not None:
                    notes += "\n# Genossenschaftsbeitritt via\n" + row[38]
                if row[41] is not None:
                    notes += "\n# Bemerkungen Gnossi\n" + row[41]
                member = Member.objects.create(
                    last_name=row[0],
                    first_name=row[1],
                    addr_street=row[3] + ' ' + str(row[2]),
                    addr_zipcode=row[4],
                    addr_location=row[5],
                    phone=row[6] or row[7] or '-',
                    mobile_phone=row[7],
                    email=row[8],
                    notes=notes
                )
                count_members += 1

                # add co-members
                co_member = None
                if row[9] is not None and row[10] is not None and row[11] is not None:
                    if row[9] == member.email:
                        print('skipping duplicate email {}'.format(row[9]))
                    else:
                        co_member = Member.objects.create(
                            email=row[9],
                            last_name=row[10],
                            first_name=row[11],
                            addr_street=row[3] + ' ' + str(row[2]),
                            addr_zipcode=row[4],
                            addr_location=row[5],
                            phone='-',
                            mobile_phone='-',
                        )
                        count_members += 1

                # create subscription
                subscription = None
                if row[17] in ['Aktiv', 'Schnupperabo']:
                    sub_type_name = row[15]
                    is_trial = row[17] == 'Schnupperabo'
                    if is_trial:
                        sub_type_name += ' schnupper'

                    if sub_type_name not in sub_types:
                        sub_types[sub_type_name] = SubscriptionType.objects.create(
                            name=sub_type_name,
                            bundle=SubscriptionBundle.objects.get_or_create(long_name='Platzhalter')[0],
                            required_assignments=12,
                            price=0,
                            trial_days=84 if is_trial else 0,
                        )

                    depot_name = row[16]
                    if depot_name not in depots:
                        depots[depot_name] = Depot.objects.create(
                            name=depot_name,
                            weekday=4,
                            location=Location.objects.get_or_create(name='Platzhalter')[0],
                            access_information='-',
                        )

                    start_date = row[18]
                    if start_date is None:
                        print('undefined subscription start date.')
                        continue
                    else:
                        start_date = datetime.datetime.strptime(start_date, "%d.%m.%Y").date()

                    notes = ''
                    if row[24] is not None:
                        notes += "\n# Bem. Zusatzabo Eier\n" + row[24]
                    if row[26] is not None:
                        notes += "\n# Zahlung / Buchungstexte\n" + row[26]
                    if row[36] is not None:
                        notes += "\n# Bemerkungen Finanzen\n" + row[36]
                    subscription = Subscription.objects.create(
                        depot=depots[depot_name],
                        nickname=str(row[13]) + ' - ' + row[14],
                        start_date=start_date,
                        activation_date=start_date,
                        notes=notes,
                    )
                    SubscriptionMembership.objects.create(
                        member=member,
                        subscription=subscription,
                        join_date=start_date,
                    )
                    subscription.primary_member = member
                    subscription.save()
                    if co_member is not None:
                        SubscriptionMembership.objects.create(
                            member=co_member,
                            subscription=subscription,
                            join_date=start_date,  # assuming joined on same date
                        )
                    SubscriptionPart.objects.create(
                        subscription=subscription,
                        type=sub_types[sub_type_name],
                        activation_date=start_date,
                    )

                    # extra sub
                    if row[23] is not None and 'eier' in sub_types:
                        week = row[23]
                        if week == 1:
                            date = datetime.date(2026, 1, 1)
                        else:
                            date = datetime.datetime.strptime(f'2026-W{week}-1', "%Y-W%W-%w").date()
                        SubscriptionPart.objects.create(
                            subscription=subscription,
                            type=sub_types['eier'],
                            activation_date=date,
                        )
                    count_subscription += 1

            print('imported {} members and {} subscriptions'.format(count_members, count_subscription))
