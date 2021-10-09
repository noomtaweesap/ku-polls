"""You can edit choices and questions for admin page."""

from django.contrib import admin
from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    """Add or edit choices for polls."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """Add or edit question for polls."""

    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {
            'fields': ['pub_date', 'end_date'],
            'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
