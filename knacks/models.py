from django.db import models
from django.conf import settings
from redactor.fields import RedactorField

User = settings.AUTH_USER_MODEL

KNACK_TYPES = (
    ('O', 'Offered'),
    ('W', 'Wanted'),
)

KNACK_IDEA_TYPES = (
    ('O', 'Offered'),
)


class Knack(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey('Category', null=False, blank=False)
    price = models.FloatField(default=0.0, blank=False)
    type = models.CharField(max_length=1, choices=KNACK_TYPES, null=False, blank=False)
    photo = models.ImageField(upload_to='knacks/images/', null=True, blank=True)
    video = models.ImageField(upload_to='knacks/videos/', null=True, blank=True)

    owner = models.ForeignKey(User, null=False, blank=False, related_name='knacks')

    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    def __unicode__(self):
        return u'%s\'s %s' % (self.owner, self.name)


class KnackIdea(models.Model):
    name = models.CharField('Knack headline', max_length=255, null=False, blank=False)
    description = models.TextField('Tell us more about what you do', null=True, blank=True)
    category = models.ForeignKey('Category', null=False, blank=False, verbose_name='Knack category')
    type = models.CharField(max_length=1, choices=KNACK_IDEA_TYPES, null=False, blank=False, default='O')
    schedule = models.CharField('What\'s your schedule like?', max_length=255, null=True, blank=True)

    travel_choices = ((True, 'Yes'), (False, 'No'))
    willing_to_travel = models.BooleanField('Are you willing to travel?', choices=travel_choices, default=True)
    miles_choices = (('5 miles', '5 miles'), ('10 miles', '10 miles'), ('20 miles', '20 miles'),
                     ('50+ miles', '50+ miles'), ('On Campus', 'On Campus'))
    miles = models.CharField('How many miles?', max_length=255, choices=miles_choices, default='On Campus')
    rate = models.FloatField('What is your rate?', default=0.0)
    charge_choices = (('Flat Fee', 'Flat Fee'), ('Hourly', 'Hourly'))
    how_charge = models.CharField('How do you charge?', max_length=255, choices=charge_choices, default='Hourly')
    business_model = RedactorField(verbose_name=u'Business Model', allow_file_upload=True,
                                   allow_image_upload=True, default='')

    created_at = models.DateField(auto_now_add=True)
    modified_at = models.DateField(auto_now=True)

    def __unicode__(self):
        return u'%s' % self.name


class KnackIdeaImage(models.Model):
    knack_idea = models.ForeignKey(KnackIdea)
    photo = models.ImageField(upload_to='knacks/images/', null=True, blank=True)


class Category(models.Model):
    name = models.CharField(max_length=64, null=False, blank=False)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
