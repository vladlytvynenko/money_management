from django import forms

from management.models import Budget, BudgetLine


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = '__all__'


class LineForm(forms.ModelForm):
    class Meta:
        model = BudgetLine
        exclude = ['budget', 'creator']
        labels = {
            'is_income': 'Is this income?',
            'fulfilled': 'Is fulfilled?',
        }

