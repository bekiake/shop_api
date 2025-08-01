from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class UserCreationForm(forms.ModelForm):
    """Foydalanuvchi yaratish formasi"""
    password1 = forms.CharField(label='Parol', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Parolni tasdiqlash', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'last_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Parollar mos emas")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """Foydalanuvchi ma’lumotlarini tahrirlash"""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'phone', 'first_name', 'last_name', 'password', 'is_active', 'is_staff', 'is_superuser')

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ('email', 'phone', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password')}),
        (_('Shaxsiy ma’lumotlar'), {'fields': ('first_name', 'last_name')}),
        (_('Ruxsatlar'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Muhim sanalar'), {'fields': ('last_login', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('email', 'phone')
    ordering = ('email',)

admin.site.register(User, UserAdmin)
