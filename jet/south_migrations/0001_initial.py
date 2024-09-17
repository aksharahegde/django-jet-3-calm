from south.db import db
from south.utils import datetime_utils as datetime
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Bookmark'
        db.create_table(
            "jet_bookmark",
            (
                ("id", self.gf("django.db.models.fields.AutoField")(primary_key=True)),
                ("url", self.gf("django.db.models.fields.URLField")(max_length=200)),
                ("title", self.gf("django.db.models.fields.CharField")(max_length=255)),
                ("user", self.gf("django.db.models.fields.PositiveIntegerField")()),
                (
                    "date_add",
                    self.gf("django.db.models.fields.DateTimeField")(
                        default=datetime.datetime.now
                    ),
                ),
            ),
        )
        db.send_create_signal("jet", ["Bookmark"])

        # Adding model 'PinnedApplication'
        db.create_table(
            "jet_pinnedapplication",
            (
                ("id", self.gf("django.db.models.fields.AutoField")(primary_key=True)),
                (
                    "app_label",
                    self.gf("django.db.models.fields.CharField")(max_length=255),
                ),
                ("user", self.gf("django.db.models.fields.PositiveIntegerField")()),
                (
                    "date_add",
                    self.gf("django.db.models.fields.DateTimeField")(
                        default=datetime.datetime.now
                    ),
                ),
            ),
        )
        db.send_create_signal("jet", ["PinnedApplication"])

        # Adding model 'UserDashboardModule'
        db.create_table(
            "jet_userdashboardmodule",
            (
                ("id", self.gf("django.db.models.fields.AutoField")(primary_key=True)),
                ("title", self.gf("django.db.models.fields.CharField")(max_length=255)),
                (
                    "module",
                    self.gf("django.db.models.fields.CharField")(max_length=255),
                ),
                (
                    "app_label",
                    self.gf("django.db.models.fields.CharField")(
                        max_length=255, null=True, blank=True
                    ),
                ),
                ("user", self.gf("django.db.models.fields.PositiveIntegerField")()),
                ("column", self.gf("django.db.models.fields.PositiveIntegerField")()),
                ("order", self.gf("django.db.models.fields.IntegerField")()),
                (
                    "settings",
                    self.gf("django.db.models.fields.TextField")(
                        default="", blank=True
                    ),
                ),
                (
                    "children",
                    self.gf("django.db.models.fields.TextField")(
                        default="", blank=True
                    ),
                ),
                (
                    "collapsed",
                    self.gf("django.db.models.fields.BooleanField")(default=False),
                ),
            ),
        )
        db.send_create_signal("jet", ["UserDashboardModule"])

    def backwards(self, orm):
        # Deleting model 'Bookmark'
        db.delete_table("jet_bookmark")

        # Deleting model 'PinnedApplication'
        db.delete_table("jet_pinnedapplication")

        # Deleting model 'UserDashboardModule'
        db.delete_table("jet_userdashboardmodule")

    models = {
        "jet.bookmark": {
            "Meta": {"ordering": "('date_add',)", "object_name": "Bookmark"},
            "date_add": (
                "django.db.models.fields.DateTimeField",
                [],
                {"default": "datetime.datetime.now"},
            ),
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "title": ("django.db.models.fields.CharField", [], {"max_length": "255"}),
            "url": ("django.db.models.fields.URLField", [], {"max_length": "200"}),
            "user": ("django.db.models.fields.PositiveIntegerField", [], {}),
        },
        "jet.pinnedapplication": {
            "Meta": {"ordering": "('date_add',)", "object_name": "PinnedApplication"},
            "app_label": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "255"},
            ),
            "date_add": (
                "django.db.models.fields.DateTimeField",
                [],
                {"default": "datetime.datetime.now"},
            ),
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "user": ("django.db.models.fields.PositiveIntegerField", [], {}),
        },
        "jet.userdashboardmodule": {
            "Meta": {
                "ordering": "('column', 'order')",
                "object_name": "UserDashboardModule",
            },
            "app_label": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "255", "null": "True", "blank": "True"},
            ),
            "children": (
                "django.db.models.fields.TextField",
                [],
                {"default": "''", "blank": "True"},
            ),
            "collapsed": (
                "django.db.models.fields.BooleanField",
                [],
                {"default": "False"},
            ),
            "column": ("django.db.models.fields.PositiveIntegerField", [], {}),
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "module": ("django.db.models.fields.CharField", [], {"max_length": "255"}),
            "order": ("django.db.models.fields.IntegerField", [], {}),
            "settings": (
                "django.db.models.fields.TextField",
                [],
                {"default": "''", "blank": "True"},
            ),
            "title": ("django.db.models.fields.CharField", [], {"max_length": "255"}),
            "user": ("django.db.models.fields.PositiveIntegerField", [], {}),
        },
    }

    complete_apps = ["jet"]
