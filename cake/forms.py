from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Customer, Level, Shape, Topping, Berry, AdditionalIngredient, Order


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
    levels = forms.ChoiceField(label='Форма уровней', choices=create_choices(elements, Level), widget=forms.RadioSelect)
    shapes = forms.ChoiceField(label='Форма уровней', choices=create_choices(elements, Shape), widget=forms.RadioSelect)
    toppings = forms.ChoiceField(label='Топпинг', choices=create_choices(elements, Topping), widget=forms.RadioSelect)
    berries = forms.MultipleChoiceField(label='Ягоды', required=False, choices=create_choices(elements, Berry), widget=forms.CheckboxSelectMultiple)
    decor = forms.MultipleChoiceField(label='Декор', required=False, choices=create_choices(elements, AdditionalIngredient), widget=forms.CheckboxSelectMultiple)
    lettering = forms.CharField(label='Мы можем разместить на торте любую надпись, например: «С днем рождения!»', required=False, max_length=500)


class AdvancedInfoForm(forms.ModelForm):
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        # init is used for other fields initialization and crispy forms

    class Meta:
        model = Order
        fields = ['delivered_at', 'delivery_time']

        widgets = {
            'delivered_at': forms.DateInput(
                format=('%d/%m/%Y'),
                attrs={'class': 'form-control',
                       'placeholder': 'Select a date',
                       'type': 'date'  # <--- IF I REMOVE THIS LINE, THE INITIAL VALUE IS DISPLAYED
                       }),
            'delivery_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    order_comment = forms.CharField(label='Комментарий к заказу', max_length=500, widget=forms.TextInput)
    address = forms.CharField(label='Адрес доставки', max_length=500, initial='')


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
