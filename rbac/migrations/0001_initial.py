# Generated by Django 4.0.3 on 2023-05-21 16:41

import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'icon图标',
                'verbose_name_plural': 'icon图标',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='权限类型')),
                ('extra', models.JSONField(blank=True, null=True, verbose_name='Json配置')),
            ],
            options={
                'verbose_name': '权限类型',
                'verbose_name_plural': '权限类型',
                'db_table': 'rbac_permission',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PermissionView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='取个名字便于权限识别，可不填', max_length=200, null=True, verbose_name='名称')),
                ('extra', models.JSONField(blank=True, null=True, verbose_name='Json配置')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.permissionview', verbose_name='菜单父对象')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rbac.permission', verbose_name='权限类型')),
            ],
            options={
                'verbose_name': '权限实例',
                'verbose_name_plural': '权限实例',
                'db_table': 'rbac_permission_view',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='RequestRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('get_args', models.TextField(blank=True, null=True)),
                ('post_args', models.TextField(blank=True, null=True)),
                ('user', models.CharField(blank=True, max_length=50, null=True)),
                ('content_params', models.TextField(blank=True, null=True)),
                ('content_type', models.TextField(blank=True, null=True)),
                ('encoding', models.CharField(blank=True, max_length=50, null=True)),
                ('headers', models.TextField(blank=True, null=True)),
                ('method', models.CharField(blank=True, max_length=50, null=True)),
                ('app_name', models.CharField(blank=True, max_length=50, null=True)),
                ('app_names', models.CharField(blank=True, max_length=100, null=True)),
                ('args', models.TextField(blank=True, null=True)),
                ('kwargs', models.TextField(blank=True, null=True)),
                ('namespace', models.CharField(blank=True, max_length=50, null=True)),
                ('namespaces', models.TextField(blank=True, null=True)),
                ('route', models.TextField(blank=True, null=True)),
                ('url_name', models.CharField(blank=True, max_length=100, null=True)),
                ('view_name', models.CharField(blank=True, max_length=100, null=True)),
                ('scheme', models.CharField(blank=True, max_length=50, null=True)),
                ('ip_from', models.CharField(blank=True, max_length=50, null=True)),
                ('res_charset', models.CharField(blank=True, max_length=50, null=True)),
                ('res_closed', models.BooleanField(blank=True, null=True)),
                ('res_cookies', models.TextField(blank=True, null=True)),
                ('res_reason_phrase', models.CharField(blank=True, max_length=50, null=True)),
                ('res_status_code', models.IntegerField(blank=True, null=True)),
                ('res_streaming', models.TextField(blank=True, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '请求记录',
                'verbose_name_plural': '请求记录',
                'db_table': 'rbac_request_record',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='名称')),
                ('code', models.JSONField(max_length=1000, verbose_name='源码1')),
                ('code2', models.TextField(blank=True, max_length=1000, null=True, verbose_name='源码2')),
            ],
            options={
                'verbose_name': '测试',
                'verbose_name_plural': '测试',
                'db_table': 'rbac_test',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ViewObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='名称')),
                ('extra', models.JSONField(blank=True, null=True, verbose_name='Json配置')),
            ],
            options={
                'verbose_name': '作用对象',
                'verbose_name_plural': '作用对象',
                'db_table': 'rbac_view_object',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='角色名')),
                ('permission_views', models.ManyToManyField(blank=True, to='rbac.permissionview', verbose_name='权限')),
            ],
            options={
                'verbose_name': '角色',
                'verbose_name_plural': '角色',
                'db_table': 'rbac_role',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='permissionview',
            name='view_object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rbac.viewobject', verbose_name='作用对象'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('chinese_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='中文名')),
                ('nickname', models.CharField(blank=True, max_length=13, null=True, verbose_name='昵称')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='年龄')),
                ('gender', models.CharField(blank=True, choices=[('1', '男'), ('2', '女')], max_length=2, null=True, verbose_name='性别')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='手机号码')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='img/avatar', verbose_name='用户头像')),
                ('home_address', models.CharField(blank=True, max_length=100, null=True, verbose_name='地址')),
                ('card_id', models.CharField(blank=True, max_length=30, null=True, verbose_name='身份证')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=True, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('roles', models.ManyToManyField(blank=True, to='rbac.role', verbose_name='角色')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
                'swappable': 'AUTH_USER_MODEL',
            },
        ),
    ]
