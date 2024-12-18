from django.shortcuts import render
from llama_cpp import Llama
from rest_framework import viewsets, views, response
from .serializers import MathematicianSerializer, EquationSerializer
from .models import Mathematician, Equation
from .llama_service import get_llama_response
from rest_framework.exceptions import NotFound

# views is where we define the logic of the API and handling requests!
#with drf (djangorestframework), we can use viewsets which define crud ops for us

# Create your views here.
class MathematicianViewSet(viewsets.ModelViewSet):
    queryset = Mathematician.objects.all() # get all mathematicians from db
    serializer_class = MathematicianSerializer #format data w/serializer

class EquationViewSet(viewsets.ModelViewSet):
    queryset = Equation.objects.all()
    serializer_class = EquationSerializer

class LlamaViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        return []

    def retrieve(self, request, pk=None):
        try:
            mathematician = Mathematician.objects.get(pk=pk)
        except Mathematician.DoesNotExist:
            raise NotFound(detail='Mathematician not found')

        prompt = f"Tell me briefly about {mathematician.name}, who worked in {mathematician.fields}. Mention topics such as {mathematician.name}'s history, contributions, fun facts, etc."

        llama_response = get_llama_response(prompt)

        return response.Response({
            "mathematician": mathematician.name,
            "llama_response": llama_response
        })
