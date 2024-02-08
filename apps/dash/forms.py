from django import forms


class GreekStudyAccountSetupForm(forms.Form):
    gs_email = forms.CharField(required=True, max_length=100)
    gs_password = forms.CharField(required=True, max_length=100)
    # This field is disabled on the front end, put placeholder text "click 'get' to retrieve user ID"
    gs_userID = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"id": "gs_userID"}))
    gs_userID.widget.attrs["placeholder"] = "Click 'Get' to fill"

    # set field labels
    gs_email.label = "GreekStudy Email"
    gs_password.label = "GreekStudy Password"
    gs_userID.label = "GreekStudy User ID"
