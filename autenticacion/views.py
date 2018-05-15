from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Permission, Group
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib import messages
from  django.contrib.auth.hashers import make_password
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import tokens
from material import *
from .forms import UsuarioForm
from django.db.models import Q

# Create your views here.
def login(request):
    mensaje = ""
    next = request.GET.get('next')
    if request.POST:
        username = request.POST.get('LoginForm[username]')
        password = request.POST.get('LoginForm[password]')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if next:
                return redirect(next)
            else:
                return redirect('/')
        else:
            mensaje = "Usuario o Contraseña Incorrecto"
            return render(request, 'autenticacion/login.html', {'mensaje': mensaje, })
    else:
        return render(request, 'autenticacion/login.html', {'mensaje': mensaje, })

def logout(request):
    auth_logout(request)
    return redirect('/login')

@login_required
def cuenta(request):
    mensaje=""
    user = request.user
    if request.POST:
        if request.POST.get('contraseña'):
            if request.POST.get('contraseña') == request.POST.get('contraseña2'):
                user.password = make_password(request.POST.get('contraseña'), None, 'argon2')
            else:
                mensaje = "Las contraseñas no coinciden, vuelva a intentarlo"
                context = {'nombre': user.first_name,
                           'apellido': user.last_name,
                           'email': user.email,
                           'mensaje': mensaje}
                return render(request, "autenticacion/cuenta.html", context)

        if request.POST.get('nombres'):
            user.first_name = request.POST.get('nombres')
        if request.POST.get('apellidos'):
            user.last_name = request.POST.get('apellidos')
        if request.POST.get('correo'):
            user.email = request.POST.get('correo')
        try:
            user.save()
            mensaje = "Datos modificados con éxito"
        except:
            mensaje = "Error al modificar datos"
    user = User.objects.get(pk=user.id)
    context = {'nombre': user.first_name,
               'apellido': user.last_name,
               'email': user.email,
               'mensaje': mensaje}
    return render(request, "autenticacion/cuenta.html", context)

# Inician vistas para Usuarios
@login_required
@permission_required('auth.add_user')
def agregar_usuario(request):
    mensaje = ""
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = User(**form.cleaned_data)
            user.set_unusable_password()
            user.save()
            mensaje = "Usuario creado con éxito"
            template = get_template('autenticacion/email_contraseña.html')
            token = tokens.PasswordResetTokenGenerator()
            content = template.render(
                {'user': user, 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                 'token': token.make_token(user), 'request': request, })
            email = EmailMessage('Creación de Contraseña', content, to={user.email, })
            email.send()
            # Limpiando campos después de guardar (Reset Forms)
            form = UsuarioForm()
    else:
        form = UsuarioForm()

    return render(request, 'autenticacion/agregar_usuario.html', {'form': form, 'mensaje': mensaje})

@login_required
def usuarios(request):
    mensaje=""
    if request.user.has_perm('auth.change_user') or request.user.has_perm('auth.delete_user') or request.user.has_perms(['auth.add_permission', 'auth.change_permission','auth.delete_permission']):
        user_list=User.objects.all().exclude(pk=request.user.id)

        return render(request, 'autenticacion/usuarios.html', {'user_list': user_list, 'mensaje': mensaje, })
    else:
        mensaje = "No posee permisos para acceder a la página solicitada. Para continuar inicie sesión con un usuario privilegiado"
        return render(request, 'autenticacion/login.html', {'mensaje': mensaje, })

class ActualizarUsuario(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'first_name', 'last_name']
    template_name = 'autenticacion/agregar_usuario.html'
    success_message = "Usuario modificado con éxito"
    permission_required = 'auth.change_user'
    success_url = reverse_lazy('usuarios')
    layout = Layout(Fieldset('Modificar Usuario: '), Row('username', 'email'), Row('first_name', 'last_name'))

    def get_context_data(self, **kwargs):
        context = super(ActualizarUsuario, self).get_context_data(**kwargs)
        context['actualizar'] = True
        return context

    def get_form(self):
        form = super(ActualizarUsuario, self).get_form()
        form.fields['email'].required = True
        form.fields['first_name'].required = True
        form.fields['last_name'].required = True
        return form

@login_required
@permission_required('auth.delete_user')
def eliminar_usuario(request, pk):
    if request.user.id != int(pk):
        try:
            usuario = User.objects.get(pk=pk)
            usuario.delete()
            messages.add_message(request, messages.INFO, 'Usuario eliminado con éxito')
        except:
            messages.add_message(request, messages.INFO, 'Error al eliminar el usuario')
    else:
        messages.add_message(request, messages.INFO, 'No puede eliminar su propio usuario')
    return HttpResponseRedirect('/usuarios')
# Finalizan vistas para Usuarios
