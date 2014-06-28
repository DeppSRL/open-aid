from django.contrib.gis import admin
from django.core.urlresolvers import reverse
from models import Entry
from django.forms import ModelForm, CharField

from tinymce.widgets import TinyMCE

from tagging.admin import TagInline

class BlogEntryAdminForm(ModelForm):
    abstract = CharField(widget=TinyMCE(
        attrs={'cols': 120, 'rows': 7},
        mce_attrs={
            'theme': "advanced",
            'plugins': "advimage,media",
            'plugin_preview_width' : "1280",
            'plugin_preview_height' : "400",
            'content_css' : "/static/css/main.css",
            'cleanup_on_startup': True,
            'custom_undo_redo_levels': 10,
            'theme_advanced_buttons1' : "bold,italic,underline,|,justifyleft,justifycenter,justifyright,justifyfull,|,formatselect,|,undo,redo",
            'theme_advanced_buttons2' : "link,unlink,|,image,media,|,code",
            'theme_advanced_buttons3': "",
            'theme_advanced_toolbar_location': "top"
        }
    ))
    body = CharField(widget=TinyMCE(
        attrs={'cols': 120, 'rows': 40},
        mce_attrs={
            'theme': "advanced",
            'plugins': "fullscreen,media,preview,advimage",
            'plugin_preview_width' : "1280",
            'plugin_preview_height' : "800",
            'content_css' : "/static/css/main.css",
            'plugin_preview_pageurl': "/tinymce/preview/entry",
            'cleanup_on_startup': True,
            'custom_undo_redo_levels': 10,
            'theme_advanced_buttons1' : "bold,italic,underline,|,justifyleft,justifycenter,justifyright,justifyfull,|,bullist,numlist,|,outdent,indent,|,formatselect,|,undo,redo",
            'theme_advanced_buttons2' : "link,unlink,|,image,media,|,fullscreen,zoom,|,preview,code",
            'theme_advanced_buttons3': "",
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
