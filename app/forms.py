from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Aluno, Logomarca

class AlunoCadastroForm(UserCreationForm):
    class Meta:
        model = Aluno
        fields = ['first_name', 'last_name', 'cpf'] # Removido password1 e password2, UserCreationForm já os tem
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Digite seu nome'}),
            'last_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Digite seu sobrenome'}),
            'cpf': forms.TextInput(attrs={'class': 'input-field', 'placeholder': '000.000.000-00'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password2'].label = "Confirme a Senha"
        for field_name, field in self.fields.items():
            if 'password' in field_name:
                field.widget.attrs.update({'class': 'input-field', 'placeholder': 'Crie uma senha segura'})


    def clean_cpf(self):
        cpf = self.cleaned_data['cpf'].replace('.', '').replace('-', '')
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