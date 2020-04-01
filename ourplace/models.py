from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import pickle
import base64
import numpy
from django.utils import timezone


class UserProfile(models.Model):
    EMAIL_MAX_LENGTH = 128
    # Links UserProfile to a User model instance.
    # I think, (I hope) this handles username, password and email
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # add a slug field as a url to peoples profiles??
    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Canvas(models.Model):
    TITLE_MAX_LENGTH = 128

    #keep slugs in to use as urls???
    slug = models.SlugField(unique=True)

    title = models.CharField(max_length=TITLE_MAX_LENGTH, unique=True)
    size = models.IntegerField(default=10) # (ARE WE MAKING THEM SQUARE OR SHOULD WE SEPARATE HEIGHT AND WIDTH)
    owner = models.ForeignKey(User, on_delete=models.CASCADE) # Get the user that's creating it somehow??

    colour_palette =  models.IntegerField(default =0) #set to an integer for testing
    bitmap = models.BinaryField(default=None, blank=True, null=True)

    # cooldown in number of seconds
    cooldown = models.IntegerField(default=60)

    #for hit tracking
    views = models.IntegerField(default=0)

    #thumbnails:
    thumbnail = models.ImageField(upload_to='thumbnails', blank=True)

    # public or private?
    PUBLIC = 'O' # o for open
    PRIVATE = 'C' # c for closed
    VISIBILITY_CHOICES = [ (PUBLIC, 'Public'), (PRIVATE, 'Private')]
    visibility = models.CharField(max_length=1, choices=VISIBILITY_CHOICES, default=PRIVATE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.bitmap is None:
            arr = numpy.zeros((self.size, self.size), dtype=numpy.ushort)
            bitmap_bytes = base64.b64encode(pickle.dumps(arr))
            self.bitmap = bitmap_bytes
        super(Canvas, self).save(*args, **kwargs)
        CanvasAccess.objects.get_or_create(user=self.owner,canvas=self)
        

    def __str__(self):
        return self.slug

    class Meta:
        verbose_name_plural = 'Canvases'

class CanvasAccess(models.Model):
    canvas = models.ForeignKey(Canvas, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    placeTime = models.DateTimeField(null=True)
    
    class Meta:
        verbose_name_plural = 'CanvasAccess'

    def __str__(self):
        return ("Canvas: " + self.canvas.slug + ", User: " + self.user.username + ", Placetime: " + str(self.placeTime))
