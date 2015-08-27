from datetime import date

from django import forms
from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.forms import CheckboxSelectMultiple
from django.db import models

from django.contrib.auth import get_permission_codename
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm

from models import (
    Institute,
    OrgLevel1,
    OrgLevel2,
    OrgLevel3,
    ReportingPeriod,
    InstituteAdmin,
    StrategicObjective,
    ProjectLeader,
    ProjectDetail,
    ProjectFunding,
    PHDStudent,
    ProjectOutput,
    NewCourseDetail,
    CourseReqDetail,
    Collaborators,
    CustomUser,
    ResearchTeamMember
)

from forms import ProjectDetailForm, ProjectDetailAdminForm


ORG_LEVEL_FIELDS = ["org_level_1", "org_level_2", "org_level_3"]

# ------------------------------------------------------------------------------
# General utility classes and functions
# ------------------------------------------------------------------------------

class ReadOnlyMixin(InlineModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if user_has_perm(request, self.opts, 'view'):
            result = list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))
            result.remove('id')
            return result
        return super(ReadOnlyMixin, self).get_readonly_fields(request, obj=obj)

    def has_add_permission(self, request):
        if user_has_perm(request, self.opts, 'view'):
            return False

    def has_delete_permission(self, request, obj=None):
        if user_has_perm(request, self.opts, 'view'):
            return False


def user_has_perm(request, opts, perm_type):
    """
    Return True if user has the permission to perform specific action
        param obj request: Current request object
        param obj opts: options for current ModelAdmin instance
        param str perm_type: type of permission to check for
    """
    codename = get_permission_codename(perm_type, opts)
    return request.user.has_perm("%s.%s" % (opts.app_label, codename))

def get_user_institute(user):
    """
    Return the institute to which the user belongs
    """
    try:
        if user.project_leader:
            return user.project_leader.institute
    except ObjectDoesNotExist:
        return user.institute_admin.institute

# ------------------------------------------------------------------------------
# Formsets
# ------------------------------------------------------------------------------

class ProjectDetailFormSet(forms.models.BaseInlineFormSet):
    def is_valid(self):
        return super(ProjectDetailFormSet, self).is_valid() and \
                    not any([bool(e) for e in self.errors])

    def clean(self, error_msg):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if count < 1:
            raise forms.ValidationError(error_msg)


class PHDStudentFormSet(ProjectDetailFormSet):
    def clean(self):
        if self.instance.phd_research == 'Y':
            error_msg = 'Please enter the PhD student\'s name.'
            super(PHDStudentFormSet, self).clean(error_msg)


class NewCourseDetailFormSet(ProjectDetailFormSet):
    def clean(self):
        if self.instance.new_courses == 'Y':
            error_msg = 'Please enter the course\'s details.'
            super(NewCourseDetailFormSet, self).clean(error_msg)


class CourseReqDetailFormSet(ProjectDetailFormSet):
    def clean(self):
        if self.instance.course_requirement == 'Y':
            error_msg = 'Please enter the course\'s details.'
            super(CourseReqDetailFormSet, self).clean(error_msg)


class CollaboratorsFormSet(ProjectDetailFormSet):
    def clean(self):
        if self.instance.external_collaboration == 'Y':
            error_msg = 'Please enter the collaborator\'s details.'
            super(CollaboratorsFormSet, self).clean(error_msg)


# ------------------------------------------------------------------------------
# Inlines
# ------------------------------------------------------------------------------

class ProjectFundingInline(ReadOnlyMixin, admin.TabularInline):
    model = ProjectFunding
    extra = 1
    inline_classes = ('grp-collapse grp-open',)
    verbose_name = _('funding source')
    verbose_name_plural = _('6.1: Please list sources of project funding, the number of years for which funding has been secured, and the amount of funding (in US$).')


class PHDStudentInline(ReadOnlyMixin, admin.TabularInline):
    model = PHDStudent
    formset = PHDStudentFormSet
    extra = 1
    inline_classes = ('grp-collapse grp-open',)
    verbose_name = _('student')
    verbose_name_plural = _('7.2.1: If yes, please provide their names.')


class ProjectOutputInline(ReadOnlyMixin, admin.StackedInline):
    model = ProjectOutput
    extra = 1
    inline_classes = ('grp-collapse grp-open',)
    verbose_name = _('Project output')
    verbose_name_plural = _('8.1: Please add the completed publications and other outputs for this project.')


