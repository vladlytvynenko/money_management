from django.contrib import admin
from .models import Budget, BudgetLine, Category

admin.site.register(Budget)
admin.site.register(BudgetLine)
admin.site.register(Category)
