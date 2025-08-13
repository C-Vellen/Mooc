from django import forms


class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom ou pseudo ", max_length=30)
    password = forms.CharField(label="Mot de passe ", widget=forms.PasswordInput)
    new = forms.BooleanField(
        label="Créer un nouveau compte ? ",
        required=False,
    )
