from django import forms
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.formfields import PhoneNumberField

from ..organisations.models import Organisation
from .models import Profile, NotificationSettings


class BaseUserProfileSignupForm(forms.Form):

    phone = PhoneNumberField(
        label=_('Your mobile phone number'),
        help_text=_('Please enter your mobile phone number starting with the country code. E.g. "+431234526"'),
        required=False
    )

    def signup(self, request, user):
        # save phone number to profile
        profile, created = Profile.objects.get_or_create(
            user=user
        )
        phone_number = self.cleaned_data['phone']
        if phone_number:
            profile.phone_number = phone_number
            profile.save()


class UserProfileSignupForm(BaseUserProfileSignupForm):

    org = forms.ModelChoiceField(
        queryset=Organisation.objects.all(),
        label=_('Organisation'),
        help_text=_('You can become a member of an existing organisation now or create your own at a later point.'),
        required=False
    )

    def signup(self, request, user):
        super().signup(request, user)

        # if given add to organisation
        org = self.cleaned_data.get('org')
        if org:
            org.add_member(user)


class NotificationSettingsForm(forms.ModelForm):

    class Meta:
        model = NotificationSettings
        fields = [
            'point',
            'point_radius',
            'notification_type',
            'organisations',
            'issue_types',
        ]
        widgets = {
            'point': forms.HiddenInput
        }
        help_texts = {
            'organisations': _('Notifications can be filtered by Organisation (default: all).'),
            'issue_types': _('Filter by issue type (default: all).'),
            'notification_type': _('Choose how you want to be notified.')
        }
