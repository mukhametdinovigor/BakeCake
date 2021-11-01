from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Customer, Level, Shape, Topping, Berry, AdditionalIngredient
from django.utils import timezone


def create_elements():
    models = (Level, Shape, Topping, Berry, AdditionalIngredient)
    elements = dict()
    for model in models:
        choices = model.objects.values_list().order_by('price')
        elements[model] = choices
    return elements


def create_choices(elements, model):
    choices = []
    for choice in elements[model]:
        choices.append((f'{choice[0]} + {choice[2]}', f'{choice[1]} + {choice[2]} руб.'))
    return choices


class ConstructCakeForm(forms.Form):
    elements = create_elements()
    levels = forms.ChoiceField(label='Стоимость уровней', choices=create_choices(elements, Level), widget=forms.RadioSelect)
    shapes = forms.ChoiceField(label='Форма уровней', choices=create_choices(elements, Shape), widget=forms.RadioSelect)
    toppings = forms.ChoiceField(label='Топпинг', choices=create_choices(elements, Topping), widget=forms.RadioSelect)
    berries = forms.MultipleChoiceField(label='Ягоды', required=False, choices=create_choices(elements, Berry), widget=forms.CheckboxSelectMultiple)
    decor = forms.MultipleChoiceField(label='Декор', required=False, choices=create_choices(elements, AdditionalIngredient), widget=forms.CheckboxSelectMultiple)
    lettering = forms.CharField(label='Надпись на торте', required=False, max_length=500)


class AdvancedInfoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    delivery_time = forms.DateTimeField(
        label='Дата доставки',
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    order_comment = forms.CharField(
        label='Комментарий к заказу',
        max_length=500,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )
    address = forms.CharField(
        label='Адрес доставки',
        max_length=500,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        initial='',
    )
    promo = forms.CharField(
        label='Промокод',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False,
    )

    def clean_delivery_time(self):
        delivery_time = super(AdvancedInfoForm, self).clean().get('delivery_time')

        if delivery_time < timezone.now():
            raise forms.ValidationError("День доставки не может быть раньше чем сегодня.")
        return delivery_time


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
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'address', 'email', 'phonenumber')

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

        self.fields['address'].label = 'Адрес'
        self.fields['address'].widget.attrs.update({'placeholder': ''})

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
