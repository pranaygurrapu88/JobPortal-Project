from django.urls import path
from . import views

app_name = "my_jobs"
urlpatterns = [
    path('',views.HomeView.as_view(), name="index"),
    path('create-job/',views.CreateJobView.as_view(), name="create_job"),
    path('category-detail/<slug>/<int:pk>',views.CategoryDetailView.as_view(), name="category_detail"),
    path('search/',views.SearchJobView.as_view(), name="search"),
    path("detail/<slug>/<int:pk>/",views.SingleJobView.as_view(),name="single_job"),
    path("update/<slug>/<int:pk>/",views.UpdateJobView.as_view(),name="update_job"),
    path("delete/<slug>/<int:pk>/",views.DeleteJobView.as_view(),name="delete_job"),
    path("about/",views.AboutUs.as_view(),name='about_us'),
    
   
]