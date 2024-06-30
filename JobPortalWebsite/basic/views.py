from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Count
from django.db import IntegrityError
# Create your views here.
from .models import skill,Job_fields,exp,user_fields,user_skill,city,job_seeker,Hr,job,skill_rqd,status,application

def view_applicant(request):

    return render(request,"view_applicant.html")

def view_applicants(request):
    if "job_id" in request.session:
        job_id = request.session["job_id"]
        jobb = job.objects.get(id = job_id)
        applicants = application.objects.filter(job_id = jobb).select_related("user_id")
        status_list = status.objects.all()
        context = {
            "applicants": applicants,
            "status_list": status_list
        }

        
    return render(request,'applicants.html',context)


def applied_jobs(request):
    applied_jobs = job.objects.filter(application__user_id=request.user).values('role', 'description', 'application__status_id__status')

    context = {
        "applied_jobs" : applied_jobs
    }

    return render(request,'applied_jobs.html',context)

def jobs_posted(request):
    hr_id = Hr.objects.get(hr_id = request.user)
    jobs_postedd = job.objects.filter(hr_id = hr_id)
    context = {
        "jobs_posted" : jobs_postedd
    }
    if request.method == "POST":
        job_id = request.POST.get('job_id')
        request.session["job_id"] = job_id
        return redirect("applicants")
    return render(request, 'jobs_posted.html',context)

@login_required(login_url='/hr/login')
def post_job(request):
    skills = skill.objects.all()
    cities = city.objects.all()
    fields = Job_fields.objects.all()
    context = {
        "skills" : skills,
        "cities": cities,
        "fields" : fields
    }
    if request.method == "POST":
        role = request.POST.get('role')
        field = request.POST.get('field')
        company = request.POST.get('company')
        openings = request.POST.get('openings')
        stipend = request.POST.get('stipend')
        duration = request.POST.get('duration')
        location = request.POST.get('location')
        cityy = request.POST.get('city')
        hr_id = Hr.objects.get(hr_id = request.user)
        city_id = city.objects.get(city_name = cityy)
        skills_list = request.POST.getlist('skill')
        fieldd = Job_fields.objects.get(field_name = field)
        job_description = f"skills required: {skills_list} \n stipend: {stipend} \n  city: {cityy} \n duration: {duration}"
        job_post = job(role = role, field_id = fieldd, company_name = company, hr_id = hr_id, openings = openings ,stipend = stipend, duration = duration, location = location, city_id = city_id, description=job_description)
        job_post.save()
        for selected_skill in skills_list:
            skill_idd = skill.objects.get(skill_name = selected_skill)
            skl_rqdd = skill_rqd(job_id = job_post,skill_id = skill_idd)
            skl_rqdd.save()
        
        messages.success(request,"Job posted Successfully")
        return redirect('hr-dashboard')
    return render(request,'postjob.html', context)
def homepage(request):
    return render(request, 'frontpage.html')

@login_required(login_url='/hr/login')
def hr_dashboard(request):


    return render(request,'hr_dashboard.html')

@login_required(login_url='/user/login')
def user_dashboard(request):
    logged_user = request.user
    userskills = user_skill.objects.filter(user_id=logged_user)
    userfields = user_fields.objects.filter(user_id = logged_user)
    seekerinfo = job_seeker.objects.get(user_id = logged_user)

    user_skills = user_skill.objects.filter(user_id=request.user).values_list('skill_id', flat=True)

    # Retrieve jobs where at least one required skill matches any of the user's skills
    matching_jobs = job.objects.filter(skill_rqd__skill_id__in=user_skills).distinct()

    context = {
        "user": request.user,
        "userskills" : userskills,
        "userfields": userfields,
        "seekerinfo": seekerinfo,
        "matching_jobs" : matching_jobs
    }

    if request.method == "POST":
        job_id = request.POST.get('job_id')
        jobb = job.objects.get(id=job_id)
        message = "na"
        user_id = request.user
        status_id = status.objects.get(status = "Applied")

        try:
            is_applied = application.objects.get(job_id = job_id, user_id = user_id )
            messages.success(request,"Already applied")
        except application.DoesNotExist:
            appl = application(job_id = jobb, message=message, user_id = user_id, status_id = status_id)
            appl.save()

    return render(request, 'user_dashboard.html', context)

def login_user(request):
    if request.method  == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user= authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('user-dashboard')
        else:
            messages.error(request,"Invalid Credentials")
    return render(request, 'userlogin.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password = make_password(password)
        email = request.POST.get('email')
        try:
            user = User(username=username,password=password,email=email)
            user.save()
            login(request,user)
            messages.success(request,"User Registration SuccessFull")
            return redirect('add-user-details')
        except IntegrityError:
            messages.error(request,"Username Already Taken")            
        
    return render(request, 'userregister.html')

def login_hr(request):
    if request.method  == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user= authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            try:
                is_hr = Hr.objects.get(hr_id = request.user)
                return redirect('hr-dashboard')
            except Hr.DoesNotExist:
                 messages.error(request,"Forbidden! Not a HR")
                 return redirect('user-dashboard')
               
        else:
            messages.error(request,"Invalid Credentials")
    return render(request, 'hrlogin.html')

def register_hr(request):
    city_list = city.objects.all()
    context = {      
        "city_list" : city_list
        }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        selected_city_value = request.POST.get('city')
        selected_city= city.objects.get(city_name=selected_city_value)
        company_name_value = request.POST.get('company')
        password = make_password(password)
        email = request.POST.get('email')
        try:
            user = User(username=username,password=password,email=email)
            user.save()
            login(request,user)
            hr = Hr(hr_id = request.user, city_id = selected_city, company_name = company_name_value)
            hr.save()
            messages.success(request,"HR Registration SuccessFull")
            return redirect('hr-dashboard')
        except IntegrityError:
            messages.error(request,"Username Already Taken") 
    return render(request, 'hrregister.html',context)


@login_required(login_url='/user/login')
def add_user_details(request):
    logged_user = request.user
    skills_list = skill.objects.all()
    fields_list = Job_fields.objects.all()
    city_list = city.objects.all()
    exp_list = exp.objects.all()
    context = {
        "skills_list" : skills_list,
        "fields_list" : fields_list,
        "exp_list" : exp_list,
        "city_list" : city_list
    }

    if request.method == 'POST':
        selected_skills = request.POST.getlist("skills")
        selected_fields = request.POST.getlist("fields")
        selected_exp = request.POST.get("exp")
        selected_location = request.POST.get("location")
        for selected_skill in selected_skills:
            skilll = skill.objects.get(skill_name = selected_skill)
            userskill = user_skill(user_id=request.user, skill_id = skilll)
            userskill.save()
        for selected_field in selected_fields:
            fieldd = Job_fields.objects.get(field_name = selected_field)
            userfields = user_fields(user_id = request.user, field_id = fieldd)
            userfields.save()
        expp = exp.objects.get(exp_name = selected_exp)
        locationn = city.objects.get(city_name = selected_location)

        job_seekerr = job_seeker(exp_id = expp, city_id = locationn, user_id = request.user)
        job_seekerr.save()
        return redirect('user-dashboard')
    return render(request, 'adduserdetails.html',context)
