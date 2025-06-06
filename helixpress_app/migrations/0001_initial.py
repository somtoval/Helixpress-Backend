# Generated by Django 5.1.4 on 2025-04-03 18:12

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HomeSlider",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("title", models.CharField(max_length=200, null=True)),
                ("body", models.TextField(null=True)),
                ("pic", models.ImageField(upload_to="")),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Journal",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=200, null=True)),
                ("about", models.CharField(blank=True, max_length=20000, null=True)),
                ("abbrv", models.CharField(blank=True, max_length=200, null=True)),
                ("impact", models.CharField(blank=True, max_length=200, null=True)),
                ("pic", models.ImageField(upload_to="journals_pics/")),
                ("issn", models.CharField(blank=True, max_length=200, null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                ("aim_scope", models.TextField(blank=True, null=True)),
                ("reviewer_board", models.TextField(blank=True, null=True)),
                ("author_instructions", models.TextField(blank=True, null=True)),
                ("article_processing_charge", models.TextField(blank=True, null=True)),
                ("indexing_and_archiving", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("name", models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name="Issue",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("number", models.IntegerField(null=True)),
                ("special", models.BooleanField(default=False)),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "journal",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="helixpress_app.journal",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Newsletter",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("email", models.EmailField(max_length=200, null=True)),
                (
                    "journal",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="helixpress_app.journal",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="journal",
            name="subject",
            field=models.ManyToManyField(
                blank=True, related_name="journals", to="helixpress_app.subject"
            ),
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("firstname", models.CharField(max_length=200, null=True)),
                ("lastname", models.CharField(max_length=200, null=True)),
                ("email", models.EmailField(max_length=200, null=True)),
                ("phonenumber", models.CharField(max_length=200, null=True)),
                ("institution", models.CharField(max_length=200, null=True)),
                ("country", models.CharField(max_length=200, null=True)),
                (
                    "manuscript",
                    models.FileField(upload_to="submitted_manuscripts/%Y/%m/%d/"),
                ),
                (
                    "supplementary",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to="supplementary_papers/%Y/%m/%d/",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("accepted", "Accepted"),
                            ("rejected", "Rejected"),
                        ],
                        default="pending",
                        max_length=10,
                    ),
                ),
                ("date_submitted", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "journal",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="helixpress_app.journal",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Volume",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("number", models.IntegerField(null=True)),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "journal",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="helixpress_app.journal",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Paper",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("title", models.CharField(max_length=200, null=True)),
                ("author", models.CharField(max_length=200, null=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("institution", models.CharField(max_length=200, null=True)),
                ("keywords", models.TextField(blank=True, null=True)),
                (
                    "document",
                    models.FileField(
                        blank=True, null=True, upload_to="published_papers/%Y/%m/%d/"
                    ),
                ),
                ("date_created", models.DateTimeField(auto_now_add=True, null=True)),
                ("doi", models.CharField(max_length=200, null=True)),
                ("editorsChoice", models.BooleanField(default=False)),
                (
                    "issue",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="helixpress_app.issue",
                    ),
                ),
                (
                    "journal",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="helixpress_app.journal",
                    ),
                ),
                (
                    "volume",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="helixpress_app.volume",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="issue",
            name="volume",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="helixpress_app.volume",
            ),
        ),
    ]