class NewCourseDetailInline(ReadOnlyMixin, admin.TabularInline):
    model = NewCourseDetail
    formset = NewCourseDetailFormSet
    extra = 1
    inline_classes = ('grp-collapse grp-open',)
    verbose_name = _('new course')
    verbose_name_plural = _('9.2.1: If yes, please provide the new course details')


class CourseReqDetailInline(ReadOnlyMixin, admin.TabularInline):
    model = CourseReqDetail
    formset = CourseReqDetailFormSet
    extra = 1
    inline_classes = ('grp-collapse grp-open',)
    verbose_name = _('required course')
    verbose_name_plural = _('9.5.1: If yes, please provide the course details.')


class CollaboratorsInline(ReadOnlyMixin, admin.TabularInline):
    model = Collaborators
    formset = CollaboratorsFormSet
    extra = 1
    inline_classes = ('grp-collapse grp-open',)
    verbose_name = _('collaborator')
    verbose_name_plural = _('10.1.1: If yes, please provide the collaborator details.')


class InstituteAdminInline(admin.TabularInline):
    model = InstituteAdmin
    can_delete = False


class ProjectLeaderInline(admin.StackedInline):
    model = ProjectLeader
    can_delete = False
    inline_classes = ('grp-collapse grp-open',)
    verbose_name = _('Project Leader')
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == 'institute':
                kwargs["queryset"] = Institute.objects.filter(
                    id=get_user_institute(request.user).id)
            if db_field.name in ORG_LEVEL_FIELDS:
                    kwargs["queryset"] = db_field.related_model.objects.filter(
                        institute=get_user_institute(request.user))
        return super(ProjectLeaderInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)


class StrategicObjectiveInline(admin.TabularInline):
    model = StrategicObjective
    inline_classes = ('grp-collapse grp-open',)
    extra = 7
    verbose_name = _('Strategic objectives of the Institute')
    verbose_name_plural = _('Strategic Objectives')


# ------------------------------------------------------------------------------
# Filters
# ------------------------------------------------------------------------------

class ReportingPeriodFilter(admin.SimpleListFilter):
    title = "Reporting Period"
    parameter_name = 'reporting_period'

    def lookups(self, request, model_admin):
        reporting_periods = []
        if not request.user.is_superuser:
            reporting_periods = list(ReportingPeriod.objects.filter(
                institute=get_user_institute(request.user)))

        return [(rp.id, rp.name) for rp in reporting_periods]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(reporting_period=self.value())
        else:
            return queryset

# ------------------------------------------------------------------------------
# Custom User Admin
# ------------------------------------------------------------------------------

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)


