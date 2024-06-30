from django.contrib import admin

from .models import Job_fields,exp,skill,city,user_fields,user_skill,job_seeker,Hr,status,job,application

admin.site.register(Job_fields)
admin.site.register(exp)
admin.site.register(skill)
admin.site.register(city)
admin.site.register(user_fields)
admin.site.register(user_skill)
admin.site.register(job_seeker)
admin.site.register(Hr)
admin.site.register(status)
admin.site.register(job)
admin.site.register(application)

