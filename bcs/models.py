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
    description = models.TextField()
    rate_of_pay = models.CharField(max_length=100)
    
    def employees(self):
        employees_with_skill = Employee.objects.filter(skill__skill=self.skill)
        employees_with_skill_list = []
        for employee in employees_with_skill:
            employees_with_skill_list.append(employee.first_name + " " + employee.last_name)
        return ', '.join(employees_with_skill_list)
    
    
    def __str__(self):
        return self.skill


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project = models.CharField(max_length=1000)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    manager = models.ForeignKey(
        'bcs.Employee', on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField()
    date_signed = models.DateField(auto_created=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_created=True)
    actual_cost = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f'PROJECT ID: {self.project_id}'
    


class ProjectSchedule(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task_id = models.AutoField(primary_key=True)
    description = models.TextField()
    skills = models.ManyToManyField('bcs.Skill')
    number_of_employees = models.IntegerField()
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_created=True)
    
    def skills_required(self):
        return "\n".join([str(s) for s in self.skills.all()])

    def __str__(self):
        return f'PROJECT Schedule ID: {self.project.project_id}'


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
        return "\n".join([str(s) for s in self.skill.all()])
    
    
    def __str__(self):
        return f'{self.first_name} {self.middle_initial}'


class ProjectAssignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    project_schedule_task = models.ForeignKey(ProjectSchedule, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_created=True)
    
    def __str__(self):
      return f'PROJECT ID: {self.project_schedule_task.task_id}'


class WorkLog(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    assignment_id = models.ForeignKey(ProjectAssignment, on_delete=models.CASCADE)
    total_hours = models.IntegerField()
    bill_number = models.IntegerField()
    
    
    def __str__(self) -> str:
        return f'{self.employee.first_name} {self.employee.middle_initial}'