class CustomUserAdmin(UserAdmin):
    inlines = [InstituteAdminInline, ProjectLeaderInline]
    add_form = CustomUserCreationForm

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    def get_queryset(self, request):
        if not request.user.is_superuser:
            return self.model.objects.filter(
                project_leader__institute=get_user_institute(request.user))
        else:
            return super(CustomUserAdmin, self).get_queryset(request)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(CustomUserAdmin, self).get_fieldsets(request, obj=obj)
        if obj and not request.user.is_superuser:
            fieldsets = (
                (None, {'fields': ('email', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name')})
            )
        return fieldsets

# ------------------------------------------------------------------------------
# ModelAdmins
# ------------------------------------------------------------------------------

class InstituteModelAdmin(admin.ModelAdmin):
    inlines = [StrategicObjectiveInline]


class OrgLevelAdmin(admin.ModelAdmin):
    pass


class ReportingPeriodAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'is_active', 'open_date', 'close_date')
    readonly_fields = ('open_date', 'close_date')
    list_display = ('name', 'description', 'open_date', 'close_date', 'is_active')

    # actions = ['close_reporting_period']

    def get_queryset(self, request):
        return self.model.objects\
                .filter(institute=request.user.institute_admin.institute)

    def has_add_permission(self, request, obj=None):
        # Can only be added if all existing reporting periods are closed.
        if not request.user.is_superuser:
            if user_has_perm(request, self.opts, 'add'):
                institute = request.user.institute_admin.institute
                if self.model.objects\
                                .filter(institute=institute)\
                                .filter(is_active=True):
                    return False
                return True
        return False

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if user_has_perm(request, self.opts, 'change'):
                return True
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.institute = request.user.institute_admin.institute
            obj.save()
        else:
            if obj.is_active == False:
                obj.close_date = date.today()
                obj.save()

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_active == False:
            return self.readonly_fields + ('is_active',)
        return self.readonly_fields


class ProjectDetailAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'record_status')
    list_display_links = ('__unicode__',)
    list_filter = []
    form = ProjectDetailForm
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    inlines = [
        ProjectFundingInline,
        PHDStudentInline,
        ProjectOutputInline,
        NewCourseDetailInline,
        CourseReqDetailInline,
        CollaboratorsInline,
    ]

    radio_fields = {
        'is_leader': admin.HORIZONTAL,
        'is_flagship': admin.HORIZONTAL,
        'project_status': admin.HORIZONTAL,
        'classification': admin.VERTICAL,
        'initiation': admin.VERTICAL,
        'authors': admin.HORIZONTAL,
        'amendments_permitted': admin.HORIZONTAL,
        'public_domain': admin.HORIZONTAL,
        'adv_group': admin.HORIZONTAL,
        'adv_group_freq': admin.VERTICAL,
        'new_initiative': admin.HORIZONTAL,
        'new_initiative_party': admin.VERTICAL,
        'research': admin.VERTICAL,
        'phd_research': admin.HORIZONTAL,
        'curriculum_changes': admin.HORIZONTAL,
        'new_courses': admin.HORIZONTAL,
        'students_involved': admin.HORIZONTAL,
        'course_requirement': admin.HORIZONTAL,
        'external_collaboration': admin.HORIZONTAL
    }

    fieldsets = (
        (None, {
            'fields': ('name', 'is_leader', 'is_flagship'),
            'description': ''
        }),
        (None, {
            'fields': ('org_level_1',),
            'description': '1.4 Please indicate where the project is located.'
        }),
        (None, {
            'fields': ('project_status', 'start_date', 'end_date', 'description', 'focus_area',
                'focus_area_text', 'classification'),
            'description': ''
        }),
        (None, {
            'fields': ('strategic_objectives', 'outcomes', 'beneficiaries'),
            'description': ''
        }),
        (None, {
            'fields': ('initiation', 'authors', 'amendments_permitted', 'public_domain', 'public_domain_url', 'adv_group',
                'adv_group_rep', 'adv_group_freq'),
            'description': ''
        }),
        (None, {
            'fields': ('team_members', 'team_members_text', 'new_initiative', 'new_initiative_text',
                'new_initiative_party', 'new_initiative_party_text'),
            'description': ''
        }),
        (None, {
            'fields': ('research', 'research_text', 'phd_research'),
            'description': ''
        }),
        (None, {
            'fields': ('curriculum_changes', 'curriculum_changes_text', 'new_courses', 'students_involved', 'student_types',
                'student_nature', 'student_nature_text'),
            'description': ''
        }),
        (None, {
            'fields': ('course_requirement', 'external_collaboration'),
            'description': ''
        }),
        (None, {
            'fields': (),
            'description': ''
        }),
    )

    class Media:
        js = ('javascript/app.js',)

    def has_add_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if user_has_perm(request, self.opts, 'add'):
                # Can only add if a reporting period is open
                institute = request.user.project_leader.institute
                if ReportingPeriod.objects\
                            .filter(institute=institute)\
                            .filter(is_active=True):
                    return True
        return False

    def has_change_permission(self, request, obj=None):
        if not request.user.is_superuser:
            if user_has_perm(request, self.opts, 'change'):
                return True
            if user_has_perm(request, self.opts, 'view'):
                return True
        return True

    def get_list_display(self, request):
        """
        Only show is_flagged field to admin users
        """
        if request.user.is_institute_admin() or request.user.is_superuser:
            list_display = self.list_display + ('is_flagged',)
            return list_display
        return self.list_display

    def get_list_filter(self, request):
        if not request.user.is_superuser:
            self.list_filter.append(ReportingPeriodFilter)
        return super(ProjectDetailAdmin, self).get_list_filter(request)

    def get_queryset(self, request):
        if not request.user.is_superuser:
            qs = self.model.objects\
                    .filter(is_deleted=False)\
                    .filter(proj_leader__institute=get_user_institute(request.user))
            if user_has_perm(request, self.opts, 'view'):
                # Don't include draft records
                return qs.exclude(record_status=1)
            if user_has_perm(request, self.opts, 'change'):
                return qs
        return super(ProjectDetailAdmin, self).get_queryset(request)

    def get_readonly_fields(self, request, obj=None):
        # For users with view access, all fields are readonly
        if user_has_perm(request, self.opts, 'view'):
            readonly_fields = []
            for field in self.form.base_fields.keys():
                if field not in self.form.Meta.exclude:
                    if field not in self.form.Meta.admin_editable:
                        readonly_fields.append(field)
            return readonly_fields
        return super(ProjectDetailAdmin, self).get_readonly_fields(request, obj=obj)

    def get_form(self, request, obj=None, **kwargs):
        # Global and institute admin have readonly views
        if request.user.is_institute_admin() or request.user.is_superuser:
            self.form = ProjectDetailAdminForm
        return super(ProjectDetailAdmin, self).get_form(request, obj=obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in ORG_LEVEL_FIELDS:
            kwargs["queryset"] = db_field.related_model.objects.filter(
                institute=get_user_institute(request.user))
        return super(ProjectDetailAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "strategic_objectives":
            kwargs["queryset"] = StrategicObjective.objects.filter(
                institute=get_user_institute(request.user))
        return super(ProjectDetailAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(ProjectDetailAdmin, self).get_fieldsets(request, obj=obj)
        if not request.user.is_superuser:
            institute = get_user_institute(request.user)
            field_list = []
            for field in ORG_LEVEL_FIELDS:
                if getattr(institute, '%s_name' % field) != '':
                    field_list.append(field)
            fields = tuple(field_list)
            fieldsets[1][1]['fields'] = fields

        if user_has_perm(request, self.opts, 'view'):
            # Global + institute admin
            fieldsets[len(fieldsets)-1][1]['fields'] = ('is_rejected', 'rejected_detail', 'is_flagged')
        return fieldsets

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        form = context['adminform'].form
        if form.fields.get('org_level_1', False):
            if add:
                institute = get_user_institute(request.user)
            elif change:
                institute = obj.institute

            for field in ORG_LEVEL_FIELDS:
                level_name = getattr(institute, '%s_name' % field)
                if level_name != '':
                    # If level_name is empty, formset doesn't have the fields included
                    # See get_fieldsets() above
                    form.fields[field].label = level_name

        return super(ProjectDetailAdmin, self).render_change_form(
            request, context, add=False, change=False, form_url='', obj=obj)

    def save_model(self, request, obj, form, change):
        """
        This assumes that only one reporting period can be active at a time
        for a given Institute.
        RECORD_STATUS:
            1: Draft -> _draft
            2: Final -> _save
        """
        institute = get_user_institute(request.user)
        reporting_period = institute.reporting_period.get(is_active=True)
        if not change:
            # New project being saved
            obj.reporting_period = reporting_period
            if request.POST.get('_draft'):
                obj.record_status = 1
            else:
                obj.record_status = 2
            obj.institute = get_user_institute(request.user)
            obj.proj_leader = request.user.project_leader

        else:
            if request.POST.get('_delete'):
                # mark object as deleted
                obj.is_deleted = True

            elif request.POST.get('_save'):
                # If project is being submitted as final: update record status
                # If we're in a new reporting period:
                # - update reporting period if it's a draft that's being saved,
                # - create a copy of the object if it's a final object that's being saved

                if obj.record_status == 1:
                    obj.record_status = 2
                    if obj.reporting_period != reporting_period:
                        obj.reporting_period = reporting_period
                elif obj.record_status == 2:
                    if obj.reporting_period != reporting_period:
                        # Save a copy of the instance
                        obj.reporting_period = reporting_period
                        obj.pk = None

        # Flag as suspect if other academics is the only chosen team member
        # 7: Other academics
        other_academics = ResearchTeamMember.objects.get(id=7)
        if other_academics in form.cleaned_data.get('team_members') and len(form.cleaned_data.get('team_members')) == 1:
            obj.is_flagged = True
        obj.save()


admin.site.register(Institute, InstituteModelAdmin)
admin.site.register(OrgLevel1, OrgLevelAdmin)
admin.site.register(OrgLevel2, OrgLevelAdmin)
admin.site.register(OrgLevel3, OrgLevelAdmin)
admin.site.register(ReportingPeriod, ReportingPeriodAdmin)
admin.site.register(ProjectDetail, ProjectDetailAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
