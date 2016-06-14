from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from user_auth.models import KnackUser, SocialLink, College, Year, RegisterEmail


class SocialInline(admin.StackedInline):
    model = SocialLink


class KnackUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('password', )
    inlines = (SocialInline, )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'gender', 'age', 'picture')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'last_seen')}),
        (_('Uknack Information'), {'fields': ('college', 'year', 'reasons', 'about_me', 'public_profile_url', 'payment_venmo', 'payment_paypal')})
    )


admin.site.register(KnackUser, KnackUserAdmin)

admin.site.register(College)

admin.site.register(Year)

admin.site.register(RegisterEmail)