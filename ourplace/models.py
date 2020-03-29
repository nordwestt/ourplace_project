from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your models here.



class UserProfile(models.Model): 
    EMAIL_MAX_LENGTH = 128
    # Links UserProfile to a User model instance. 
    # I think, (I hope) this handles username, password and email
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    #add a slug field as a url to peoples profiles??

    # The additional attributes we wish to include. 
    picture = models.ImageField(upload_to='profile_images', blank=True)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs): 
        self.slug = slugify(self.user) 
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self): 
        return self.user.username

class Canvas(models.Model):
    TITLE_MAX_LENGTH = 128

    #keep slugs in to use as urls???
    slug = models.SlugField(unique=True)

    title = models.CharField(max_length=TITLE_MAX_LENGTH, unique=True) 
    size = models.IntegerField(default=10) # (ARE WE MAKING THEM SQUARE OR SHOULD WE SEPARATE HEIGHT AND WIDTH)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE) # Get the user that's creating it somehow??
    colour_palette =  models.IntegerField(default =0) #set to an integer for testing
    url = models.URLField()
    canvas_image = models.ImageField(upload_to='canvas_images',blank=True) #Should open a blank canvas?
    bitmap = models.BinaryField(default=None, blank=True, null=True)
    
    # cooldown in number of seconds
    cooldown = models.IntegerField(default=60)

    def save(self, *args, **kwargs): 
        self.slug = slugify(self.title) 
        super(Canvas, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = 'canvases'

class CanvasAccess(models.Model):
    canvas = models.ForeignKey(Canvas, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    placeTime = models.DateTimeField()
    
    class Meta:
        verbose_name_plural = 'CanvasAccess'