from django.urls import path
from .views import (BudgetCreate, BudgetDetail, BudgetList, BudgetDelete, BudgetEdit,
                    LineCreate, LineDetail, LineDelete, LineEdit,)

urlpatterns = [
    path('budgets/', BudgetList.as_view(), name='budget-list'),
    path('budget/create/', BudgetCreate.as_view(), name='budget-create'),
    path('budget/<int:pk>/', BudgetDetail.as_view(), name='budget-detail'),
    path('budget/<int:pk>/edit', BudgetEdit.as_view(), name='budget-edit'),
    path('budget/<int:pk>/delete', BudgetDelete.as_view(), name='budget-delete'),

    path('line/<int:budget_pk>/create/', LineCreate.as_view(), name='line-create'),
    path('line/<int:pk>/', LineDetail.as_view(), name='line-detail'),
    path('line/<int:pk>/edit', LineEdit.as_view(), name='line-edit'),
    path('line/<int:pk>/delete', LineDelete.as_view(), name='line-delete'),
]
