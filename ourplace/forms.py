from django import forms
from ourplace.models import CanvasAccess, Canvas, UserProfile
from django.contrib.auth.models import User 

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
    size = forms.IntegerField(initial=10, label="Size", widget=forms.NumberInput(attrs=class_attrs))
    colour_palette = forms.IntegerField(initial=0, label="Colour Palette", widget=forms.NumberInput(attrs=class_attrs))
    cooldown = forms.IntegerField(initial=60, label="Cooldown Time", widget=forms.NumberInput(attrs=class_attrs))
    visibility = forms.CharField(initial=Canvas.PRIVATE, label="Visibility", widget=forms.Select(attrs=class_attrs, choices = Canvas.VISIBILITY_CHOICES))
    class Meta:
        model = Canvas
        fields = ('title', 'size', 'colour_palette', 'cooldown', 'visibility')

class CanvasEditForm(forms.ModelForm):
    cooldown = forms.IntegerField(initial=60, label="Cooldown Time", widget=forms.NumberInput(attrs=class_attrs))
    visibility = forms.CharField(initial=Canvas.PRIVATE, label="Visibility", widget=forms.Select(attrs=class_attrs, choices=Canvas.VISIBILITY_CHOICES))
    class Meta:
        model = Canvas
        fields = ('cooldown', 'visibility')

class CanvasAccessForm(forms.ModelForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs=class_attrs))

    class Meta:
        model = CanvasAccess
        fields = ('username', )


    def clean(self):
        cd = self.cleaned_data
        if not User.objects.filter(username=cd.get('username')).exists:
            self.add_error('username', 'User not found')
        return cd

