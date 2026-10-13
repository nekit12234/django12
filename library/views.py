from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect

from .models import Author, Book
from accounts.models import Profile

def book_list(request):
    """Список доступных книг."""
    books = (
        Book.objects
        .filter(available=True)
        .select_related('author')
        .order_by('title')
    )
    return render(request, 'library/book_list.html', {'books': books})


def book_detail(request, slug):
    """Детальная страница книги."""
    book = get_object_or_404(
        Book.objects.select_related('author').prefetch_related('genres'),
        slug=slug,
        available=True,
    )
    return render(request, 'library/book_detail.html', {'book': book})


def author_list(request):
    """Список авторов с количеством книг."""
    authors = (
        Author.objects
        .annotate(books_count=Count('books'))
        .order_by('last_name', 'first_name')
    )
    return render(request, 'library/author_list.html', {'authors': authors})


def author_detail(request, pk):
    """Страница автора со списком его доступных книг."""
    author = get_object_or_404(Author, pk=pk)
    books = (
        author.books
        .filter(available=True)
        .order_by('title')
    )
    return render(request, 'library/author_detail.html', {
        'author': author,
        'books': books,
    })


def about(request):
    """Статичная страница «О библиотеке»."""
    return render(request, 'library/about.html', {'title': 'О библиотеке'})



def index(request):
    """Редирект с корня сайта на список книг."""
    return redirect('library:book_list')
def reader_list(request):
    readers = (
        Profile.objects
        .select_related('user')
        .order_by('user__last_name', 'user__first_name')
    )
    return render(request, 'library/reader_list.html', {'readers': readers})


def reader_detail(request, pk):
    reader = get_object_or_404(
        Profile.objects.select_related('user'),
        pk=pk,
    )
    return render(request, 'library/reader_detail.html', {'reader': reader})