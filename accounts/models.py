# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class User(AbstractUser):
#     phone = models.CharField(max_length=15, blank=True)
#     address = models.TextField(blank=True)
#     city = models.CharField(max_length=100, blank=True)
#     state = models.CharField(max_length=100, blank=True)
#     zip_code = models.CharField(max_length=10, blank=True)
#     country = models.CharField(max_length=100, blank=True)
    
#     def __str__(self):
#         return self.email

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add your custom fields here
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    
    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='accounts_user_set',  # Add this
        related_query_name='accounts_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='accounts_user_set',  # Add this
        related_query_name='accounts_user',
    )
    
    def __str__(self):
        return self.username