from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, age, contact_number, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name or not last_name:
            raise ValueError('Users must provide their first name and last name')
        if not age:
            raise ValueError('Users must provide their age')
        if not contact_number:
            raise ValueError('Users must provide their contact number')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            age=age,
            contact_number=contact_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, first_name, last_name, age, contact_number, password=None):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            age=age,
            contact_number=contact_number,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    contact_number = models.CharField(max_length=14)  # Assuming the format is XXX-XXXXXXX
    password = models.CharField(max_length=128)  # Storing hashed password
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=True)  # New field for verification
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'age', 'contact_number']
    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    tags = models.CharField(max_length=100)
    image_location = models.CharField(max_length=200)
    # image_location = models.ImageField(upload_to='item_images/')
    url = models.URLField()

    def __str__(self):
        return self.item_name



