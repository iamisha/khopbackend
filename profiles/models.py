from datetime import date
from django.db import models
from accounts.models import Users
from recommendation.models import Vaccinations
# Create your models here.


class HealthProfessionalProfile(models.Model):
    user=models.OneToOneField(Users,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=200,null=True,blank=True,default="")
    profile_verification=models.IntegerField(default=25)
    profile_pic=models.ImageField(upload_to="profile_pics/",null=True,blank=True)
    document=models.FileField(upload_to="verification_documents/",null=True,blank=True)
    liscence_no=models.CharField(max_length=50,default="")
    yrs_of_experience=models.IntegerField(default=0)


    def save(self, *args, **kwargs):
        if not self.pk:  # This checks if the instance has been saved before
            self.full_name = self.user.email
        super().save(*args, **kwargs)


    def __str__(self) -> str:
        return self.full_name
    
class ParentProfile(models.Model):
    user = models.ForeignKey(HealthProfessionalProfile, on_delete=models.CASCADE, related_name="parent_profile")
    full_name = models.CharField(max_length=200, null=True, blank=True, default="")
    profile_pic = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    date_of_birth = models.DateField(null=True, blank=True)

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def __str__(self) -> str:
        return self.full_name

class ChildProfile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.ForeignKey(ParentProfile, on_delete=models.CASCADE, related_name="child_profile")
    full_name = models.CharField(max_length=200, null=True, blank=True, default="")
    date_of_birth = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default="M")
    past_vaccinations=models.ManyToManyField(Vaccinations,related_name="past_vaccinations",blank=True)

    @property
    def age(self):
        today = date.today()
        dob = self.date_of_birth.date()  
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    @property
    def age_in_months(self):
        today = date.today()
        dob = self.date_of_birth.date()  
        return (today.year - dob.year)*12 + today.month - dob.month - ((today.day) < (dob.day))

    @property
    def age_in_days(self):
        today = date.today()
        dob = self.date_of_birth.date()  
        return (today - dob).days

    @property
    def age_in_weeks(self):
        today = date.today()
        dob = self.date_of_birth.date() 
        return (today - dob).days//7

    
    def __str__(self) -> str:
        return self.full_name





