from django import forms
from .models import Song

# singup
class Signup(forms.Form):
    # 每个参数都要require，然后定义min_length
    full_name = forms.CharField(min_length=5, required=True)
    email = forms.EmailField(required=True)
    # 如何使用PasswordInput的widget？widget=forms.PasswordInput
    password = forms.CharField(min_length=5, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(min_length=5, required=True, widget=forms.PasswordInput)

class Login(forms.Form):
    # email = forms.EmailField(required=True)
    username = forms.CharField(min_length=5, required=True)
    password = forms.CharField(min_length=5, required=True, widget=forms.PasswordInput)


class SongEditForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["track","artist","album","length","playlist_name"]
        exclude = []