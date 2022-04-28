from pyexpat import model
from statistics import mode
from django.db import models
from django.forms import IntegerField
from customer.models import Customer


VALID_REGIONS = (
    ("Greater Accra (GA)", "Greater Accra (GA)"),
    ("Ashanti (AS)", "Ashanti (AS)"),
    ("Brong East (BE)", "Brong East (BE)"),
    ("Eastern Region (ER)", "Eastern Region (ER)"),
    ("Volta Region (VR)", "Volta Region (VR)"),
    ("Oti Region (OR)", "Oti Region (OR)")
)


VALID_SKILL = (
    ("Data Entry I", "Data Entry I"),
    ("Data Entry II", "Data Entry II"),
    ("Systems Analyst I", "Systems Analyst I"),
    ("Systems Analyst II", "Systems Analyst II"),
    ("Database Designer I", "Database Designer I",),
    ("Database Designer II", "Database Designer II"),
    ("Java I", "Java I"),
    ("Java II", "Java II"),
    ("C++ I", "C++ I"),
    ("C++ II", "C++ II"),
    ("Python I", "Python I"),
    ("Python II", "Python II"),
    ("ColdFusion I", "ColdFusion I"),
    ("ColdFusion II", "ColdFusion II"),
    ("ASP I", "ASP I"),
    ("ASP II", "ASP II"),
    ("Oracle DBA", "Oracle DBA"),
    ("MS SQL Server", "MS SQL Server"),
    ("DBA", "DBA"),
    ("Network Engineer I", "Network Engineer I"),
    ("Network Engineer II", "Network Engineer II"),
    ("Web Administrator", "Web Administrator"),
    ("Technical Writer", "Technical Writer"),
    ("Project Manager", "Project Manager")
)


class Skill(models.Model):
    skill_id = models.AutoField(primary_key=True)
    skill = models.CharField(max_length=200, choices=VALID_SKILL)
    description = models.TextField(blank=True, null=True)
    rate_of_pay = models.CharField(max_length=100)

    def employees(self):
        employees_with_skill = Employee.objects.filter(skill__skill=self.skill)
        employees_with_skill_list = []
        for employee in employees_with_skill:
            employees_with_skill_list.append(
                employee.first_name + " " + employee.last_name)
        return ', '.join(employees_with_skill_list)

    # Prevent duplicate skills
    def save(self, *args, **kwargs):
        if self.skill in [skill.skill for skill in Skill.objects.all()]:
            raise ValueError("Skill already exists")
        else:
            super(Skill, self).save(*args, **kwargs)

    def __str__(self):
        return self.skill


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    company = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date_signed = models.DateField(auto_created=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_created=True)
    actual_cost = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f'PROJECT ID: {self.project_id}'


class ProjectSchedule(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True, null=True)
    skills = models.ManyToManyField('bcs.Skill')
    number_of_employees = models.IntegerField()
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_created=True)

    def skills_required(self):
        return ", ".join([str(s) for s in self.skills.all()])

    # Only assign a project schedule to an employee if the employee is not already assigned to a project schedule
    def assign_employee(self, employee):
        if employee.project_schedule is None:
            employee.project_schedule = self
            employee.save()
        else:
            raise ValueError("Employee already assigned to a project schedule")

    def __str__(self):
        return f'{self.description}'


# Employee model \\ table
class Employee(models.Model):
    EmployeeId = models.AutoField(primary_key=True)
    skill = models.ManyToManyField(Skill)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_initial = models.CharField(max_length=5)
    date_of_hire = models.DateTimeField(auto_now_add=True)
    region = models.CharField(max_length=50, choices=VALID_REGIONS, default=0)

    def skills(self):
        return ", ".join([str(s) for s in self.skill.all()])

    def __str__(self):
        return f'{self.first_name} {self.middle_initial}'


class ProjectAssignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    employee = models.ManyToManyField(Employee, blank=True, null=True)
    project_schedule_task = models.ForeignKey(
        ProjectSchedule, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_created=True)
    
    # get all skills from project_schedule_task
    def skills (self):
        return ", ".join([str(s) for s in self.project_schedule_task.skills.all()])
    
    # Get project task from project_schedule_task
    def project_task(self):
        return self.project_schedule_task.description

    # get project_schedule_task start date
    def scheduled_start_date(self):
        return self.project_schedule_task.start_date

    # get project_schedule_task end date
    def scheduled_end_date(self):
        return self.project_schedule_task.end_date

    def assginment_start_date(self):
        return self.start_date

    def assginment_end_date(self):
        return self.end_date

    # get employees
    def employees(self):
        return ", ".join([str(e) for e in self.employee.all()])

    def __str__(self):
        return f'PROJECT ID: {self.project_schedule_task.task_id}'


class WorkLog(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    assignment_id = models.ForeignKey(
        ProjectAssignment, on_delete=models.CASCADE)
    total_hours = models.IntegerField()
    bill_number = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.employee.first_name} {self.employee.middle_initial}'


class Bill(models.Model):
    bill_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_hours = models.IntegerField()

    def __str__(self):
        return f'BILL ID: {self.bill_id}'
