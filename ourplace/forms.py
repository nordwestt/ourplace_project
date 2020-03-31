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
        exclude = ('slug', 'owner', 'url', 'bitmap', 'views')
        #fields = ('title', 'size', 'colour_palette', 'cooldown', 'visibility')

class CanvasEditForm(forms.ModelForm):
    cooldown = forms.IntegerField(initial=60, label="Cooldown Time", widget=forms.NumberInput(attrs=class_attrs))
    visibility = forms.CharField(initial=Canvas.PRIVATE, label="Visibility", widget=forms.Select(attrs=class_attrs, choices=Canvas.VISIBILITY_CHOICES))
    class Meta:
        model = Canvas
        exclude = ('slug', 'title', 'size', 'owner', 'colour_palette', 'url', 'views')

class CanvasAccessForm(forms.ModelForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(attrs=class_attrs))

    class Meta:
        model = CanvasAccess
        exclude = ('user', 'canvas', 'placeTime')


    def clean(self):
        cd = self.cleaned_data
        if not User.objects.filter(username=cd.get('username')).exists:
            self.add_error('username', 'User not found')
        return cd

# class CategoryForm(forms.ModelForm):
#     name = forms.CharField(max_length=Category.NAME_MAX_LENGTH,
#     help_text="Please enter the category name.")
#     views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#     likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
#     slug = forms.CharField(widget=forms.HiddenInput(), required=False)

#     # An inline class to provide additional information on the form.
#     class Meta:
#         # Provide an association between the ModelForm and a model
#         model = Category
#         fields = ('name',)

# class PageForm(forms.ModelForm):
#     title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH,
#     help_text="Please enter the title of the page.")
#     url = forms.URLField(max_length=200,
#     help_text="Please enter the URL of the page.")
#     views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

#     def clean(self): 
#         cleaned_data = self.cleaned_data 
#         url = cleaned_data.get('url')
        
#         # If url is not empty and doesn't start with 'http://', 
#         # then prepend 'http://'. 
#         if url and not url.startswith('http://'): 
#             url = f'http://{url}' 
#             cleaned_data['url'] = url
#         return cleaned_data

#     class Meta:
#         # Provide an association between the ModelForm and a model
#         model = Page

#         # What fields do we want to include in our form?
#         # This way we don't need every field in the model present.
#         # Some fields may allow NULL values; we may not want to include them.
#         # Here, we are hiding the foreign key.
#         # we can either exclude the category field from the form,
#         exclude = ('category',)
#         # or specify the fields to include (don't include the category field).
#         #fields = ('title', 'url', 'views')
