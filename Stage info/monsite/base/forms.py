from django import forms
from .models import CustomUser



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['gender', 'interet', 'age']
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 18 :
            age = 18
            
        elif age > 99 :
            age = 99
            
        return age