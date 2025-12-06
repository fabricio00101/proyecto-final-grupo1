from django.contrib.auth.models import Group

def usuario_colaborador(request):
    """Context processor para verificar si el usuario es colaborador"""
    context = {
        'pertenece_a_colaboradores': False,
    }
    
    if request.user.is_authenticated:
        context['pertenece_a_colaboradores'] = request.user.groups.filter(name='Colaborador').exists()
    
    return context
