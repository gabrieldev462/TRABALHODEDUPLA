from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app.views import (
    home, cadastro_aluno, login_view, logout_view, votar, dashboard,
    LogomarcaListView, LogomarcaCreateView, LogomarcaUpdateView, LogomarcaDeleteView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('cadastro/', cadastro_aluno, name='cadastro_aluno'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('votar/', votar, name='votar'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logomarcas/', LogomarcaListView.as_view(), name='logomarca_list'),
    path('logomarcas/create/', LogomarcaCreateView.as_view(), name='logomarca_create'),
    path('logomarcas/<int:pk>/update/', LogomarcaUpdateView.as_view(), name='logomarca_update'),
    path('logomarcas/<int:pk>/delete/', LogomarcaDeleteView.as_view(), name='logomarca_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)