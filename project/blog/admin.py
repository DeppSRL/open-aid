from django.contrib.gis import admin
from models import Entry
from django.forms import ModelForm, CharField

from tinymce.widgets import TinyMCE

from tagging.admin import TagInline

class BlogEntryAdminForm(ModelForm):
    body = CharField(widget=TinyMCE(
        attrs={'cols': 120, 'rows': 40},
        mce_attrs={
            'theme': "advanced",
            'plugins': "fullscreen,media,preview",
            'plugin_preview_width' : "500",
            'plugin_preview_height' : "600",
            'cleanup_on_startup': True,
            'custom_undo_redo_levels': 10,
            'theme_advanced_buttons3': 'fullscreen,media,preview',
            'theme_advanced_toolbar_location': "top"

        }
    ))
    class Meta:
        model = Entry

class BlogEntryAdmin(admin.ModelAdmin):
    date_hierarchy= 'published_at'
    list_display = ('title', 'published_at')
    exclude = ['body_plain']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TagInline]
    form = BlogEntryAdminForm

admin.site.register(Entry, BlogEntryAdmin)
