from django import forms
from social_profiles.models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('email', 'first_name', 'last_name', 'username', 'avatar')
