__author__ = 'Elliot'

from django import forms

# 定义表单模型


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='',
        error_messages={'required': '请输入用户名'},
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'username',
            }
        )
    )
    password = forms.CharField(
        required=True,
        label='',
        error_messages={'required': '请输入密码'},
        max_length=32,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'password',
            }
        )
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError('用户名和密码为必填项')
        else:
            cleaned_data = super(LoginForm, self).clean()

