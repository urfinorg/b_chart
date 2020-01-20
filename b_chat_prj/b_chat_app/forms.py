from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput( attrs={'id':'login_form_user'} ),
                                label='*Login', max_length=30 )
    password = forms.CharField(widget=forms.PasswordInput( attrs={'id':'login_form_password'} ),
                               label='*Password' )


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def is_valid(self):
        #pass
        #if not (uniq user)
        #if (password missmatch)
        return True


    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    # def clean(self):
    #     cleaned_data = super(UserCreationForm, self).clean()



    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError(
    #             self.error_messages['password_mismatch'],
    #             code='password_mismatch',
    #         )
    #     return password2




# class RegistrationForm(forms.Form):
#     class Meta:
#         model = User
#         fields = ("username", "email", "password1", "password2")
#
#     user_name = forms.CharField(widget=forms.TextInput(attrs={'id':'reg_form_user',
#                                                               'value':'demo-user'}),
#                                 label='*login', max_length=30 )
#     mail = forms.EmailField( widget=forms.TextInput(attrs={'value':'simple@demo.ru'}),
#                              label='*mail',)
#
#     password1 = forms.CharField(widget=forms.PasswordInput( attrs={'id': 'reg_form_password'} ),
#                                required=False, label='Password')
#     password2 = forms.CharField(widget=forms.PasswordInput( attrs={'id': 'reg_form_confirm'} ),
#                                        required=False, label='confirm password')
#
#     def save(self, commit=True):
#         user = super(RegistrationForm, self).save(commit=False)
#         user.email = self.cleaned_data["email"]
#         if commit:
#             user.save()
#         return user
#
#     def clean(self):
#         cleaned_data = super(RegistrationForm, self).clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")
#
#         if password != confirm_password:
#             raise forms.ValidationError(
#                 "password and confirm_password does not match"
#             )


