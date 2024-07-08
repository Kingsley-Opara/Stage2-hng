from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models.signals import pre_save, post_save


# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, firstname, lastname, email, phone = None, password =None, **other_fields):
        other_fields.setdefault("is_active", True)
        # other_fields.setdefault("is_staff", False)
        # other_fields.setdefault("is_superuser", False)

        if not firstname:
            raise ValueError('Firstname cannot be blank')
        if not lastname:
            raise ValueError ('Lastname cannot be blank')
        if not email:
            raise ValueError ("Email can't be blank")
        
        email = self.normalize_email(email)
        user = self.model(firstname=firstname, lastname=lastname, email= email, phone=phone, password=password)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staffuser(self, firstname, lastname, email, phone = None, password =None, **other_fields):
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_staff", True)

        if not other_fields.get('active'):
            raise ValueError('All staff users must have an active account')

        user = self.create_user(
            firstname= firstname,
            lastname= lastname,
            email= email,
            phone= phone,
            password= password,
            **other_fields
        )
        user.save(using= self._db)
        return user
    
    def create_superuser(self, firstname, lastname, email, phone = None, password =None, **other_fields):
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)

        if not other_fields.get('is_active'):
            raise ValueError('All superuser must have an active account')
        if not other_fields.get('is_staff'):
            raise ValueError('All superuser must have an active account')
        
        user = self.create_user(
            firstname= firstname,
            lastname= lastname,
            email= email,
            phone= phone,
            password= password,
            **other_fields
        )
        user.save(using= self._db)
        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    userId = models.IntegerField(blank= True, null=True, editable=False, unique=True)
    firstname = models.CharField(max_length=25)
    lastname = models.CharField(max_length=25)
    phone = models.CharField(max_length=25, blank=True, null=True)
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['firstname', 'lastname']
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.firstname

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    

class Organizations(models.Model):
    orgId = models.IntegerField(blank= True, null=True, editable=False, unique=True)
    user = models.ManyToManyField(to=User)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


def create_organization(sender, instance, created, *args, **kwargs):
    if created:
        name = f'{instance.firstname}-organization'
        # user = instance
        obj = Organizations.objects.create(name = name)
        obj.orgId = obj.id
        obj.user.add(instance)
        obj.save()
        instance.userId = instance.id
        instance.save()
        
# def edit_orgId(sender, instance, created, *args, **kwargs):
#     if created:
#         instance.orgId = instance.id
#         instance.save()

post_save.connect(create_organization, sender=User)
# post_save.connect(create_organization, sender=Organizations)
    



