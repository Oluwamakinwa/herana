# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvisoryGroupRep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Collaborators',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('university', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='CourseReqDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name_plural': 'Faculties',
            },
        ),
        migrations.CreateModel(
            name='FocusArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Institute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('logo', models.ImageField(null=True, upload_to=b'', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='InstituteAdmin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('institute', models.ForeignKey(related_name='institute_admin', to='herana.Institute')),
                ('user', models.OneToOneField(related_name='institute_admin', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NewCourseDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='PHDStudent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_status', models.CharField(max_length=1, null=True, choices=[(1, 'Complete'), (2, 'Ongoing')])),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('multi_faculty', models.CharField(max_length=1, null=True, verbose_name='Does the project span multiple faculties/schools?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('description', models.TextField(null=True, verbose_name='Please provide a short description of the project.')),
                ('focus_area_text', models.CharField(help_text=b'', max_length=256, null=True)),
                ('classification', models.PositiveIntegerField(null=True, verbose_name='How would you classify this flagship engagement activity?', choices=[(1, 'Project'), (2, 'Programme'), (3, 'Service'), (4, 'Other')])),
                ('outcomes', models.TextField(null=True)),
                ('beneficiaries', models.TextField(null=True)),
                ('initiation', models.PositiveIntegerField(null=True, choices=[(1, 'Approached or invited by funder, company, NGO, government, research institute or by another university to submit a proposal for the project'), (2, 'Informed by the university research or contracts office about the reach project'), (3, 'Initiated by colleagues at own university'), (4, 'Initiated by project leader'), (5, 'Initiated by project leader in collaboration with colleagues'), (6, 'Follow-on or continuation from existing project'), (7, 'Project assigned to project leader')])),
                ('authors', models.PositiveIntegerField(null=True, choices=[(1, 'One author'), (1, 'More than one author')])),
                ('amendments_permitted', models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('public_domain', models.CharField(help_text=b'If yes, please provide the URL', max_length=1, null=True, verbose_name='Will the written up findings or data or other outputs of the project be available electronically in the public domain?', choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('public_domain_url', models.URLField(null=True, verbose_name='URL')),
                ('adv_group', models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('adv_group_freq', models.PositiveIntegerField(null=True, choices=[(1, 'Monthly'), (2, 'Quarterly'), (3, 'Annually'), (4, 'Ad hoc')])),
                ('new_initiative', models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('new_initiative_text', models.TextField(null=True)),
                ('new_initiative_party', models.PositiveIntegerField(null=True, choices=[(1, 'A third party has been contracted to develop the product / service / intervention / policy'), (2, 'The project team will develop the product / service / intervention / policy'), (3, 'Other')])),
                ('new_initiative_party_text', models.TextField(null=True)),
                ('research', models.PositiveIntegerField(null=True, choices=[(1, 'The project conducted original research'), (2, 'The project collected new data and conducted original research to complete the project'), (3, 'The project collected new data and applied existing knowledge to the data collected to complete the project'), (4, 'No new data was required and existing knowledge was applied to complete the project'), (5, 'Not applicable')])),
                ('research_text', models.TextField(null=True)),
                ('phd_research', models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('curriculum_changes', models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('curriculum_changes_text', models.TextField(null=True)),
                ('new_courses', models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('students_involved', models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('student_nature_text', models.CharField(max_length=128, null=True)),
                ('course_requirement', models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('external_collaboration', models.CharField(max_length=1, null=True, choices=[(b'Y', 'Yes'), (b'N', 'No')])),
                ('record_status', models.PositiveIntegerField(choices=[(1, b'Draft'), (2, b'Final'), (3, b'Rejected')])),
                ('adv_group_rep', models.ManyToManyField(to='herana.AdvisoryGroupRep')),
                ('collaboration_detail', models.ManyToManyField(to='herana.Collaborators')),
                ('course_req_detail', models.ManyToManyField(to='herana.CourseReqDetail')),
                ('faculty', models.ForeignKey(verbose_name=(), to='herana.Faculty', null=True)),
                ('focus_area', models.ManyToManyField(help_text=b'Select ALL applicable', to='herana.FocusArea', verbose_name='Please provide a short description of the project.')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectFunding',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('funder', models.CharField(max_length=256)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('years', models.DecimalField(max_digits=5, decimal_places=2)),
                ('renewable', models.BooleanField(choices=[(b'Y', 'Yes'), (b'N', 'No')])),
            ],
        ),
        migrations.CreateModel(
            name='ProjectHeader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('is_flagship', models.BooleanField(default=False)),
                ('is_leader', models.BooleanField(default=False)),
                ('faculty', models.ForeignKey(to='herana.Faculty')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectLeader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('staff_no', models.CharField(max_length=64)),
                ('position', models.CharField(max_length=128)),
                ('faculty', models.ForeignKey(to='herana.Faculty')),
                ('institute', models.ForeignKey(to='herana.Institute')),
                ('user', models.OneToOneField(related_name='project_leader', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectOutputs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ReportingPeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('open_date', models.DateField(auto_now_add=True)),
                ('close_date', models.DateField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Open')),
                ('institute', models.ForeignKey(related_name='reporting_period', to='herana.Institute')),
            ],
        ),
        migrations.CreateModel(
            name='ResearchTeamMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='StrategicObjective',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('statement', models.CharField(max_length=512)),
                ('institute', models.ForeignKey(to='herana.Institute')),
            ],
        ),
        migrations.CreateModel(
            name='StudentParticipationNature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='StudentType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('choice', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='projectheader',
            name='proj_leader',
            field=models.ForeignKey(to='herana.ProjectLeader'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='funding',
            field=models.ManyToManyField(to='herana.ProjectFunding'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='header',
            field=models.ForeignKey(related_name='project_detail', verbose_name='Name of flagship engagement project', to='herana.ProjectHeader'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='new_course_detail',
            field=models.ManyToManyField(to='herana.NewCourseDetail'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='outputs',
            field=models.ManyToManyField(to='herana.ProjectOutputs'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='phd_research_name',
            field=models.ManyToManyField(to='herana.PHDStudent'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='reporting_period',
            field=models.ForeignKey(to='herana.ReportingPeriod'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='strategic_objectives',
            field=models.ManyToManyField(to='herana.StrategicObjective'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='student_nature',
            field=models.ManyToManyField(to='herana.StudentParticipationNature'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='student_types',
            field=models.ManyToManyField(to='herana.StudentType'),
        ),
        migrations.AddField(
            model_name='projectdetail',
            name='team_members',
            field=models.ManyToManyField(to='herana.ResearchTeamMember'),
        ),
        migrations.AddField(
            model_name='faculty',
            name='institute',
            field=models.ForeignKey(to='herana.Institute'),
        ),
    ]