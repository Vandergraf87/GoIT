from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView, ListView
from django.http import JsonResponse
from django.core.serializers import serialize
from django.views import View
from .forms import AuthorForm, QuoteForm
from .models import Author, Quote

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')
    
class AuthorListView(ListView):
    model = Author
    template_name = 'author_list.html'
    context_object_name = 'authors'

class QuoteListView(ListView):
    model = Quote
    template_name = 'quote_list.html'
    context_object_name = 'quotes'

# def quote_list(request):
#     quotes = Quote.objects.all()
#     authors = Author.objects.all()
#     return render(request, 'quote_list.html', {'quotes': quotes, 'authors': authors})
    
# def quote_list(request):
#     quotes = Quote.objects.all()
#     return render(request, 'quotes/quote_list.html', {'quotes': quotes})

def quote_list(request):
    quotes = Quote.objects.all()

    # Manually serialize queryset to JSON
    quotes_json = [{'text': quote.text, 'author': quote.author, 'tags': quote.tags} for quote in quotes]
    
    # Return JSON response with 'quotes' as the key
    return JsonResponse({'quotes': quotes_json})

# def home(request):
#     quotes = Quote.objects.all()
#     return render(request, 'quotes/quote_list.html', {'quotes': quotes})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile_view(request):
    # Отримуємо поточного користувача
    user = request.user

    # Отримуємо дані профілю користувача, доступні в стандартній моделі
    # username, first_name, last_name, email та інші атрибути користувача
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    email = user.email

    # Передаємо дані в шаблон
    context = {'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email}
    return render(request, 'registration/profile.html', context)

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()
    return render(request, 'myquotes/add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = request.user
            quote.save()
            return redirect('quote_list')
    else:
        form = QuoteForm()
    return render(request, 'myquotes/add_quote.html', {'form': form})

