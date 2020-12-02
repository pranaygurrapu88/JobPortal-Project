from django.urls import path

from .views import *
from django.contrib.auth import views as authViews
app_name = "users"
urlpatterns = [
    path("register/",UserRegisterView.as_view(),name="register"),
    path("login/",UserLoginView.as_view(),name="login"),
    path("logout/",UserLogoutView.as_view(),name="logout"),
    path("password-change/",authViews.PasswordChangeView.as_view(),name="password_change"),
    path("password-change-done/",authViews.PasswordChangeDoneView.as_view(),name="password_change_done"),
   
    path("update-profile/<int:pk>/",UserUpdateView.as_view(),name="update_profile"),
    path("employee-profile/<int:employee_id>/<int:job_id>",EmployeeProfileView.as_view(),name="employee_profile"),
    path("employer-jobs/",EmployerPostedJobsView.as_view(),name="employer_jobs"),
    path("employee-message/<int:pk>/",EmployeeMessageView.as_view(),name="employee_messages"),
    path("employee-display-message/<int:pk>/",EmployeeDisplayMessageView.as_view(),name="employee_display_messages"),
    path("add-wishlist/<int:pk>/",AddWishListView.as_view(),name="add_wishlist"),
    path("remove-from-wishlist/<int:pk>/",RemoveFromWishListView.as_view(),name="remove_from_wishlist"),
    path("mywishlist/<int:pk>/",MyWishList.as_view(),name="my_wishlist"),
    path("blog/",Blog.as_view(),name='blog'),
    path("blog-single/",BlogPostView.as_view(),name='blog_single'),
    path("blog-detail/<slug:slug>",SingleBlogView.as_view(),name='blog_detail'),
    path("delete-blog/<slug:slug>",DeleteBlogView.as_view(),name='blog_delete'),
    
]