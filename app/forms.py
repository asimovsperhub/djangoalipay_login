from django import forms

from app.models import Userinfo


class UserForm(forms.Form):
    phone = forms.IntegerField(required=True, label='手机号')
    email = forms.EmailField(required=True, label='邮箱', widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "请输入邮箱账号", "value": ""}), max_length=50, error_messages={"required": "邮箱不能为空", "invalid": ""})

    def clean(self):

        # 用户名
        try:
            email = self.cleaned_data['email']
        except Exception as e:
            print('except: ' + str(e))
            raise forms.ValidationError("邮箱格式错误")

        # 登录验证(邮箱去重)，查看邮箱是否存在
        is_email_exist = Userinfo.objects.filter(email=email).exists()
        # is_username_exist = User.objects.filter(username=username).exists()
        if is_email_exist:
            raise forms.ValidationError("该邮箱已存在")
