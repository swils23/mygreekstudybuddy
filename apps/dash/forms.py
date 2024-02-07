from django import forms


class GreekStudyAccountSetupForm(forms.Form):
    gs_email = forms.CharField(required=True, max_length=100)
    gs_password = forms.CharField(required=True, max_length=100)
    gs_userID = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"id": "gs_userID"}))

    # set field labels
    gs_email.label = "Greek Study Email"
    gs_password.label = "Greek Study Password"
    gs_userID.label = "Greek Study User ID"
