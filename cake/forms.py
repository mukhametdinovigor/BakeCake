from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Customer


class ConstructCakeForm(forms.Form):
    LEVEL_CHOICES = [
        ('level1', '1 уровень'),
        ('level2', '2 уровня'),
        ('level3', '3 уровня')
    ]
    LEVEL_SHAPES = [
        ('circle', 'Круг'),
        ('square', 'Квадрат'),
        ('rectangle', 'Прямоугольник')
    ]

    TOPPINGS = [
        ('without_toppings', 'Без топпинга'),
        ('white_souse', 'Белый соус'),
        ('caramel_syrup', 'Карамельный сироп'),
        ('maple_syrup', 'Кленовый сироп'),
        ('strawberry_syrup', 'Клубничный сироп'),
        ('blueberry_syrup', 'Черничный сироп'),
        ('milk_choco', 'Молочный шоколад')
    ]
    BERRIES = [
        ('blackberry', 'Ежевика'),
        ('raspberry', 'Малина'),
        ('blueberry', 'Голубика'),
        ('Strawberry', 'Клубника')
    ]

    DECOR = [
        ('without_decor', 'Без декора'),
        ('pistachio', 'Фисташки'),
        ('meringue', 'Безе'),
        ('funduk', 'Фундук'),
        ('pecan', 'Пекан'),
        ('Marshmallow', 'Маршмеллоу'),
        ('marzipan', 'Марципан'),
    ]

    levels = forms.ChoiceField(label='Количество уровней', choices=LEVEL_CHOICES, widget=forms.RadioSelect)
    level_shapes = forms.ChoiceField(label='Форма уровней', choices=LEVEL_SHAPES, widget=forms.RadioSelect)
    toppings = forms.ChoiceField(label='Топпинг', choices=TOPPINGS, widget=forms.RadioSelect)
    berries = forms.MultipleChoiceField(label='Ягоды', choices=BERRIES, widget=forms.CheckboxSelectMultiple)
    decor = forms.MultipleChoiceField(label='Декор', choices=DECOR, widget=forms.CheckboxSelectMultiple)
    lettering = forms.CharField(label='Мы можем разместить на торте любую надпись, например: «С днем рождения!»', max_length=500)


class AdvancedInfoForm(forms.Form):
    order_comment = forms.CharField(label='Комментарий к заказу', max_length=500, widget=forms.TextInput)
    address = forms.CharField(label='Адрес доставки', max_length=500)
    date = forms.DateField(label='Дата доставки', widget=forms.DateInput)
    time = forms.TimeField(label='Время доставки')


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

        self.fields['username'].label = 'Юзернейм'
        self.fields['username'].widget.attrs.update({'placeholder': ''})

        self.fields['password'].label = 'Пароль'
        self.fields['password'].widget.attrs.update({'placeholder': ''})


class UserCreationWithEmailForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Customer
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phonenumber')

    def save(self, commit=True):
        user = super(UserCreationWithEmailForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Юзернейм'
        self.fields['username'].widget.attrs.update({'placeholder': ''})
        self.fields['username'].help_text = 'Обязательное поле. Только английские \
                                             буквы, цифры и символы @/./+/-/_'

        self.fields['first_name'].label = 'Имя'
        self.fields['first_name'].widget.attrs.update({'placeholder': ''})

        self.fields['last_name'].label = 'Фамилия'
        self.fields['last_name'].widget.attrs.update({'placeholder': ''})

        self.fields['email'].label = 'Почта'
        self.fields['email'].widget.attrs.update({'placeholder': ''})

        self.fields['password1'].label = 'Пароль'
        self.fields['password1'].widget.attrs.update({'placeholder': ''})
        self.fields['password1'].help_text = 'Обязательное поле. От восьми символов, не только \
                                              цифры, не должен совпадать с другими полями'
        
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['password2'].widget.attrs.update({'placeholder': ''})
        self.fields['password2'].help_text = 'Обязательное поле'

        self.fields['phonenumber'].label = 'Номер телефона'
        self.fields['phonenumber'].widget.attrs.update({'placeholder': ''})
