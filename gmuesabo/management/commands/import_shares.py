import datetime
import re

import tablib
from django.core.exceptions import MultipleObjectsReturned

from django.core.management.base import BaseCommand
from juntagrico.entity.member import Member
from juntagrico.entity.share import Share

PAYBACK_REGEX = re.compile(r'(\d{2}).(\d{2}).(\d{2})')


class Command(BaseCommand):
    help = "Import gmuesabo shares"

    def add_arguments(self, parser):
        parser.add_argument('file', help='xlsx file to import')

        parser.add_argument(
            '-c' '--clear',
            action='store_true',
            dest='clear',
            default=False,
            help='Delete existing shares before import',
        )

        parser.add_argument(
            '-e' '--exclude-former',
            action='store_true',
            dest='exclude_former',
            default=False,
            help='Do not import paid back shares',
        )

    def handle(self, file, *args, clear=False, exclude_former=False, **options):
        with open(file, 'rb') as fh:
            imported_data = tablib.import_set(fh, skip_lines=4)

            if clear:
                count, _ = Share.objects.all().delete()
                print('cleared {} shares'.format(count))
                count, _ = Member.objects.filter(email__endswith='@juntagrico.id').delete()
                print('cleared {} members'.format(count))

            today = datetime.date.today()
            count_shares = 0
            full_name = street = zipcode = location = None
            for row in imported_data:
                if row[1] == 'vakant':
                    continue

                number = row[0]
                first_name = (row[2] or '-').strip()
                last_name = row[1].strip()
                if full_name != f'{first_name} {last_name}':
                    full_name = f'{first_name} {last_name}'
                    zipcode, _, location = (row[6] or '').partition(' ')
                    street = row[5]

                payback_date = None
                payback = str(row[10]).lower()
                if 'spende' in payback or 'ausbez' in payback:
                    result = PAYBACK_REGEX.search(payback)
                    if result:
                        if exclude_former:
                            continue
                        payback_date = datetime.date(
                            2000 + int(result.group(3)), int(result.group(2)), int(result.group(1))
                        )

                try:
                    member = Member.objects.get_or_create(first_name=first_name or '-', last_name=last_name, defaults={
                        'email': f'share{number}@juntagrico.id',
                        'addr_street': street or '?',
                        'addr_zipcode': zipcode,
                        'addr_location': location,
                        'phone': '-',
                        'mobile_phone': '-',
                        'deactivation_date': today,  # deactivate account to prevent sending emails
                    })[0]
                except MultipleObjectsReturned:
                    member = Member.objects.filter(first_name=first_name, last_name=last_name).first()

                paid_date = row[7]
                if type(paid_date) == datetime.datetime:
                    paid_date = paid_date.date()
                elif paid_date is not None:
                    try:
                        paid_date = datetime.datetime.strptime(paid_date, "%d.%m.%Y").date()
                    except ValueError:
                        paid_date = datetime.datetime.strptime(paid_date[4:].strip(), "%d.%m.%y").date()
                Share.objects.create(
                    number=number,
                    member=member,
                    paid_date=paid_date,
                    issue_date=paid_date,
                    booking_date=paid_date,
                    cancelled_date=payback_date,
                    termination_date=payback_date,
                    payback_date=payback_date,
                    notes=f'{row[3] or ""}\n{row[4] or ""}\n{row[10] or ""}'
                )
                count_shares += 1

            print('imported {} shares'.format(count_shares))
