from django.contrib import admin, messages
from .models import Movie
from django.db.models import QuerySet


class RaingFilter(admin.SimpleListFilter):
    title = 'Фильтр по рейтингу'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return [
            ('до 40', 'Ужасный'),
            ('от 40 до 60', 'Плохой'),
            ('от 60 до 70', 'Нормальный'),
            ('от 70 до 85', 'Хороший'),
            ('от 85 до 90', 'Очень хороший'),
            ('более 90', 'Отличный'),
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == 'до 40':
            return queryset.filter(rating__lt=40)
        if self.value() == 'от 40 до 60':
            return queryset.filter(rating__range=(40, 60))
        if self.value() == 'от 60 до 70':
            return queryset.filter(rating__range=(60, 70))
        if self.value() == 'от 70 до 85':
            return queryset.filter(rating__range=(70, 85))
        if self.value() == 'от 85 до 90':
            return queryset.filter(rating__range=(85, 90))
        if self.value() == 'более 90':
            return queryset.filter(rating__gt=90)
        return queryset


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    # exclude = ('slug',)
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'rating', 'currency', 'budget', 'rating_status')
    list_editable = ('rating', 'currency', 'budget')
    ordering = ('-rating', 'name')
    list_per_page = 10
    actions = ('set_dollar', 'set_euro')
    search_fields = ('name__startswith',)
    list_filter = ('name', 'currency', RaingFilter)

    @admin.display(ordering='rating', description='Статус')
    def rating_status(self, obj):
        if obj.rating < 40:
            return 'Ужасный'
        if obj.rating < 60:
            return 'Плохой'
        if obj.rating <= 70:
            return 'Нормальный'
        if obj.rating <= 85:
            return 'Хороший'
        if obj.rating <= 90:
            return 'Очень хороший'
        else:
            return 'Отличный'

    @admin.action(description='Установить в доллары')
    def set_dollar(self, request, queryset: QuerySet):
        queryset.update(currency=Movie.USD)

    @admin.action(description='Установить в евро')
    def set_euro(self, request, queryset: QuerySet):
        count_upbated = queryset.update(currency=Movie.EUR)
        self.message_user(request, f'Обновлено {count_upbated} записей', messages.SUCCESS)

# admin.site.register(Movie, MovieAdmin)
