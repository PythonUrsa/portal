import ast
from django.db import models
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from rest_framework.authtoken.models import Token
from djangotoolbox.fields import ListField
from .forms import StringListField
from server.local_settings import *


# from rest_framework.permissions import IsAuthenticatedOrReadOnly

GENDER_CHOICES = (
    ('MM', 'Male'),
    ('FF', 'Female'),
    ('TT', 'Transgender'),
    ('II', 'Intersex'),
    ('GN', 'Gender Neutral'),
    ('GQ', 'Genderqueer'),
    ('CC', 'Cisgender'),
    ('BB', 'Bigender'),
    ('PP', 'Pangender')
)


class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given user email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, last_seen=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class KnackUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    picture = models.ImageField(upload_to='avatar', null=True, blank=True)
    gender = models.CharField(max_length=2, null=True, blank=True, choices=GENDER_CHOICES)
    age = models.SmallIntegerField(default=20, blank=True)
    college = models.ForeignKey('College', blank=True, null=True)
    year = models.ForeignKey('Year', blank=True, null=True)
    grand_total = models.FloatField(default=0.0, blank=False)

    about_me = models.TextField(null=True, blank=True)
    payment_venmo = models.CharField(max_length=255, null=True, blank=True)
    payment_paypal = models.CharField(max_length=255, null=True, blank=True)
    public_profile_url = models.CharField(max_length=255, null=True, blank=True)
    reasons = ListField(default=['I\'m an awesome knacker',
                                 'Who absolutely loves what I do',
                                 'I\'m fun, fair and honest',
                                 'I\'ll do a great job everytime',
                                 'you\'ll really love your knack',
                                 ])

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_seen = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_online(self):
        try:
            if (timezone.now() - self.last_seen).seconds / 60 < 30:
                return True
        except:
            return False
        return False

    @property
    def full_name(self):
        return self.get_full_name()


class SocialLink(models.Model):
    user = models.OneToOneField('KnackUser', blank=False, null=False)
    twitter = models.CharField(max_length=255, blank=True, null=True)
    facebook = models.CharField(max_length=255, blank=True, null=True)
    instagram = models.CharField(max_length=255, blank=True, null=True)
    googleplus = models.CharField(max_length=255, blank=True, null=True)


class Feedback(models.Model):
    user = models.ForeignKey('KnackUser', blank=False)
    rating = models.SmallIntegerField()
    review = models.CharField(max_length=128, blank=True)
    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.user


class Description(models.Model):
    user = models.ForeignKey('KnackUser', blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)


class College(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __unicode__(self):
        return self.name


class Year(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __unicode__(self):
        return self.name


class RegisterEmail(models.Model):
    uuid = models.CharField(null=False, blank=False, max_length=64)
    email = models.EmailField(null=False, blank=False)

    def __unicode__(self):
        return self.email


@receiver(post_save, sender=KnackUser)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)
        instance.save()