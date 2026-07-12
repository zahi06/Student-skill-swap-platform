from django import forms
from .models import SkillOffer, SkillRequest


class SkillOfferForm(forms.ModelForm):
    class Meta:
        model = SkillOffer
        fields = ['skill', 'proficiency_level']


class SkillRequestForm(forms.ModelForm):
    class Meta:
        model = SkillRequest
        fields = ['skill', 'desired_proficiency']