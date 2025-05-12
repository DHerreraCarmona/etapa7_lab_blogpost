from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserPermission(models.Model):
    class Roles(models.IntegerChoices):
            BLOGGER = 0, "Blogger"
            ADMIN = 1, "Admin"

    role = models.IntegerField(choices=Roles.choices,default=Roles.BLOGGER)
    def __str__(self):
        return self.get_role_display()
    class Meta:
        app_label = "user"
    
class Group(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email,username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('The Username must be set'))
        
        email = self.normalize_email(email)
        user = self.model(email=email,username=username, **extra_fields)
        user.set_password(password)

        # none_group, _ = Group.objects.get_or_create(name="None")
        # user.group = none_group

        user.save(using=self._db)
        return user 

    def create_superuser(self, email,username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        admin_role, _ = UserPermission.objects.get_or_create(role=UserPermission.Roles.ADMIN)
        extra_fields.setdefault('role', admin_role)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email,username, password, **extra_fields)  

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'),unique=True)
    username = models.CharField(_('username'),max_length=20,unique=True)
    is_active = models.BooleanField(_('active'),default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    role = models.ForeignKey(UserPermission,on_delete=models.SET_NULL,related_name="User",null=True,default=0)

    none_group, _ = Group.objects.get_or_create(name="None")
    group = models.ForeignKey(Group,on_delete=models.SET_NULL,related_name="user",null=True,default=none_group,blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

