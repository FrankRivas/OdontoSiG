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
from .forms import UsuarioForm2, RolForm
from django.db.models import Q
from django.conf import settings
from axes.models import AccessAttempt
from axes.utils import reset
from gerencial.models import Bitacora, Accion
import datetime
import locale
from datetime import datetime


# Create your views here.
def login(request):
    mensaje = ""
    next = request.GET.get('next')
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            reset(username=username)
            if next:
                return redirect(next)
            else:
                return redirect('/')
        else:
            mensaje = "Usuario o Contraseña Incorrecto"
            try:
                axes = AccessAttempt.objects.get(username=username)
                user = User.objects.get(username=username)
                if user.is_active:
                    if axes.failures_since_start >=settings.AXES_FAILURE_LIMIT:
                        user.is_active = False
                        user.save()
                        mensaje = "Usuario bloqueado, póngase en contacto con el administrador"
                    else:
                        mensaje = "Contraseña errónea le quedan " + str(settings.AXES_FAILURE_LIMIT-axes.failures_since_start) + " intentos"
                else:
                    mensaje = "Usuario bloqueado, póngase en contacto con el administrador"
            except:
                pass
            return render(request, 'autenticacion/login.html', {'mensaje': mensaje, })
    else:
        return render(request, 'autenticacion/login.html', {'mensaje': mensaje, })

def logout(request):
    auth_logout(request)
    return redirect('/login')

@login_required()
def recuperarContra(request, id):
    mensaje=""
    usuario = User.objects.get(pk=id)
    if request.POST:
        if request.POST.get('contraseña'):
            if request.POST.get('contraseña') == request.POST.get('contraseña2'):
                usuario.password = make_password(request.POST.get('contraseña'), None, 'argon2')

                id_accion = Accion.objects.get(pk=7)
                id = id_accion.id

                new_user_bit = Bitacora.objects.create(
                    Usuario_id=request.user.id,
                    Accion_id=id
                )

            else:
                mensaje = "Las contraseñas no coinciden, vuelva a intentarlo"
                return render(request, "autenticacion/contra.html",{'mensaje': mensaje})
        try:
            usuario.save()
            new_user_bit.save()
            messages.add_message(request, messages.INFO, 'Contraseña Modificada con Exito')
            return HttpResponseRedirect('/usuarios', )
        except:
            mensaje = "Error al modificar Contraseña"
    return render(request, "autenticacion/contra.html", {'mensaje': mensaje})


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
                           'username': user.username,
                           'mensaje': mensaje}
                return render(request, "autenticacion/cuenta.html", context)

        if request.POST.get('nombres'):
            user.first_name = request.POST.get('nombres')
        if request.POST.get('apellidos'):
            user.last_name = request.POST.get('apellidos')
        if request.POST.get('username'):
            user.username = request.POST.get('username')
        if request.POST.get('correo'):
            user.email = request.POST.get('correo')
        try:
            user.save()
            mensaje = "Datos modificados con éxito"
        except:
            mensaje = "Error al modificar datos"

        user = User.objects.get(pk=user.id)

        id_accion = Accion.objects.get(pk=3)
        id = id_accion.id

        new_user_bit = Bitacora.objects.create(
            Usuario_id=request.user.id,
            Accion_id=id
        )
        try:
            new_user_bit.save()
        except:
            pass

    context = {'nombre': user.first_name,
               'apellido': user.last_name,
               'email': user.email,
               'username': user.username,
               'mensaje': mensaje}
    return render(request, "autenticacion/cuenta.html", context)

# Inician vistas para Usuarios

@login_required
def usuarios(request):
    mensaje=""
    user_list=User.objects.all().exclude(pk=request.user.id)

    id_accion = Accion.objects.get(pk=4)
    id = id_accion.id

    new_user_bit = Bitacora.objects.create(
        Usuario_id=request.user.id,
        Accion_id=id
    )
    try:
        new_user_bit.save()
    except:
        pass

    return render(request, 'autenticacion/usuarios.html', {'user_list': user_list, 'mensaje': mensaje, })


def bloquear_usuario(request, pk):
    user = User.objects.get(pk=pk)
    user.is_active = not user.is_active
    user.save()
    reset(username=user.username)
    messages.add_message(request, messages.INFO, 'Cambio de estado exitoso')

    return HttpResponseRedirect(reverse("usuarios"))
# Finalizan vistas para Usuarios

# Inician vistas para Usuarios

@login_required
def registroUsuario(request):

    mensaje = ""
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    if request.method == 'POST':
        form=UsuarioForm2(request.POST or None)
        form2=RolForm(request.POST or None)

        if form.is_valid() and form2.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            first_name = form.cleaned_data['nombre']
            last_name = form.cleaned_data['apellido']
            if password2 == password:
                #new_user = User.objects.create_user(username, email, password,first_name,last_name)
                encrypted_pass = make_password(password, None, 'argon2')
                new_user = User.objects.create(
                    username=username,
                    email=email,
                    password=encrypted_pass,
                    first_name=first_name,
                    last_name=last_name
                )
                new_user.is_active = True
                rol = form2.cleaned_data['group']
                new_user.groups.add(rol)

                id_accion = Accion.objects.get(pk=1)
                id = id_accion.id

                new_user_bit = Bitacora.objects.create(
                    Usuario_id=request.user.id,
                    Accion_id=id,
                    Afectado=username
                )

                try:
                    new_user.save()
                    mensaje = "Usuario Creado con Exito"

                    new_user_bit.save()

                    form = UsuarioForm2()
                    form2 = RolForm()
                except:
                    mensaje = "Error al Crear Usuario"
            else:
                mensaje = "Contraseñas no coinciden"
                return render(request, 'autenticacion/agregar_usuarios.html', {'form': form,'form2':form2, 'mensaje': mensaje, }, )
        else:
            mensaje = "Datos no validos"
    else:
        form=UsuarioForm2()
        form2 = RolForm()

    return render(request, 'autenticacion/agregar_usuarios.html', {'form':form,'form2':form2, 'mensaje': mensaje, }, )


@login_required
def confirmar_desactivar_usuario(request, id):
    usuario = User.objects.get(pk=id)
    msj = ""
    if usuario.is_active:
        msj = "Desactivar"
    else:
        msj = "Activar"

    return render(request, 'autenticacion/confirmar.html', {'usuario': usuario, 'msj': msj, })

@login_required
def desactivar_usuario(request, id):
    usuario = User.objects.get(pk=id)
    if usuario.is_active:
        usuario.is_active = 0
    else:
        usuario.is_active = 1
        reset(username=usuario.username)
    usuario.save()

    id_accion = Accion.objects.get(pk=5)
    id = id_accion.id

    new_user_bit = Bitacora.objects.create(
        Usuario_id=request.user.id,
        Accion_id=id,
        Afectado=usuario.username
    )
    try:
        new_user_bit.save()
    except:
        pass
    messages.add_message(request, messages.INFO, 'Se Modifico Exitosamente')
    return HttpResponseRedirect('/usuarios')
# Finalizan Vistas para Usuarios