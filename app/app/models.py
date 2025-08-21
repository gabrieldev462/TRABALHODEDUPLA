from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class AlunoManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, cpf, password=None, **extra_fields):
        if not cpf:
            raise ValueError('O campo CPF deve ser preenchido')
        extra_fields.setdefault('username', cpf)  # Garante compatibilidade com AbstractUser
        user = self.model(cpf=cpf, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_professor', True)
        extra_fields.setdefault('username', cpf)  # Garante compatibilidade com AbstractUser

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True.')

        return self.create_user(cpf, password, **extra_fields)

class Aluno(AbstractUser):
    cpf = models.CharField(max_length=9, unique=True, help_text="CPF sem pontos ou traços")
    voto_realizado = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)  # Campo para identificar professores

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = AlunoManager()  # Adicione esta linha

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.cpf})"

    def save(self, *args, **kwargs):
        if self.is_professor and self.voto_realizado:
            raise ValueError("Professores não podem votar.")
        super().save(*args, **kwargs)

class Logomarca(models.Model):
    nome = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='logomarcas/')
    descricao = models.TextField(blank=True, null=True)
    votos = models.IntegerField(default=0)

    def __str__(self):
        return self.nome

    def percentual_votos(self):
        total_votos = Logomarca.objects.aggregate(total=models.Sum('votos'))['total'] or 0
        return (self.votos / total_votos * 100) if total_votos > 0 else 0


class Voto(models.Model):
    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE)
    logomarca = models.ForeignKey(Logomarca, on_delete=models.CASCADE)
    data_voto = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Voto de {self.aluno} em {self.logomarca}"