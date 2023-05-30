# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db import models
from django.apps import apps


def create_model(model_name, app_label='', fields=None, module='', meta_options=None, admin_options=None):
    """
    Create specified model
    """

    class Meta:
        # Using type('Meta', ...) gives a dictproxy error during model creation
        pass

    if app_label:
        # app_label must be set using the Meta inner class
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if meta_options is not None:
        for key, value in meta_options.iteritems():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}

    # Add in any fields that were provided
    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(model_name, (models.Model,), attrs)

    # Create an Admin class if admin options were provided
    if admin_options is not None:
        class Admin(admin.ModelAdmin):
            pass

        for key, value in admin_options.items():
            setattr(Admin, key, value)
        admin.site.register(model, Admin)

    return model


def create_user_model():
    # 字段类型
    FIELD_TYPES = {
        "CharField": models.CharField,
    }

    model_name = "User"
    app_label = "app1"
    meta_options = {}
    admin_options = {}
    fields = [
        {
            "name": "name",
            "field_type": "CharField",
            "options": dict(
                verbose_name=u"用户",
                db_index=True,
                max_length=50,
                null=True,
                blank=True,
                help_text=u"操作的用户2"
            )
        },
        {
            "name": "sex",
            "field_type": "CharField",
            "options": dict(
                verbose_name=u"用户",
                db_index=True,
                max_length=50,
                null=True,
                blank=True,
                help_text=u"sex"
            )
        }
    ]
    model_fields = {}
    for f in fields:
        field_klass = FIELD_TYPES[f["field_type"]]

        model_fields[f["name"]] = field_klass(**f["options"])

    try:
        MyKlass = apps.get_model(app_label, model_name)
    except LookupError as e:
        MyKlass = create_model(
            model_name=model_name,
            app_label=app_label,
            fields=model_fields,
            module=app_label,
            meta_options=meta_options,
            admin_options=admin_options,
        )

    return MyKlass
