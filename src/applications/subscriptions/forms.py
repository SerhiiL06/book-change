from django import forms


class ChoicePeriodForm(forms.Form):
    period = (
        ("1", "One mounth"),
        ("3", "Three mounth"),
        ("6", "Six mounth"),
        ("12", "One year"),
    )

    plan_period = forms.ChoiceField(
        choices=period,
        help_text="choice one of the select period",
        label="Period for your plan",
    )
