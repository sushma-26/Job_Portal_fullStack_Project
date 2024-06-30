from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Job_fields( models.Model):
    field_name =  models.CharField(max_length=100)
    
    def __str__(self):
        return self.field_name
    
class exp(models.Model):
    exp_name = models.CharField(max_length=40)
    exp_lvl=models.IntegerField()

    def __str__( self):
        return self.exp_name
    
class skill(models.Model):
    skill_name = models.CharField(max_length=50)

    def __str__(self):
        return self.skill_name

class city( models.Model):
    city_name = models.CharField(max_length=50)

    def __str__(self):
        return self.city_name

class user_fields(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    field_id = models.ForeignKey(Job_fields, on_delete = models.CASCADE)

class user_skill( models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    skill_id = models.ForeignKey(skill,on_delete = models.CASCADE)

class job_seeker(models.Model):
    user_id = models.ForeignKey(User,on_delete = models.CASCADE)
    city_id = models.ForeignKey(city, on_delete = models.CASCADE)
    exp_id = models.ForeignKey(exp, on_delete = models.CASCADE)

class Hr(models.Model):
    hr_id =  models.ForeignKey(User, on_delete = models.CASCADE)
    company_name = models.CharField(max_length = 100)
    city_id = models.ForeignKey(city,on_delete = models.CASCADE)


class status(models.Model):
    status = models.CharField(max_length = 100)

class job(models.Model):
    role = models.CharField(max_length = 50)
    field_id = models.ForeignKey(Job_fields,on_delete = models.CASCADE)
    company_name = models.CharField(max_length = 100)
    hr_id  = models.ForeignKey(Hr,on_delete = models.CASCADE)
    openings = models.IntegerField()
    stipend = models.IntegerField()
    duration = models.CharField(max_length=100)
    location = models.CharField(max_length = 150)
    city_id = models.ForeignKey(city, on_delete = models.CASCADE)
    description = models.CharField(max_length = 250)


    
class skill_rqd( models.Model):
    job_id = models.ForeignKey(job, on_delete = models.CASCADE)
    skill_id = models.ForeignKey(skill, on_delete = models.CASCADE)

    
class application(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    job_id = models.ForeignKey(job,on_delete = models.CASCADE)
    status_id = models.ForeignKey(status,on_delete = models.CASCADE)
    message = models.CharField(max_length  = 200)

