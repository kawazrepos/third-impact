from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView

from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotAllowed
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView

from .forms import ProjectCreateForm
from .forms import ProjectUpdateForm

from .models import Project

from permission.decorators import permission_required

@permission_required('projects.add_project')
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectCreateForm

    def form_valid(self, form):
        form.instance.administrator = self.request.user
        return super().form_valid(form)


@permission_required('projects.change_project')
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectUpdateForm


@permission_required('projects.delete_project')
class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('projects_project_list')


@permission_required('projects.view_project')
class ProjectDetailView(DetailView):
    model = Project


class ProjectListView(ListView):
    model = Project

    def get_queryset(self):
        return Project.objects.published(self.request.user)

class ProjectJoinMixin(object):
    model = Project

    def join(self, request, *args, **kwargs):
        """
        Calls the join() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.join(request.user)
            return HttpResponseRedirect(success_url)
        except PermissionDenied:
            return HttpResponseForbidden

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])

    def post(self, request, *args, **kwargs):
        return self.join(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()


class BaseProjectJoinView(ProjectJoinMixin, BaseDetailView):
    ''''''


@permission_required('projects.join_project')
class ProjectJoinView(SingleObjectTemplateResponseMixin, BaseProjectJoinView):
    '''The view class to enable users to join to the specific project'''


class ProjectQuitMixin(object):
    model = Project

    def quit(self, request, *args, **kwargs):
        """
        Calls the quit() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.quit(request.user)
            return HttpResponseRedirect(success_url)
        except PermissionDenied:
            return HttpResponseForbidden

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST',])

    def post(self, request, *args, **kwargs):
        return self.quit(request, *args, **kwargs)

    def get_success_url(self):
        return self.object.get_absolute_url()

class BaseProjectQuitView(ProjectQuitMixin, BaseDetailView):
    ''''''

@permission_required('projects.quit_project')
class ProjectQuitView(SingleObjectTemplateResponseMixin, BaseProjectQuitView):
    '''The view class to enable users to quit from the specific project'''
