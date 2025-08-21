from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Aluno, Logomarca

class AlunoCadastroForm(UserCreationForm):
    class Meta:
        model = Aluno
        fields = ['first_name', 'last_name', 'cpf', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            
        }

    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        if len(cpf) != 11 or not cpf.isdigit():
            raise forms.ValidationError("CPF deve ter 11 dígitos numéricos.")
        if Aluno.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("CPF já cadastrado.")
        return cpf

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.cpf  # Garante que username será igual ao CPF
        if commit:
            user.save()
        return user

class LogomarcaForm(forms.ModelForm):
    class Meta:
        model = Logomarca
        fields = ['nome', 'imagem', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }