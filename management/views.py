from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.generic import CreateView, UpdateView, DeleteView
from django.core.handlers.wsgi import WSGIRequest
from django.views import View
from management.forms import BudgetForm, LineForm
from management.models import Budget, BudgetLine


class BudgetCreate(View):

    def get(self, request):
        form = BudgetForm()
        return TemplateResponse(request, 'management/budget/upsert.html', {'form': form, })

    def post(self, request):
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save()
            return redirect('budget-detail', pk=budget.pk)
        return TemplateResponse(request, 'management/budget/upsert.html', {'form': form, })


class BudgetEdit(View):

    def get(self, request, pk):
        budget = get_object_or_404(Budget, pk=pk)
        form = BudgetForm(instance=budget)
        return TemplateResponse(request, 'management/budget/upsert.html', {'form': form, })

    def post(self, request, pk):
        budget = get_object_or_404(Budget, pk=pk)
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            budget = form.save()
            return redirect('budget-detail', pk=budget.pk)
        return TemplateResponse(request, 'management/budget/upsert.html', {'form': form, })


class BudgetList(View):

    def get(self, request):
        budgets = Budget.objects.all()[::-1]
        return TemplateResponse(request, 'management/budget/list.html', {'budgets': budgets, })


class BudgetDetail(View):

    def get(self, request, pk):
        budget = get_object_or_404(Budget, pk=pk)
        return TemplateResponse(request, 'management/budget/detail.html', {'budget': budget, })


class BudgetDelete(View):

    def post(self, request, pk):
        budget = get_object_or_404(Budget, pk=pk)
        budget.delete()
        return redirect('budget-list')


class LineCreate(View):

    def get(self, request, budget_pk):
        budget = get_object_or_404(Budget, pk=budget_pk)
        form = LineForm()
        return TemplateResponse(request, 'management/line/upsert.html', {'form': form,
                                                                         'budget': budget})

    def post(self, request: WSGIRequest, budget_pk: int):
        form = LineForm(request.POST)
        user = request.user
        if form.is_valid() and user.is_authenticated:
            line: BudgetLine = form.save(commit=False)
            budget = get_object_or_404(Budget, pk=budget_pk)
            line.budget = budget
            line.creator = user
            line.save()
            return redirect('budget-detail', pk=budget_pk)
        return TemplateResponse(request, 'management/line/upsert.html', {'form': form, })


class LineEdit(View):

    def get(self, request, pk):
        line = get_object_or_404(BudgetLine, pk=pk)
        form = LineForm(instance=line)
        return TemplateResponse(request, 'management/line/upsert.html', {'form': form, })

    def post(self, request, pk):
        line = get_object_or_404(BudgetLine, pk=pk)
        form = LineForm(request.POST, instance=line)
        if form.is_valid():
            line = form.save()
            return redirect('budget-detail', pk=line.budget.pk)
        return TemplateResponse(request, 'management/line/upsert.html', {'form': form, })


class LineDetail(View):

    def get(self, request, pk):
        line = get_object_or_404(BudgetLine, pk=pk)
        return TemplateResponse(request, 'management/line/detail.html', {'line': line, })


class LineDelete(View):

    def post(self, request, pk):
        line = get_object_or_404(BudgetLine, pk=pk)
        line.delete()
        return redirect('budget-detail', pk=line.budget.pk)
