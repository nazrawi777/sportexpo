# Generated manually to preserve existing date-only countdown values as midnight datetimes.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heroslide',
            name='countdown_date',
            field=models.DateTimeField(),
        ),
    ]
