import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Sum
from django.urls import reverse
import calendar

User = get_user_model()

GOOD = 'bg-success'
BAD = 'bg-danger'


class Budget(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    is_purpose_save_money = models.BooleanField(default=True, verbose_name="Purpose save money")
    purpose = models.IntegerField(default=0)
    group = models.ForeignKey(
        'auth.Group', related_name='budgets', on_delete=models.CASCADE)

    def lines_count(self):
        return self.lines.all().count()

    def get_url(self):
        return reverse('budget-detail', args=[self.pk])

    def get_month(self):
        return self.start_date.strftime("%B %Y")

    @property
    def all_lines(self):
        return self.lines.order_by('fulfilled', '-pk').all()

    @property
    def goal(self):
        return 'Save' if self.is_purpose_save_money else 'Spend'

    @property
    def incomes(self):
        return BudgetLine.objects.filter(is_income=True, budget=self.pk)

    @property
    def expenses(self):
        return BudgetLine.objects.filter(is_income=False, budget=self.pk)

    @property
    def real_income(self):
        return self._get_lines_sum(self.incomes, fulfilled=True)

    @property
    def soon_income(self):
        return self._get_lines_sum(self.incomes, fulfilled=False)

    def real_income_higher(self):
        return self.real_income >= self.soon_income

    @property
    def real_expense(self):
        return self._get_lines_sum(self.expenses, fulfilled=True)

    @property
    def soon_expense(self):
        return self._get_lines_sum(self.expenses, fulfilled=False)

    def real_expense_higher(self):
        return self.real_expense >= self.soon_expense

    @property
    def real_difference(self):
        return self.real_income - self.real_expense

    @property
    def soon_difference(self):
        return self.soon_income - self.soon_expense

    def real_diff_higher(self):
        return self.real_difference >= self.soon_difference

    @property
    def real_spend_per_day(self):
        diff = self.real_difference - self.purpose
        if not self.is_purpose_save_money:
            diff *= -1
        return diff / (self.days_left() or 1)

    @property
    def soon_spend_per_day(self):
        diff = self.soon_difference - self.purpose
        if not self.is_purpose_save_money:
            diff *= -1
        return diff / (self.days_left() or 1)

    @property
    def real_spend_per_week(self):
        this_week_days = self.days_left_to_end_of_week()
        return this_week_days * self.real_spend_per_day

    @property
    def soon_spend_per_week(self):
        this_week_days = self.days_left_to_end_of_week()
        return this_week_days * self.soon_spend_per_day

    def real_spend_per_day_higher(self):
        return self.real_spend_per_day >= self.soon_spend_per_day

    def real_spend_per_week_higher(self):
        return self.real_spend_per_week >= self.soon_spend_per_week

    def days_left(self):
        return calendar.monthrange(self.start_date.year, self.start_date.month)[1] - datetime.datetime.now().day

    def days_left_to_end_of_week(self):
        first_day_of_week, last_day_of_month = calendar.monthrange(self.start_date.year, self.start_date.month)
        today = datetime.datetime.today()
        today_day_of_month, today_weekday = today.day, today.weekday()
        this_week_days = 7 - today_weekday
        if today_day_of_month + this_week_days > last_day_of_month:
            this_week_days = last_day_of_month - today_day_of_month + 1
        return this_week_days

    @staticmethod
    def _get_lines_sum(qs, fulfilled=True):
        if fulfilled:
            qs = qs.filter(fulfilled=True)
        return qs.aggregate(Sum('value'))['value__sum'] or 0

    def __str__(self):
        return (f'Budget {self.start_date.strftime("%m-%Y")} '
                f'with {self.real_income} {settings.CURRENCY} income '
                f'and {self.real_expense} {settings.CURRENCY} expense')


class Category(models.Model):
    name = models.CharField(max_length=128)
    is_income = models.BooleanField()

    @property
    def is_expense(self):
        return not self.is_income

    def __str__(self):
        return self.get_name()

    def get_name(self):
        return self.name.capitalize() if self.name else '-'

    class Meta:
        verbose_name_plural = "Categories"


class BudgetLine(models.Model):
    budget = models.ForeignKey(
        Budget, related_name='lines',
        null=True, blank=True,
        on_delete=models.CASCADE)
    creator = models.ForeignKey(
        User, related_name='lines',
        null=True, blank=True,
        on_delete=models.SET_NULL)
    category = models.ForeignKey(
        Category, related_name='lines',
        null=True, blank=True,
        on_delete=models.SET_NULL)
    fulfilled = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)
    value = models.PositiveIntegerField()
    note = models.TextField(null=True, blank=True)
    short_description = models.CharField(max_length=24)
    is_income = models.BooleanField()

    def __str__(self):
        return f'{self.name}: {self.value} {settings.CURRENCY}'

    def get_url(self):
        return reverse('line-detail', args=[self.pk])

    def get_date(self):
        return self.date.strftime("%d %B %Y")

    def get_note(self):
        return self.note or "-"

    def get_category_name(self):
        return self.category.get_name() if self.category else "-"

    @property
    def is_expense(self):
        return not self.is_income

    def class_style(self):
        return 'success' if self.is_income else 'danger'

    @property
    def name(self):
        return 'Income' if self.is_income else 'Expense'
