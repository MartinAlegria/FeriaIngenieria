from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from .models import Project, Categoria
from django.contrib.auth.decorators import login_required
from users.models import Alumno, Profesor
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


# Create your views here.

@login_required
def home(request):
    context = {
        'projects': Project.objects.all(),
    }
    return render(request, 'feria_ing/home.html', context)

class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        alum = []
        list_al = Alumno.objects.all()
        project_id = self.kwargs['pk']
        ld_user = self.request.user
        self.request.session['pk'] = project_id
        mat = ld_user.username.split('@')[0]
        current_user = None
        for al in list_al:
            if al.matricula == mat:
                current_user = al
            if al.proyecto_id == project_id:
                alum.append(al)
        context['alumnos'] = alum
        context['user_current'] = current_user
        return context

@login_required
def unirse_proyecto(request):
    ld_user = request.user
    project_id = request.session.get('pk', None)
    mat = ld_user.username.split('@')[0]
    list_al = Alumno.objects.filter(matricula = mat)
    project_object = Project.objects.filter(id = project_id).first()
    print(project_object)
    alumno = list_al.first()
    print(alumno)
    alumno.proyecto = project_object
    alumno.save()

    messages.success(request, f'{alumno.nombres} {alumno.apellidos} se ha unido al proyecto {project_object.nombre}!')
    return redirect('feria_ing-home')


    
    

@login_required
def search_bar(request):
    query = request.GET.get('q')
    print(query)
    if query:
        results =  Project.objects.filter(
            Q(nombre__icontains=query)
        )
    
        context = {
            'projects': results
        }
        return render(request, 'feria_ing/home.html', context)
    else:
        return render(request, 'feria_ing/home.html')
    

