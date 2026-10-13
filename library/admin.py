from django.contrib import admin
from django.db.models import Count

from .models import Author, Genre, Book


# ═══════════════════════════════════════════════════
# Author
# ═══════════════════════════════════════════════════
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'birth_date')
    search_fields = ('first_name', 'last_name')
    list_filter = ('birth_date',)
    ordering = ('last_name',)


# ═══════════════════════════════════════════════════
# Genre
# ═══════════════════════════════════════════════════
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'books_count')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

    def get_queryset(self, request):
        # annotate решает N+1: вместо COUNT для каждого жанра — один SQL с COUNT
        qs = super().get_queryset(request)
        return qs.annotate(_books_count=Count('books'))

    @admin.display(description='Количество книг', ordering='_books_count')
    def books_count(self, obj):
        return obj._books_count


# ═══════════════════════════════════════════════════
# Book
# ═══════════════════════════════════════════════════
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # ── Список ──
    list_display = (
        'title',
        'author',
        'publication_year',
        'price',
        'available',
    )
    list_display_links = ('title',)
    list_editable = ('price', 'available')
    list_filter = ('available', 'author', 'genres')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    # ── Оптимизация N+1 ──
    list_select_related = ('author',)
    # Жанры — M2M, для них нужен prefetch; делаем через get_queryset
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author').prefetch_related('genres')

    # ── Форма редактирования ──
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основное', {
            'fields': ('title', 'slug', 'description'),
        }),
        ('Автор и жанры', {
            'fields': ('author', 'genres'),
        }),
        ('Издание', {
            'fields': ('publication_year', 'isbn', 'pages'),
        }),
        ('Цена и наличие', {
            'fields': ('price', 'available'),
        }),
        ('Служебное', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),   # ← сворачиваемая группа
        }),
    )

    # ── Удобства ──
    filter_horizontal = ('genres',)
    save_on_top = True