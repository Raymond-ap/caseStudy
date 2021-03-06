from csv import list_dialects
from dataclasses import field, fields
from django.contrib import admin
from .models import *


admin.site.site_header = "BSYSTEMS COMPUTER SOLUTIONS"


class SkillAdmin(admin.ModelAdmin):
    list_display = ("skill", "employees")


class ProjectAdmin(admin.ModelAdmin):
    list_display = ("start_date", "end_date","company", "description", "actual_cost")


class ProjectScheduleAdmin(admin.ModelAdmin):
    list_display = ("start_date", "end_date", "description",
                    "skills_required", "number_of_employees")


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("EmployeeId", "first_name", "last_name",
                    "middle_initial", "skills", "date_of_hire", "region")


class ProjectAssignmentAdmin(admin.ModelAdmin):
    list_display = ("project_task", "scheduled_start_date", "scheduled_end_date",
                    "employees", "skills", "assginment_start_date", "assginment_end_date")


class WorkLogAdmin(admin.ModelAdmin):
    list_display = ("employee", "date", "assignment_id",
                    "total_hours", "bill_number")


class BillAdmin(admin.ModelAdmin):
    list_display = ("bill_id", "customer_id", "total_hours")

admin.site.register(Skill, SkillAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectSchedule, ProjectScheduleAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(ProjectAssignment, ProjectAssignmentAdmin)
admin.site.register(WorkLog, WorkLogAdmin)
admin.site.register(Bill, BillAdmin)
