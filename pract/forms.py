from django import forms
from django.utils import timezone
from pract.models import Category
from django.contrib.auth.models import User

class VoteForm(forms.Form):
    voteFor = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        self.fields['voteFor'].label = 'Голос'

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логін'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Логін не існує!')

        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('Невірний пароль!')

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_check',
            'first_name',
            'last_name',
            'email'
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логін'
        self.fields['password'].label = 'Пароль'
        self.fields['password'].help_text = 'Придумайте пароль'
        self.fields['password_check'].label = 'Повторіть пароль'
        self.fields['first_name'].label = "Ім\'я"
        self.fields['last_name'].label = 'Прізвище'
        self.fields['email'].label = 'Ваша поштова скринька'
        self.fields['email'].help_text = 'Будь ласка, вказуйте справжній email'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Логін вже існує!')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Користувач з таким email вже зареєстрований!')
        if password != password_check:
            raise forms.ValidationError('Ваші паролі не співпадать! Спробуйте ще раз!')





class PetitonCrForm(forms.Form):
    title = forms.CharField(max_length=100)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    info = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(PetitonCrForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = 'Назва'
        self.fields['category'].label = 'Категорія'
        self.fields['category'].help_text = 'Тема, за якою вашу петицію буде легше знати на нашому сайті'
        self.fields['info'].label = 'Зміст петиції'
        self.fields['info'].help_text = 'Зміст вашої пропозиції до влади'