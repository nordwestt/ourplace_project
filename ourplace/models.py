from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your models here.



class UserProfile(models.Model): 

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    #add a slug field as a url to peoples profiles??

    # The additional attributes we wish to include. 
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self): 
        return self.user.username
    
        
class Canvas(models.Model):
    TITLE_MAX_LENGTH = 128


    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True) 
    size = models.IntegerField(default=10)
    url = models.URLField()


    class Meta: 
        verbose_name_plural = 'Canvas'


    # cooldown in number of seconds
    cooldown = models.IntegerField(default=60)

    def save(self, *args, **kwargs): 
        self.slug = slugify(self.name) 

        super(Canvas, self).save(*args, **kwargs)

        

