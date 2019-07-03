from django import forms

from .models import Tier, Perk, Hackathon, Sponsorship, Lead
from companies.models import Company
from contacts.models import Contact
from ckeditor.widgets import CKEditorWidget

class HackathonForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control col-md-6 col-lg-4", "placeholder": "Name"}
        ),
    )

    date = forms.DateField(
        widget=forms.SelectDateWidget(
            attrs={"class": "form-control cold-md-6 cold-lg-4"}
        )
    )

    fundraising_goal = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control cold-md-6 cold-lg-4"})
    )

    class Meta:
        model = Hackathon
        fields = ("name", "date", "fundraising_goal")


class TierForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control col-md-6 col-lg-4", "placeholder": "Name"}
        ),
    )

    hackathon = forms.ModelChoiceField(
        required=True,
        queryset=Hackathon.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "custom-select col-md-6 col-lg-4",
                "placeholder": "Hackathon",
            }
        ),
    )

    class Meta:
        model = Tier
        fields = ("name", "hackathon")


class PerkForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={"class": "form-control col-md-6 col-lg-4", "placeholder": "Name"}
        ),
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control col-md-9 col-lg-6",
                "placeholder": "Description",
            }
        ),
    )

    hackathon = forms.ModelChoiceField(
        required=True,
        queryset=Hackathon.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "custom-select col-md-6 col-lg-4",
                "placeholder": "Hackathon",
            }
        ),
    )

    class Meta:
        model = Perk
        fields = ("name", "description", "hackathon")


class SponsorshipForm(forms.ModelForm):
    hackathon = forms.ModelChoiceField(
        required=True,
        queryset=Hackathon.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "custom-select col-md-6 col-lg-4",
                "placeholder": "Hackathon",
            }
        ),
    )

    company = forms.ModelChoiceField(
        required=True,
        queryset=Company.objects.all(),
        widget=forms.Select(
            attrs={"class": "custom-select col-md-6 col-lg-4",}
        ),
    )

    contribution = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control cold-md-6 cold-lg-4", "placeholder": 0}
        )
    )

    def clean_contribution(self):
        contribution = self.cleaned_data.get('contribution')
        return contribution or 0

    status = forms.ChoiceField(
        required=True,
        choices=Sponsorship.STATUSES,
        widget=forms.Select(
            attrs={"class": "custom-select col-md-6 col-lg-4",}
        ),
    )

    tier = forms.ModelChoiceField(
        required=False,
        queryset=Tier.objects.all(),
        widget=forms.Select(attrs={"class": "custom-select col-md-6 col-lg-4",}),
    )

    perks = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Perk.objects.all(),
        widget=forms.SelectMultiple(attrs={"class": "custom-select col-md-6 col-lg-4"}),
    )

    notes = forms.CharField(
        required=False,
        widget=CKEditorWidget(
            config_name = 'default',
            attrs={"placeholder": "Notes"}
        ),
    )

    class Meta:
        model = Sponsorship
        fields = ("hackathon", "company", "contribution", "status", "tier", "perks", "notes")


class SponsorshipMarkContactedForm(SponsorshipForm):
    class Meta:
        model = Sponsorship
        fields = ("hackathon", "company", "notes",)
    
    def __init__(self, *args, **kwargs):
        super(SponsorshipMarkContactedForm, self).__init__(*args, **kwargs)
        self.fields['hackathon'].widget = forms.HiddenInput()
        self.fields['company'].widget = forms.HiddenInput()
        del self.fields['contribution']
        del self.fields['status']
        del self.fields['tier']
        del self.fields['perks']

class LeadForm(forms.ModelForm):
    sponsorship = forms.ModelChoiceField(
        required=True,
        queryset=Sponsorship.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "custom-select col-md-6 col-lg-4",
            }
        ),
    )

    contact = forms.ModelChoiceField(
        required=True,
        queryset=Contact.objects.all(),
        widget=forms.Select(
            attrs={"class": "custom-select col-md-6 col-lg-4",}
        ),
    )

    status = forms.ChoiceField(
        required=True,
        choices=Lead.STATUSES,
        widget=forms.Select(
            attrs={"class": "custom-select col-md-6 col-lg-4",}
        ),
    )

    times_contacted = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control cold-md-6 cold-lg-4", "placeholder": 1}
        )
    )

    class Meta:
        model = Lead
        fields = ("sponsorship", "contact", "status", "times_contacted")
    
    def __init__(self, hackathon, company=None, *args, **kwargs):
        super(LeadForm, self).__init__(*args, **kwargs)
        self.fields['sponsorship'].queryset = Sponsorship.objects.filter(hackathon=hackathon)
        if company:
            self.fields['contact'].queryset = Contact.objects.filter(company=company)

class LeadMarkContactedForm(LeadForm):
    class Meta:
        model = Lead
        fields = ("sponsorship", "contact",)
    
    def __init__(self, hackathon, company=None, *args, **kwargs):
        super(LeadMarkContactedForm, self).__init__(hackathon, company, *args, **kwargs)
        self.fields['sponsorship'].widget = forms.HiddenInput()
        self.fields['contact'].widget = forms.HiddenInput()
        del self.fields['status']
        del self.fields['times_contacted']