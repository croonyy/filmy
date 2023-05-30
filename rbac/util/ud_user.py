from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import PermissionsMixin

from rbac.util import admin_tools as at
from rbac.util import tools_ud as tu


# from rbac.models import RbacRole,RbacPermission

class UserManager(BaseUserManager):
    def _create_user(self, username, password, email, **kwargs):
        if not username:
            raise ValueError("请传入用户名！")
        if not password:
            raise ValueError("请传入密码！")
        # if not email:
        #     raise ValueError("请传入邮箱地址！")
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password, email, **kwargs):
        kwargs['is_superuser'] = False
        return self._create_user(username, password, email, **kwargs)

    def create_superuser(self, username, password, email, **kwargs):
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self._create_user(username, password, email, **kwargs)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    chinese_name = models.CharField(max_length=20, verbose_name="中文名", null=True, blank=True)
    nickname = models.CharField(max_length=13, verbose_name="昵称", null=True, blank=True)
    age = models.IntegerField(verbose_name="年龄", null=True, blank=True)
    gender = models.CharField(max_length=2, choices=(("1", "男"), ("2", "女")),
                              verbose_name="性别", null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号码")
    avatar = models.ImageField(upload_to="img/avatar", verbose_name="用户头像", null=True, blank=True)
    home_address = models.CharField(max_length=100, null=True, blank=True, verbose_name="地址")
    card_id = models.CharField(max_length=30, verbose_name="身份证", null=True, blank=True)
    roles = models.ManyToManyField(to='rbac.Role', blank=True, verbose_name="角色")
    permission_views = models.ManyToManyField(to='rbac.PermissionView', blank=True, verbose_name='权限')

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=True,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username and password are required. Other fields are optional.
    """

    exe_btn = tu.curry(at.set_model_btn, btn_list=[("edit", {}), ])

    class Meta(AbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"
        # db_table = 'rbac_user'
        # app_label = "rbac"

# admin user


#
#
# class User(AbstractBaseUser, PermissionsMixin):  # 继承AbstractBaseUser，PermissionsMixin
#     # username_validator = UnicodeUsernameValidator()
#     username = models.CharField(max_length=50, verbose_name="用户名", unique=True)
#     nickname = models.CharField(max_length=13, verbose_name="昵称", null=True, blank=True)
#     age = models.IntegerField(verbose_name="年龄", null=True, blank=True)
#     gender = models.CharField(max_length=2, choices=(("1", "男"), ("2", "女")),
#                               verbose_name="性别", null=True, blank=True)
#     phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号码")
#     email = models.EmailField(null=True, blank=True, verbose_name="邮箱")
#     avatar = models.ImageField(upload_to="img/avatar", verbose_name="用户头像", null=True, blank=True)
#     # home_address = models.CharField(max_length=100, null=True, blank=True, verbose_name="地址")
#     # card_id = models.CharField(max_length=30, verbose_name="身份证", null=True, blank=True)
#     # roles = models.ManyToManyField('RbacRole', blank=True, verbose_name="角色")
#     # permissions = models.ManyToManyField('RbacPermission', blank=True, verbose_name='角色权限')
#     is_staff = models.BooleanField(default=True, verbose_name="是否是员工")
#     is_active = models.BooleanField(default=True, verbose_name="激活状态")
#     date_joined = models.DateTimeField(auto_now_add=True)
#
#     EMAIL_FIELD = 'email'
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']
#
#     objects = UserManager()
#
#     def get_full_name(self):
#         return self.username
#
#     def get_short_name(self):
#         return self.username
#
#     def clean(self):
#         super().clean()
#         self.email = self.__class__.objects.normalize_email(self.email)
#
#     class Meta:
#         # managed = True
#         swappable = "AUTH_USER_MODEL"
#         # db_table = 'auth_user'  # 跟原始用户表表名auth_user不一样的名字
#         app_label = 'auth'
#
#         # verbose_name = _("user")
#         # verbose_name_plural = _("users")
#         # abstract = True
