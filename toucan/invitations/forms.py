from django import forms
from django.utils.translation import ugettext_lazy as _

from user_profile.forms import BaseUserProfileSignupForm
from .models import ToucanInvitation

invitation_error = forms.ValidationError(
    _('''
        There was a problem with your invitation key.
        Please contact us if you think that this might be an error.'''
    ), code='invalid_invitation'
)

class InvitedUserSignupForm(BaseUserProfileSignupForm):
    invitation_key = forms.CharField(widget=forms.HiddenInput)

    @property
    def invitation(self):
        key = self.cleaned_data.get('invitation_key')
        try:
            return ToucanInvitation.objects.get(secret_key=key)
        except ToucanInvitation.DoesNotExist:
            raise invitation_error

    def clean_invitation_key(self):
        if self.invitation.is_active():
            return self.invitation.secret_key

        raise invitation_error

    def clean(self):
        super().clean()
        invitation_email = self.invitation.email
        signup_email = self.cleaned_data.get('email')
        if invitation_email != signup_email:
            raise forms.ValidationError(
                _('''
                    The email given in the invitation does not correspond with the entered email address.
                    Please use the email address where you received the invitation.
                '''), code='invalid'
            )

    def signup(self, request, user):
        super().signup(request, user)
        self.invitation.accept(user)
        # add user to organisation
        organisation = self.invitation.organisation
        organisation.add_user_to_org(
            user,
            role=self.invitation.role
        )
