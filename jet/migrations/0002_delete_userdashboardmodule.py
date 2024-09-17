from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("jet", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="UserDashboardModule",
        ),
    ]
