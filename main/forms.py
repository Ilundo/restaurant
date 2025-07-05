from django import forms

class OrderForm(forms.Form):
    street = forms.CharField(label="Вулиця", max_length=100)
    city = forms.CharField(label="Місто", max_length=50)
    postal_code = forms.CharField(label="Поштовий індекс", max_length=10)

    payment_method = forms.ChoiceField(
        label="Спосіб оплати",
        choices=[('cash', 'Готівка'), ('card', 'Картка')],
        widget=forms.RadioSelect
    )

    card_number = forms.CharField(label="Номер картки", max_length=19, required=False)
    card_expiry = forms.CharField(label="Термін дії (MM/YY)", max_length=5, required=False)
    card_cvv = forms.CharField(label="CVV", max_length=3, required=False)
