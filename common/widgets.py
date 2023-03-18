# coding:utf-8
from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class ForeignKey(forms.ChoiceField):
    pass


class UMeditorWidget(forms.Textarea):
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''

        editor_id = "id_%s" % name.replace("-", "_")
        uSettings = {
            "name": name,
            "id": editor_id,
            "value": value
        }
        context = {
            'UEditor': uSettings,
            'STATIC_URL': settings.STATIC_URL,
            'STATIC_ROOT': settings.STATIC_ROOT,
            'MEDIA_URL': settings.MEDIA_URL,
            'MEDIA_ROOT': settings.MEDIA_ROOT
        }
        return mark_safe(render_to_string('umeditor/umeditor.html', context))

    class Media:
        js = ("js/umeditor/umeditor.config.js", "js/umeditor/umeditor.js",)


class LabelImageWidget(forms.TextInput):
    template_name = 'common/widget/image_label.html'


class LabelWidget(forms.TextInput):
    template_name = 'common/widget/label.html'


class MyImageWidget(forms.TextInput):
    template_name = 'common/image.html'

    class Media:
        js = ("upload/upload.js",)
        css = {
            'all': ("upload/upload.css",)
        }


class MyDataSetWidget(forms.TextInput):
    template_name = ''

    def __init__(self, queryset, tpl, **kwargs):
        self.queryset = queryset
        self.template_name = tpl
        super(MyDataSetWidget, self).__init__(**kwargs)


class SpecWidget(forms.TextInput):
    template_name = 'common/widget/spec.html'

    class Media:
        js = ("tags/tags.js",)
        css = {
            'tags': ("tags/tags.css",)
        }


class MyImagesWidget(forms.Widget):
    allow_multiple_selected = True

    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = []

        context = {
            'name': name,
            'value': value,
        }
        return mark_safe(render_to_string('common/images.html', context))

    def format_value(self, value):
        if value is None and self.allow_multiple_selected:
            return []
        if not isinstance(value, (tuple, list)):
            value = [value]
        return [str(v) if v is not None else '' for v in value]

    class Media:
        js = ("upload/upload.js")
        css = {
            'upload': ("upload/upload.css",)
        }


class MyPaperWidget(forms.TextInput):
    template_name = 'common/widget/paper.html'

    class Media:
        js = ("paper/paperForm.js")
