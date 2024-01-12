
from django.conf import settings
from .models import Nutrition,  Vaccinations, RecommendedNutritionAndVaccination
from profiles.models import  ParentProfile
from celery import shared_task
from django.forms.models import model_to_dict
from email.mime.image import MIMEImage
from django.contrib.sites.models import Site

current_site = Site.objects.get_current()
domain = current_site.domain



def create_all_recommendation(age, age_unit):
    try:
        print(age,age_unit)
        suitable_nutritions = Nutrition.objects.filter(
            min_age__lte=age, max_age__gte=age, age_unit=age_unit
        )
        suitable_vaccinations = Vaccinations.objects.filter(
            min_age__lte=age, max_age__gte=age, age_unit=age_unit
        )

        recommendation = RecommendedNutritionAndVaccination.objects.filter(
                min_age__lte=age, max_age__gte=age, age_unit=age_unit
                ).first()

        if recommendation:
            current_nutritions = set(recommendation.nutrition.all())
            current_vaccinations = set(recommendation.vaccination.all())
            vaccine_min_age = min([vaccine.min_age for vaccine in suitable_vaccinations])
            vaccine_max_age = max([vaccine.max_age for vaccine in suitable_vaccinations])
            nutrition_min_age = min([nutrition.min_age for nutrition in suitable_nutritions])
            nutrition_max_age = max([nutrition.max_age for nutrition in suitable_nutritions])


            if current_nutritions != suitable_nutritions or current_vaccinations != suitable_vaccinations:
                recommendation.nutrition.set(suitable_nutritions)
                recommendation.vaccination.set(suitable_vaccinations)
                recommendation.min_age=min(vaccine_min_age,nutrition_min_age)
                recommendation.max_age=max(vaccine_max_age,nutrition_max_age)
                recommendation.save()
        else:
            recommendation = RecommendedNutritionAndVaccination.objects.filter(
                min_age__lte=age, max_age__gte=age, age_unit=age_unit
                ).first()
            recommendation.nutrition.set(suitable_nutritions)
            recommendation.vaccination.set(suitable_vaccinations)
            recommendation.save()

        print("recommendation created")
        return recommendation

    except Exception as e:
        print(e)

from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives
from django.contrib.staticfiles.storage import staticfiles_storage


@shared_task
def email_user(subject, from_email=None, **kwargs):
    """Send an email to this user."""
    recipient_list = [kwargs.get('email')]
    context = kwargs.get('context')
    html = kwargs.get('html')
    html_message = render_to_string(html, context)
    from_email = from_email or settings.EMAIL_HOST_USER

    msg = EmailMultiAlternatives(subject, '', from_email, recipient_list)
    msg.attach_alternative(html_message, "text/html")

    image_path = staticfiles_storage.path('vaccination.png')

    with open(image_path, 'rb') as img:
        msg_image = MIMEImage(img.read())
        msg.attach(msg_image)

    msg_image.add_header('Content-ID', '<image1>')

    try:
        msg.send()
        print("email sent")
    except Exception as e:
        print(e, "email not sent", "***********")


@shared_task
def send_recommendation_to_parents():
    for parent in ParentProfile.objects.prefetch_related("child_profile").all():
        context={}
        for child in parent.child_profile.all():
            age = child.age
            age_unit = "years"
            if age < 1:
                age = child.age_in_months
                age_unit = "months"
                if age < 1:
                    age = child.age_in_days
                    age_unit = "days"

            rec = create_all_recommendation(age, age_unit)

            rec_nutrition = []
            for nutrition in rec.nutrition.all():
                nutrition_dict = model_to_dict(nutrition, exclude=["image"])
                nutrition_dict['image'] = domain + nutrition.image.url
                rec_nutrition.append(nutrition_dict)

            rec_vaccination = []
            for vaccination in rec.vaccination.all():
                vaccination_dict = model_to_dict(vaccination, exclude=["image"])
                vaccination_dict['image'] = domain + vaccination.image.url
                rec_vaccination.append(vaccination_dict)

            context = {
                'child_name': child.full_name,
                'rec_nutrition': rec_nutrition,
                'rec_vaccination': rec_vaccination
            }
            print(context, "***********")
            email_user.delay(
                subject="suggestion",
                email=parent.email,
                context=context,
                html="nutritions.html"
            )
            print("recommendation sent to parents")




from datetime import datetime, timedelta


@shared_task
def send_vaccination_notifications():
    for parent in ParentProfile.objects.prefetch_related("child_profile").all():
        suitable_vaccinations=[]
        for child in parent.child_profile.all():
            age = child.age
            age_unit = "years"
            if age < 1:
                age = child.age_in_months
                age_unit = "months"
                if age < 1:
                    age = child.age_in_days
                    age_unit = "days"

            suitable_vaccinations = Vaccinations.objects.prefetch_related("places").filter(
                min_age__lte=age, max_age__gte=age, age_unit=age_unit
            )
            upcoming_vaccinations = []

            for vaccine in suitable_vaccinations:
                vaccine_dict = model_to_dict(vaccine, exclude=["image"])
                vaccine_dict['image'] =  domain + vaccine.image.url
                places=[]
                for place in vaccine.places.all():
                    days_until_vaccination = (place.vaccination_date - datetime.now().date()).days
                    if days_until_vaccination in [1, 2, 3] and vaccine.min_age <= age <= vaccine.max_age:
                        
                        place_dict = model_to_dict(place, exclude=["vaccine"])  
                        places.append( place_dict )
                if places:  
                    vaccine_dict['places'] = places
                    upcoming_vaccinations.append(vaccine_dict)
            print(upcoming_vaccinations,"***********")

            if upcoming_vaccinations:
                context = {
                    'child_name': child.full_name,
                    'vaccines': upcoming_vaccinations,
                }
                email_user.delay(
                    subject="Vaccination reminder",
                    email=parent.email,
                    context=context,
                    html="vaccination.html"
                )
                print("Vaccination reminder sent to parents")