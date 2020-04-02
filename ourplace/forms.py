from django import forms
from ourplace.models import CanvasAccess, Canvas, UserProfile
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class_attrs = {'class':'form-control'}

class UserForm(forms.ModelForm): 
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta: 
        model = User 
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm): 
    class Meta: 
        model = UserProfile 
        fields = ('picture',)


class CanvasForm(forms.ModelForm):
    title = forms.CharField(max_length=Canvas.TITLE_MAX_LENGTH, label = "Title", widget=forms.TextInput(attrs=class_attrs))
    size = forms.IntegerField(initial=10, label="Size (pixels)", widget=forms.NumberInput(attrs=class_attrs))
    # colour_palette = forms.IntegerField(initial=0, label="Colour Palette", widget=forms.NumberInput(attrs=class_attrs))
    cooldown = forms.IntegerField(initial=60, label="Cooldown Time (seconds)", widget=forms.NumberInput(attrs=class_attrs))
    visibility = forms.CharField(initial=Canvas.PRIVATE, label="Visibility", widget=forms.Select(attrs=class_attrs, choices = Canvas.VISIBILITY_CHOICES))
    class Meta:
        model = Canvas
        fields = ('title', 'size', 'cooldown', 'visibility') # removed  'colour_palette', from the form
    def clean(self):
        cd = super().clean()
        if cd.get('cooldown') < 0:
            self.add_error('cooldown', 'Cooldown must not be negative.')
        if cd.get('size') > 512:
            self.add_error('size', 'Size must not be greater than 512')
        if Canvas.objects.filter(slug=slugify(cd.get('title'))).exists():
            self.add_error('title', 'Canvas with this Title already exists.')


class CanvasEditForm(forms.ModelForm):
    cooldown = forms.IntegerField(initial=60, label="Cooldown Time (seconds)", widget=forms.NumberInput(attrs=class_attrs))
    visibility = forms.CharField(initial=Canvas.PRIVATE, label="Visibility", widget=forms.Select(attrs=class_attrs, choices=Canvas.VISIBILITY_CHOICES))
    class Meta:
        model = Canvas
        fields = ('cooldown', 'visibility')

    def clean(self):
        cd = super().clean()
        if cd.get('cooldown') < 0:
            self.add_error('cooldown', 'Cooldown must not be negative.')


class CanvasAccessForm(forms.ModelForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs=class_attrs))

    class Meta:
        model = CanvasAccess
        fields = ('username', )

    def clean(self):
        cd = super().clean()
        if not User.objects.filter(username=cd.get('username')).exists():
            self.add_error('username', 'User not found.')




