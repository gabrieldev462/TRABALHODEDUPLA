from django.contrib import admin
from .models import Aluno, Logomarca, Voto

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'first_name', 'last_name', 'is_professor', 'voto_realizado')
    list_filter = ('is_professor', 'voto_realizado')
    search_fields = ('cpf', 'first_name', 'last_name')

@admin.register(Logomarca)
class LogomarcaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'votos')

admin.site.register(Voto)