from django.shortcuts import render
from .forms import *
from django.urls import reverse
# Create your views here.
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from .models import Job, Category
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from .forms import CreateJobForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.views.generic.edit import DeleteView
from django.http import HttpResponseRedirect
from users.models import Accounts, Profile


class HomeView(ListView):
    template_name = "my_jobs/index.html"
    context_object_name = "jobs"
    model = Job
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["all_jobs"] = Job.objects.all().count() * 1997
        context["candidates"] = Accounts.objects.filter(is_employee=True).count() * 2000
        context["resumes"] = Profile.objects.exclude(resume="").count() * 600
        context["employers"] = Accounts.objects.filter(is_employer=True).count() * 1225
        if self.request.user.is_authenticated:
            context["wish_list"]=Job.objects.filter(wish_list__user_id=self.request.user.id).values_list("id",flat=True)
            
        return context

@method_decorator(login_required(login_url="/"),name="dispatch")
class CreateJobView(SuccessMessageMixin,CreateView):
    model = Job
    template_name = "my_jobs/create-jobs.html"
    form_class = CreateJobForm
    success_url = "/"
    success_message = "Job has been posted!"

    def form_valid(self, form):
        job = form.save(commit=False)
        job.employer = self.request.user
        job.save()
        return super(CreateJobView, self).form_valid(form)

class SingleJobView(SuccessMessageMixin,UpdateView):
    model = Job
    template_name = "my_jobs/job-single.html"
    context_object_name = "job"
    form_class = ApplyJobForm
    success_message = "you applied for this job"


    def get_context_data(self,*args, **kwargs):
        context = super(SingleJobView, self).get_context_data(*args ,**kwargs)
        context["categories"] = Category.objects.all()
        
        context["employee_applied"] = Job.objects.get(pk=self.kwargs["pk"]).employee.all().filter(id=self.request.user.id)
        context["in_my_list"] = Job.objects.get(pk=self.kwargs["pk"]).wish_list.all().filter(user_id=self.request.user.id)
        try:
            context["applied_employees"] = Job.objects.get(pk=self.kwargs["pk"],employer_id=self.request.user.id).employee.all()
            context["employer_id"] = Job.objects.get(pk=self.kwargs["pk"]).employer_id
        except:
            pass
        return context


    def form_valid(self, form):
        employee = self.request.user
        form.instance.employee.add(employee)
        form.save()
        return super(SingleJobView,self).form_valid(form)

    def get_success_url(self):
        return reverse("my_jobs:single_job",kwargs={"slug":self.object.slug,"pk":self.object.pk})
    
     


class CategoryDetailView(ListView):
    model = Job
    template_name = "my_jobs/category-detail.html"
    context_object_name = "jobs"
    paginate_by = 2


    def get_queryset(self):
        self.category = get_object_or_404(Category,pk=self.kwargs["pk"])
        return Job.objects.filter(category = self.category)

    def get_context_data(self,*args, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(*args ,**kwargs)
        self.category = get_object_or_404(Category,pk=self.kwargs["pk"])
        context["categories"] = Category.objects.all()
        context["category"] = self.category 
        return context

class SearchJobView(ListView):
    model = Job
    template_name = "my_jobs/search.html"
    paginate_by = 2
    context_object_name = "jobs"

    def get_queryset(self):
        q1 = self.request.GET.get("job_title")
        q2 = self.request.GET.get("job_type")
        q3 = self.request.GET.get("job_location")

        if q1 or q2 or q3 :
            return Job.objects.filter(Q(title__icontains=q1)|Q(description__icontains=q1),job_type=q2,location__icontains=q3).order_by("-id")
                                    

    
        return Job.objects.all().order_by("-id") 

    def get_context_data(self,*args, **kwargs):
        context = super(SearchJobView, self).get_context_data(*args ,**kwargs)
        context["categories"] = Category.objects.all()
        return context       

class UpdateJobView(UpdateView):
    model = Job
    template_name = "my_jobs/update.html"
    form_class = UpdateJobForm
    success_message = "You updated your job"

    def form_valid(self,form):
        form.instance.employer = self.request.user
        return super (UpdateJobView , self).form_valid(form)

    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        if self.object.employer != request.user:
            return HttpResponseRedirect("/")

        return super(UpdateJobView,self).get(request,*args, **kwargs)
    
    def get_success_url(self):
        return reverse("my_jobs:single_job",kwargs={"pk":self.object.pk,"slug":self.object.slug})

class DeleteJobView(SuccessMessageMixin,DeleteView):
    model = Job
    success_url = "/"
    template_name = "my_jobs/delete.html"

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.employer == request.user:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        else:
            return HttpResponseRedirect(self.success_url)
    
    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        if self.object.employer != request.user:
            return HttpResponseRedirect("/")

        return super(DeleteJobView,self).get(request,*args, **kwargs)

class AboutUs(TemplateView):
    template_name = "my_jobs/about.html"
   


  

    
    
         

  

   