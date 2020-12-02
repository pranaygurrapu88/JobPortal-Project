from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image
from ckeditor.fields import RichTextField
from my_jobs.models import Job
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
from django.template.defaultfilters import slugify
# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True


    def _create_user(self,email,password, **extra_fields):
        if not email:
            raise ValueError(" your email is not correct")


        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self,email,password=None,**extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email,password,**extra_fields)


    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser",True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser = True")

        return self._create_user(email,password,**extra_fields)




class Accounts(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_("email address"),unique=True)
    first_name = models.CharField(_("first name"),max_length=50,blank=False)
    last_name = models.CharField(_("last name"),max_length=50,blank=False)
    date_joined = models.DateTimeField(_("date joined"),auto_now_add=True)
    is_active = models.BooleanField(_("active"),default=True)
    is_staff = models.BooleanField(_("is_staff"),default=True)
    is_employee = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD="email"
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = ("user")
        verbose_name_plural = _("users")

    def get_profile_id(self):
        return self.profile.id

    def count_unread_messages(self):
        return self.invites.filter(unread=True).count()

    def unread_messages(self):
        return self.invites.filter(unread=False).values_list("job_id",flat=True)

class Profile(models.Model):
    user = models.OneToOneField(Accounts,on_delete=models.CASCADE,related_name="profile")
    image = models.ImageField(upload_to="media/users",default='media/users/newindex.png',blank=True,null=True)
    birth_day = models.DateField(default=None,blank=True,null=True)
    location= models.CharField(max_length=100,blank=True)
    resume = RichTextField(blank=True)
    company = models.CharField(max_length=250,blank=True)
    wish_list = models.ManyToManyField(Job,default=None,blank=True,related_name="wish_list")

    def __str__(self):
        return self.user.first_name +""+self.user.last_name+""+self.user.email


    def save(self,*args, **kwargs):
        super(Profile, self).save(*args,**kwargs)
        img = Image.open(self.image)
        if img.height > 200 or img.width > 200 :
            new_size = (200,200)
            img.thumbnail(new_size)
            img.save(self.image.path)

@receiver(models.signals.post_save, sender=Accounts)
def post_save_user_signal(sender,instance,created, **kwargs):
    if created:
        instance.save()
def create_user_profile(sender,instance,created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile,sender=Accounts)

class Invite(models.Model):
    user = models.ForeignKey(Accounts,on_delete=models.CASCADE,related_name="invites")
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name="invites")
    date = models.DateField(default=None,blank=True,null=True)
    message = RichTextField(blank=True)
    unread = models.BooleanField(default=True)    

    def __str__(self):
        return self.job.title



class Blogging(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    img = models.ImageField(upload_to="media/blog")
    content = RichTextField(blank=False)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        self.slug = slugify(self.title)
        super(Blogging, self).save(*args,**kwargs)



    # def save(self,*args, **kwargs):
    #     super(Blogging, self).save(*args,**kwargs)