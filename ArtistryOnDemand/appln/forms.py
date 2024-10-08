from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Artist, User as CustomUser

class CustomUserSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    phone_number = forms.CharField(max_length=20)
    address_line1 = forms.CharField(max_length=255)
    address_line2 = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=255)
    province = forms.CharField(max_length=255)
    country = forms.CharField(max_length=255)
    
    class Meta:
        model = User  # This links to Django's auth_user model
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            custom_user = CustomUser.objects.create(
                user_id=user.id,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
                phone_number=self.cleaned_data['phone_number'],
                address_line1=self.cleaned_data['address_line1'],
                address_line2=self.cleaned_data.get('address_line2', ''),
                city=self.cleaned_data['city'],
                province=self.cleaned_data['province'],
                country=self.cleaned_data['country'],
                username=user.username,
                password=user.password,
                date_of_birth=None  
            )
            custom_user.save()
            
        return user


class ArtistSignupForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = Artist
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        artist = super().save(commit=False)
        
        # Create the User
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

        # Now save the Artist record
        artist.password = user.password  # Store the hashed password in the Artist model too
        if commit:
            artist.save()
        return artist
    
class ArtistLoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)