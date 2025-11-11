from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ["question_text"]
    list_filter = ["pub_date"]
    list_display = ["question_text", "pub_date", "was_published_recently"]

    # fieldsets 은 두 가지 tuple 로 구성
    # 첫번째는 name 으로 fieldset 의 title 로 활용됨
    # 두번째는 fieldset 의 옵션을 나타내는 dictionary
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date Information", {
            "fields": ["pub_date"], "classes": ["copllapse"]
        }),
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
