from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
# we need t restrict the user
from django.contrib.auth.mixins import LoginRequiredMixin
# register 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

# Create your views here.
# login view

class CustomisedLogin(LoginView):
    template_name='mytodo/login.html'
    fields='__all__'
    redirect_authenticated_user='tasks'
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    
    
#registration view
class CustomRegisterPage(FormView):
    template_name='mytodo/register.html'
    form_class=UserCreationForm 
    success_url=reverse_lazy('tasks')
    
    
    def form_valid(self, form):
        user=form.save()
        if user is not None:
            login(self.request, user)
        
        return super(CustomRegisterPage,self).form_valid(form)
    
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(CustomRegisterPage,self).get(*args,**kwargs)



# list view

class TaskList(LoginRequiredMixin,ListView):
    model=Task
    context_object_name='tasks'
    # we want to get user specific data
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tasks']=context['tasks'].filter(user=self.request.user)
        context["count"] = context["tasks"].filter(completed=False).count()
        # search_input=self.request.GET.get('search-area') or ' '
        # if search_input:
        #    context['tasks']=context['tasks'].filter(title__startswith=search_input)
        # context['search_input']=search_input
        
        return context

    
    
class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name='task'
        
class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    fields=['title','description','completed']
    success_url=reverse_lazy('tasks')
    
    # ensure no one can edit another persons list
    # so we override a form
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super(TaskCreate,self).form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView):
     model=Task
     fields=['title','description','completed']
     success_url=reverse_lazy('tasks')        
     
class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task   
    fields='__all__'
    success_url=reverse_lazy('tasks')    