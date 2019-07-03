from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from companies.models import Company


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='contacts')
    position = models.CharField(max_length=100)
    primary = models.BooleanField(default=False)

    email = models.EmailField()
    phone_number = PhoneNumberField(blank=True)

    notes = models.TextField(blank=True)
    updated = models.DateField(auto_now=True)
    # sponsorships field

    def __str__(self):
        return f"Name: {self.name()}, Company: {self.company}, Position: {self.position}, Email: {self.email}, Phone: {self.phone_number}"

    def name(self):
        return f"{self.first_name} {self.last_name}"
