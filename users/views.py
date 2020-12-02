from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render , redirect
from django.contrib.auth.views import LoginView , LogoutView
from django.views.generic.detail import DetailView
from .models import Accounts , Blogging
from my_jobs.models import Category , Job
from django.views.generic import TemplateView, ListView
from .forms import InviteEmployeeForm , BloggingForm
# Create your views here.
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView ,FormView
from .models import Profile
from .forms import UserUpdateForm
from .forms import AccountRegisterForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Invite  
from django.views.generic.edit import DeleteView


class UserRegisterView(SuccessMessageMixin,CreateView):
    template_name = "users/user-register.html"
    form_class = AccountRegisterForm
    success_url = "/"
    success_message = "Your account has been created!"

    def form_valid(self, form):
        user = form.save(commit=False)
        user_type = form.cleaned_data["user_types"]
        if user_type == "is_employee":
            user.is_employee = True
        elif user_type == "is_employer":
            user.is_employer = True
        
        user.save()

        return redirect(self.success_url)

class UserLoginView(LoginView):
    template_name = "users/login.html"


class UserLogoutView(LogoutView):
    template_name = "users/login.html"


@method_decorator(login_required(login_url="/login/"),name="dispatch")
class UserUpdateView(SuccessMessageMixin,UpdateView):
    model = Profile
    success_message = "You updated your profile"
    template_name = "users/update.html"
    form_class = UserUpdateForm

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(UserUpdateView, self).form_valid(form)


    def get(self,request,*args,**kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect("/")
        return super(UserUpdateView, self).get(request,*args,**kwargs)

    def get_success_url(self):
        return reverse("users:update_profile",kwargs={"pk":self.object.pk})

class EmployeeProfileView(CreateView):
    template_name = "employee-profile.html"
    model = Accounts
    form_class = InviteEmployeeForm

    def get_context_data(self, **kwargs):
        context = super(EmployeeProfileView,self).get_context_data(**kwargs)
        context["account"] = Accounts.objects.get(pk=self.kwargs["employee_id"])
        context["profile"] = Profile.objects.get(user_id=self.kwargs["employee_id"])
        context["job"] = Job.objects.get(id=self.kwargs["job_id"])
        context["categories"] = Category.objects.all() 
        return context

    def form_valid(self,form):
        instance = form.save(commit=False)
        instance.user = Accounts.objects.get(pk=self.kwargs["employee_id"])
        instance.job = Job.objects.get(pk=self.kwargs["job_id"])
        instance.save()
        return super(EmployeeProfileView,self).form_valid(form)
    
    def get_success_url(self):
        return reverse("users:employer_jobs")

@method_decorator(login_required(login_url="/login/"),name="dispatch")
class EmployerPostedJobsView(ListView):
    template_name = "users/employer-posted-jobs.html"
    context_object_name = "employer_jobs"
    model = Job
    paginated_by = 3

    def get_quaryset(self):
        return Job.objects.filter(employer=self.request.user).order_by("-id")

@method_decorator(login_required(login_url="/login/"),name="dispatch")
class EmployeeMessageView(ListView):
    model = Job
    template_name = "employee-messages.html"
    paginate_by = 5
    context_object_name = "jobs"

    def get_queryset(self):
        return Job.objects.filter(invites__isnull=False,invites__user_id=self.request.user).order_by("-invites")

class EmployeeDisplayMessageView(DetailView):
    model = Invite
    template_name = "users/employee-display-messages.html"
    context_object_name = "invite"

    def get_quaryset(self):
        invite = self.model.objects.filter(id=self.kwargs["pk"])
        invite.update(unread=False)
        return invite

    def get(self,request,*args,**kwargs):
        self.object=self.get_object()
        if self.object.user != request.user:
            return HttpResponseRedirect("/")
        return super(EmployeeDisplayMessageView, self).get(request,*args,**kwargs)

@method_decorator(login_required(login_url="/login/"),name="dispatch")
class AddWishListView(UpdateView):
    template_name = "my_jobs/index.html"
    model = Profile

    def get(self,request,*args,**kwargs):
        if self.request.user.is_employee:
            job = Job.objects.get(id=self.kwargs["pk"])
            profile = Profile.objects.get(user=request.user)
            profile.wish_list.add(job)
            return redirect("my_jobs:index")
        else:
            return redirect("my_jobs:index")

@method_decorator(login_required(login_url="/login/"),name="dispatch")
class RemoveFromWishListView(UpdateView):
    template_name = "my_jobs/index.html"
    model = Profile

    def get(self,request,*args,**kwargs):
        if self.request.user.is_employee:
            job = Job.objects.get(id=self.kwargs["pk"])
            profile = Profile.objects.get(user=request.user)
            profile.wish_list.remove(job)
            return redirect("my_jobs:index")
        else:
            return redirect("my_jobs:index")


class MyWishList(ListView):
    template_name = "users/my-wishlist.html"
    context_object_name = "jobs"
    model = Job
    paginate_by = 5

    def get_queryset(self):
        return Job.objects.filter(wish_list__user_id=self.request.user.id)

    def get_context_data(self, **kwargs):
        context = super(MyWishList, self).get_context_data(**kwargs)
      
        if self.request.user.is_authenticated:
            context["wish_list"]=Job.objects.filter(wish_list__user_id=self.request.user.id).values_list("id",flat=True)
            
        return context

    
class Blog(ListView):
    model = Blogging
    
    template_name = "users/blog.html"
    context_object_name = "blog"
    paginate_by = 4



class BlogPostView(CreateView):
    model = Blogging
    template_name = "users/single-blog.html"
    
    form_class = BloggingForm

    

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return redirect("users:blog")

class SingleBlogView(DetailView):
    model = Blogging
    template_name = "users/detail-blog-view.html"
    context_object_name = "details"

    def get_context_data(self, **kwargs):
        context = super(SingleBlogView,self).get_context_data(**kwargs)
        return context
    
    
    

class DeleteBlogView(SuccessMessageMixin,DeleteView):
    model =Blogging
    success_url = "/"
    template_name = "users/delete-blog.html"
    context_object_name = "details"
    




