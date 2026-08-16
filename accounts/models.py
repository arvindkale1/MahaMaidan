from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model.

    role drives what a logged-in user can do:
      - CUSTOMER: browse turfs and make bookings
      - OWNER:    list/manage their own turfs and view bookings on them
      - ADMIN:    full platform control (also use is_staff/is_superuser
                  for Django admin access)
    """

    class Role(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        OWNER = 'OWNER', 'Turf Owner'
        ADMIN = 'ADMIN', 'Platform Admin'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CUSTOMER)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_owner(self):
        return self.role == self.Role.OWNER

    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER
