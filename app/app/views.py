from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import AlunoCadastroForm, LogomarcaForm
from .models import Logomarca, Aluno, Voto
from django.db.models import Sum  # Adicione este import no topo se não existir

def home(request):
    return render(request, 'home.html')

def cadastro_aluno(request):
    if request.method == 'POST':
        form = AlunoCadastroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado!')
            return redirect('home')
    else:
        form = AlunoCadastroForm()
    return render(request, 'cadastro_aluno.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        cpf = request.POST['cpf']
        password = request.POST['password']
        user = authenticate(request, cpf=cpf, password=password)
        if user:
            login(request, user)
            return redirect('home')
        messages.error(request, 'Credenciais inválidas.')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def votar(request):
    if request.user.is_professor:
        messages.error(request, 'Professores não podem votar.')
        return redirect('home')
    if request.user.voto_realizado:
        messages.error(request, 'Você já votou.')
        return redirect('home')
    logomarcas = Logomarca.objects.all()
    if request.method == 'POST':
        logo_id = request.POST.get('logo_id')
        if logo_id:
            logo = Logomarca.objects.get(id=logo_id)
            logo.votos += 1
            logo.save()
            Voto.objects.create(aluno=request.user, logomarca=logo)
            request.user.voto_realizado = True
            request.user.save()
            messages.success(request, 'Voto registrado!')
            return redirect('home')
    return render(request, 'votar.html', {'logomarcas': logomarcas})

class ProfessorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_professor  # Atualizado para is_professor

class LogomarcaListView(LoginRequiredMixin, ProfessorRequiredMixin, ListView):
    model = Logomarca
    template_name = 'logomarca_list.html'
    context_object_name = 'logomarcas'

class LogomarcaCreateView(LoginRequiredMixin, ProfessorRequiredMixin, CreateView):
    model = Logomarca
    form_class = LogomarcaForm
    template_name = 'logomarca_form.html'
    success_url = reverse_lazy('logomarca_list')

class LogomarcaUpdateView(LoginRequiredMixin, ProfessorRequiredMixin, UpdateView):
    model = Logomarca
    form_class = LogomarcaForm
    template_name = 'logomarca_form.html'
    success_url = reverse_lazy('logomarca_list')

class LogomarcaDeleteView(LoginRequiredMixin, ProfessorRequiredMixin, DeleteView):
    model = Logomarca
    template_name = 'logomarca_confirm_delete.html'
    success_url = reverse_lazy('logomarca_list')


@login_required
def dashboard(request):
    if not request.user.is_professor:
        return redirect('home')
    total_alunos = Aluno.objects.filter(is_professor=False).count()
    alunos_votaram = Aluno.objects.filter(is_professor=False, voto_realizado=True).count()
    logomarcas_qs = Logomarca.objects.all()
    total_votos = logomarcas_qs.aggregate(total=Sum('votos'))['total'] or 0

    logomarcas = []
    for logo in logomarcas_qs:
        percentual = (logo.votos / total_votos * 100) if total_votos > 0 else 0
        logomarcas.append({
            'nome': logo.nome,
            'votos': logo.votos,
            'percentual_votos': percentual,
        })

    context = {
        'total_alunos': total_alunos,
        'alunos_votaram': alunos_votaram,
        'logomarcas': logomarcas,
    }
    return render(request, 'dashboard.html', context)