from dataclasses import field, fields
from django.contrib import admin
from .models import *


admin.site.site_header = "BSYSTEMS COMPUTER SOLUTIONS"

class SkillAdmin(admin.ModelAdmin):     
    list_display = ("skill", "employee")


class ProjectAdmin(admin.ModelAdmin):
    pass


class ProjectScheduleAdmin(admin.ModelAdmin):
    fields = ("project", "description")
    list_display = ("start_date", "end_date", "description",
                    "skills_required", "number_of_employees")


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("EmployeeId", "first_name", "last_name",
                    "middle_initial", "skills", "date_of_hire", "region")


class ProjectAssignmentAdmin(admin.ModelAdmin):
    pass


class WorkLogAdmin(admin.ModelAdmin):
    list_display = ("employee", "date", "assignment_id",
                    "total_hours", "bill_number")


admin.site.register(Skill, SkillAdmin)
admin.site.register(Project)
admin.site.register(ProjectSchedule, ProjectScheduleAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(ProjectAssignment)
admin.site.register(WorkLog, WorkLogAdmin)
