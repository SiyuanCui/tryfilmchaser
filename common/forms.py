from django import forms
from .widgets import MyDataSetWidget


class ModelChoiceField(forms.ModelChoiceField):

    def __init__(self, queryset, *, label_text=None, empty_label="---------",
                 required=True, widget=None, label=None, initial=None,
                 help_text='', to_field_name=None, limit_choices_to=None,
                 blank=False, **kwargs):
        self.label_text = label_text
        super(ModelChoiceField, self).__init__(queryset,
                                               empty_label=empty_label,
                                               required=required,
                                               widget=widget,
                                               label=label,
                                               initial=initial,
                                               help_text=help_text,
                                               to_field_name=to_field_name,
                                               limit_choices_to=limit_choices_to,
                                               blank=blank
                                               , **kwargs)

    # 原有得写法必须写在对象上面得__str__ 方法下返回，重写了该方法后，系统自动使用用户设定得字段显示
    def label_from_instance(self, obj):
        return getattr(obj, self.label_text)
