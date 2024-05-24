from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Farmer(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('manager', 'Manager'),
    ]

    fullname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    address = models.TextField()
    farm_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(Group, blank=True)
    user_permissions = models.ManyToManyField(Permission, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.fullname

    def get_short_name(self):
        return self.fullname.split(' ')[0]

    class Meta:
        ordering = ('-date_joined',)


class Cow(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    cow_id = models.AutoField(primary_key=True)
    health_status = models.CharField(max_length=100)

    def __str__(self):
        return f"Cow {self.cow_id} - {self.health_status}"

class SensorData(models.Model):
    cow = models.ForeignKey(Cow, on_delete=models.CASCADE)
    temperature = models.FloatField()
    steps = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SensorData for Cow {self.cow.cow_id} at {self.timestamp}"

