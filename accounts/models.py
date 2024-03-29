from django.db import models
import datetime
from fileinput import filename
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
# from distutils.command.upload import upload
from django.contrib.auth.models import User
# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, state, district, contact, address, land_mark, role, pincode, is_customer, password=None):

        if not email:
            raise ValueError('User must have an email address')

        # if not username:
        #     raise ValueError('User must have an username')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            # username=username,
            state=state,
            district=district,
            contact=contact,
            address=address,
            land_mark=land_mark,
            role=role,
            pincode=pincode,
            is_customer=is_customer,

        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, email, **extra_fields):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password, **extra_fields

        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)


class Account(AbstractBaseUser,PermissionsMixin):
    state_choices = (('kerala', 'kerala'), ('demo', 'demo'), ('None', 'None'))
    status_choices = (('Approved', 'Approved'), ('Pending', 'Pending'), ('None', 'None'))
    role_choices = (('is_customer', 'is_customer'),('is_admin', 'is_admin'), ('is_superadmin', 'is_superadmin'),('is_driverreg', 'is_driverreg'))
    district_choices = (
        ('Kozhikode', 'Kozhikode'),
        ('Malappuram', 'Malappuram'),
        ('Kannur', 'Kannur'),
        ('Trivandrum', 'Trivandrum'),
        ('Palakkad', 'Palakkad'),
        ('Thrissur', 'Thrissur'),
        ('Kottayam', 'Kottayam'),
        ('Alappuzha', 'Alappuzha'),
        ('Idukki', 'Idukki'),
        ('Kollam', 'Kollam'),
        ('Ernakulam', 'Ernakulam'),
        ('Wayanad', 'Wayanad'),
        ('Kasaragod', 'Kasaragod'),
        ('Pathanamthitta', 'Pathanamthitta'),
        ('Thiruvananthapuram', 'Thiruvananthapuram'),
        ('None', 'None'),
    )

    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')
    # username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    contact = models.BigIntegerField(default=0)
    state = models.CharField(max_length=100, choices=state_choices, default='kerala')
    district = models.CharField(max_length=100, choices=district_choices, default='None')
    address = models.CharField(max_length=200, default='')
    land_mark = models.CharField(max_length=50)
    pincode = models.BigIntegerField(default=0)

    # password = models.CharField(max_length=200)

    role = models.CharField(max_length=100, choices=role_choices)
    status = models.CharField(default='Completed', max_length=40)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_driverreg = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    # last_login = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'state', 'district', 'contact', 'address','land_mark', 'role', 'pincode', 'is_customer']
    # REQUIRED_FIELDS = ['username','password']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True