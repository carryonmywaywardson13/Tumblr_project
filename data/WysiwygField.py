from wtforms import fields, widgets


class WysiwygWidget(widgets.TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' wysiwyg'
        else:
            kwargs.setdefault('class', 'wysiwyg')
        return super(WysiwygWidget, self).__call__(field, **kwargs)


class WysiwygField(fields.TextAreaField):
    widget = WysiwygWidget()