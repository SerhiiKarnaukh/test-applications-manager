from .serializers import ProjectSerializer
from rest_framework import generics
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Project


class VueAppsAPIList(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        queryset = Project.objects.filter(category__slug='vuejs')
        return queryset


@api_view(['POST'])
def search_api(request):
    query = request.data.get('query', '')

    if query:
        projects = Project.objects.filter(Q(title__icontains=query)
                                          | Q(content__icontains=query),
                                          category__slug='vuejs').distinct()
        serialized_projects = ProjectSerializer(projects, many=True).data

        for project in serialized_projects:
            project['photo'] = request.build_absolute_uri(
                '/' + project['photo'].strip('/'))
            project['url'] = request.build_absolute_uri(
                '/' + project['url'].strip('/'))

        return Response(serialized_projects)

    return Response({'projects': []})
