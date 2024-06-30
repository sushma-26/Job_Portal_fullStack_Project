from django.urls import path
from . import views
urlpatterns = [
    path("",views.homepage, name="homepage"),
    path("user/login/",views.login_user, name="login"),
    path("user/register/",views.register_user, name="register-user"),
    path("hr/login/",views.login_hr, name="login-hr"),
    path("hr/register/",views.register_hr, name="register-hr"),
    path("user/add-user-details/",views.add_user_details, name="add-user-details"),
    path("user/dashboard/", views.user_dashboard, name="user-dashboard"),
    path("hr/dashboard/", views.hr_dashboard, name="hr-dashboard"),
    path("hr/post-job", views.post_job, name="post-job"),
    path("hr/jobs-posted/", views.jobs_posted, name="jobs-posted"),
    path("user/applied-jobs",views.applied_jobs, name="applied-jobs"),
    path("hr/applicants",views.view_applicants, name="applicants"),
    path("hr/view-applicant/",views.view_applicant,name="view-applicant")
]
