import operator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from users import forms
from users.forms import EvaluationForm
from .models import Project, Categoria
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from users.models import Alumno, Profesor, Evaluacion
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
    list_al = Alumno.objects.all()
    prof_list = Profesor.objects.all()
    ld_user = request.user
    mat = ld_user.username.split('@')[0]
    print(mat)
    current_user = None

    for al in list_al:
            if al.matricula == mat:
                current_user = al
    #No encuentra alumno, entonces es prof
    if current_user:
        type = True #Es alumno
    else:
        type= False

    for prof in prof_list:
        if prof.matricula == mat:
                current_user = prof

    context = {
        'projects': Project.objects.all(),
        'user_current': current_user,
        'type': type
    }
    return render(request, 'feria_ing/home.html', context)

class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(ProjectDetailView, self).get_context_data(**kwargs)
        alum = []

        list_al = Alumno.objects.all()
        prof_list = Profesor.objects.all()

        project_id = self.kwargs['pk']
        project = Project.objects.get(id = project_id)
        ld_user = self.request.user
        self.request.session['pk'] = project_id
        mat = ld_user.username.split('@')[0]
        eva_list =  Evaluacion.objects.all().filter(proyecto = project_id, profesor = mat)
        evas = Evaluacion.objects.all().filter(proyecto = project_id)
        numero_ev = evas.count()

        current_user = None

        for al in list_al:
            if al.matricula == mat:
                current_user = al
            if al.proyecto_id == project_id:
                alum.append(al)

        if current_user:
            type = True #Es alumno
        else:
            type= False #Es prof

        for prof in prof_list:
            if prof.matricula == mat:
                current_user = prof
            
        if eva_list:    
            evaluated = True
        else:
            evaluated = False
            numero_ev = 1

        numero_ev = project.evaluaciones/numero_ev

        context['alumnos'] = alum
        context['user_current'] = current_user
        context['type'] = type
        context['evaluated'] = evaluated
        context['calificacion'] = numero_ev
        return context

class ProjectCreateView(LoginRequiredMixin,CreateView):
    model = Project
    fields = ['nombre', 'descripcion', 'categorias', 'requierements']

    def form_valid(self, form):
        last_id = Project.objects.last().id
        if not last_id:
            last_id = 0
        new_id = last_id +1
        form.instance.id = new_id
        form.instance.evaluaciones = 0

        ld_user = self.request.user
        mat = ld_user.username.split('@')[0]
        list_al = Alumno.objects.filter(matricula = mat)
        alumno = list_al.first()
        print(form.instance)
        projecto = form.instance
        cat = form.instance.categorias
        num_proyectos = cat.num_proyectos + 1
        cat.num_proyectos = num_proyectos
        cat.save()
        projecto.save()
        alumno.proyecto = projecto
        alumno.save()
        return super(ProjectCreateView, self).form_valid(form)
    


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
def salir_projecto(request):
    ld_user = request.user
    project_id = request.session.get('pk', None)
    mat = ld_user.username.split('@')[0]
    list_al = Alumno.objects.filter(matricula = mat)
    project_object = Project.objects.filter(id = project_id).first()
    print(project_object)
    alumno = list_al.first()
    print(alumno)
    alumno.proyecto = None
    alumno.save()

    al_proy = Alumno.objects.filter(proyecto = project_object)
    if al_proy.count() == 0:
        cat = Categoria.objects.get(abreviacion = project_object.categorias.abreviacion)
        cat.num_proyectos -= 1
        cat.save()
        project_object.delete()
        
    messages.success(request, f'{alumno.nombres} {alumno.apellidos} ha salido del proyecto proyecto {project_object.nombre} :(')
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

@login_required
def evauluar(request):
    form = forms.EvaluationForm(request.POST)
    project_id = request.session.get('pk', None)
    project = Project.objects.filter(id = project_id).first()
    ld_user = request.user
    mat = ld_user.username.split('@')[0]
    profe = Profesor.objects.filter(matricula = mat).first()

    if request.method == 'POST':
        form = forms.EvaluationForm(request.POST)
        planteamiento = request.POST['ejecucion']
        planteamiento = int(planteamiento)
        ejecucion = request.POST['ejecucion1']
        ejecucion = int(ejecucion)
        presentacion = request.POST['ejecucion2']
        presentacion = int(presentacion)

        print(planteamiento,ejecucion,presentacion)

        calif = planteamiento + ejecucion + presentacion
        project.evaluaciones += calif
        evaluacion = Evaluacion(proyecto = project, profesor = profe, calificacion = calif)
        evaluacion.save()
        print(calif,project,project, evaluacion)
        project.save()
        evaluacion.save()

        messages.success(request, f'Has calificado el proyecto {project.nombre}, con {calif}!')
        return redirect('feria_ing-home')
        
    return render(request, 'users/evaluar.html', {'form':form, 'project': project})


@login_required
def leaderboard(request):

    #Hacer lista de proyectos ordenados por sus calificaciones
    project_list = Project.objects.all()
    project_dict = {}
    for project in project_list:   
        evas = Evaluacion.objects.all().filter(proyecto = project.id)
        count = evas.count()
        if count == 0:
            count = 1
        project_dict[project.id] = project.evaluaciones/count

    sorted_projects = sorted(project_dict.items(), key=operator.itemgetter(1))
    sorted_projects.reverse()
    
    projects_final = []
    califs_final = []

    #Pasar la lista de tuplas a lista de objects
    for thing in sorted_projects:
        proj = Project.objects.get(id = thing[0])
        calif = thing[1]
        projects_final.append(proj)
        califs_final.append(calif)

    
    #Sacar el usuario
    list_al = Alumno.objects.all()
    prof_list = Profesor.objects.all()
    ld_user = request.user
    mat = ld_user.username.split('@')[0]
    print(mat)
    current_user = None

    for al in list_al:
            if al.matricula == mat:
                current_user = al
    #No encuentra alumno, entonces es prof
    if current_user:
        type = True #Es alumno
    else:
        type= False

    for prof in prof_list:
        if prof.matricula == mat:
                current_user = prof

    context = {
        'projects': projects_final,
        'user_current': current_user,
        'type': type,
        'califs': califs_final,
        'range': range(1,11)
    }

    return render(request, 'feria_ing/leaderboard.html', context)

@login_required
def cat_projs(request, categoria):
    proj_list_by_cat = Project.objects.filter(categorias = categoria)
    count = proj_list_by_cat.count()
    name = Categoria.objects.get(abreviacion = categoria)

    list_al = Alumno.objects.all()
    prof_list = Profesor.objects.all()
    ld_user = request.user
    mat = ld_user.username.split('@')[0]
    print(mat)
    current_user = None

    for al in list_al:
            if al.matricula == mat:
                current_user = al
    #No encuentra alumno, entonces es prof
    if current_user:
        type = True #Es alumno
    else:
        type= False

    for prof in prof_list:
        if prof.matricula == mat:
                current_user = prof

    context = {
        'projects': proj_list_by_cat,
        'user_current': current_user,
        'type': type,
        'name': name,
        'count': count
    }
    return render(request, 'feria_ing/project_by_cat.html', context)



    
