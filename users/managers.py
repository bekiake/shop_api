from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("Email kiritilishi shart")
        if not phone:
            raise ValueError("Telefon raqam kiritilishi shart")
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser uchun is_staff=True bo‘lishi shart')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser uchun is_superuser=True bo‘lishi shart')

        return self.create_user(email, phone, password, **extra_fields)
