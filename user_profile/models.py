from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Discount(models.Model):
    offer_name = models.CharField(max_length=100)
    discount_percentage = models.PositiveIntegerField()
    discount_amount_threshold = models.PositiveIntegerField()
    offer_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.offer_name


class UserProfile(models.Model):
    """
    A user profile model for maintaining default
    delivery information and order history
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
        # Existing users: just save the profile
        instance.userprofile.save()
        # print("Created Profile")
