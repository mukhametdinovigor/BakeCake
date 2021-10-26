from django import forms


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
    berries = forms.ChoiceField(label='Ягоды', choices=BERRIES, widget=forms.CheckboxSelectMultiple)
    decor = forms.ChoiceField(label='Декор', choices=DECOR, widget=forms.CheckboxSelectMultiple)
    lettering = forms.CharField(label='Мы можем разместить на торте любую надпись, например: «С днем рождения!»', max_length=300)

