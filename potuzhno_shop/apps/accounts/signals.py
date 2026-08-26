import logging

from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import (
    user_logged_in, user_logged_out, user_login_failed
)
from django.db.models.signals import post_save

from .models import Profile


logger = logging.getLogger("security")


def client_ip(request):
    if request is None:
        return "unknown"
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")

    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    print("TRUE")
    logger.info(f"LOGIN OK user={user.username} ip={client_ip(request)}")



@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    logger.info("LOGOUT user=%s ip=%s", getattr(user, "username", "?"), client_ip(request))


@receiver(user_login_failed)
def log_login_failed(sender, credentials, request=None, **kwargs):
    logger.warning(
        "LOGIN FAILED user=%s ip=%s",
        credentials.get("username", "?"),
        client_ip(request),
    )