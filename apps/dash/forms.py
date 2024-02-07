from django import forms


class GreekStudyAccountSetupForm(forms.Form):
    gs_email = forms.CharField(max_length=100)
    gs_password = forms.CharField(max_length=100)

    # set field labels
    gs_email.label = "Greek Study Email"
    gs_password.label = "Greek Study Password"

