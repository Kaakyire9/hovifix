from django.contrib import admin
from .models import FaultCall
from datetime import date, timedelta

# Filters
class TodayFilter(admin.SimpleListFilter):
    title = "Today's Calls"
    parameter_name = 'today'

    def lookups(self, request, model_admin):
        return (('today', 'Today'),)

    def queryset(self, request, queryset):
        if self.value() == 'today':
            return queryset.filter(created_at__date=date.today())

        return queryset

class DateRangeFilter(admin.SimpleListFilter):
    title = 'Date Range'
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return [
            ('yesterday', 'Yesterday'),
            ('last_7', 'Last 7 Days'),
            ('last_30', 'Last 30 Days'),
        ]

    def queryset(self, request, queryset):
        today = date.today()

        if self.value() == 'yesterday':
            return queryset.filter(created_at__date=today - timedelta(days=1))

        elif self.value() == 'last_7':
            return queryset.filter(created_at__date__gte=today - timedelta(days=7))

        elif self.value() == 'last_30':
            return queryset.filter(created_at__date__gte=today - timedelta(days=30))

        return queryset

@admin.register(FaultCall)
class FaultCallAdmin(admin.ModelAdmin):
    list_display = ('caller', 'location', 'assigned_engineer', 'status', 'created_at')
    list_filter = ('status', 'location', TodayFilter, DateRangeFilter)
    search_fields = ('caller__username', 'location', 'assigned_engineer__username')
    ordering = ('-created_at',)
    list_editable = ('assigned_engineer',)  # 👈 Allow inline assignment

