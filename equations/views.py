from django.shortcuts import render
from llama_cpp import Llama
from rest_framework import viewsets, views, response
from .serializers import MathematicianSerializer, EquationSerializer
from .models import Mathematician, Equation
from .llama_service import get_llama_response, random_mathematician_ask_llama
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action

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


    @action(detail=False, methods=['get'])
    def random_mathematician(self, request):
        mathematician_name, llama_response = random_mathematician_ask_llama()
        return response.Response({
            "mathematician": mathematician_name,
            "llama_response": llama_response
        })
    
    @action(detail=False, methods=['get'])
    def find_mathematician(self, request):
        name = request.query_params.get('name', '').strip() #get name from http request

        if not name:
            return response.Response({
                "error": "no name provided"
            }, status=400)

        mathematician = Mathematician.objects.filter(name__icontains=name).first() #grab first mathematician with name containing name, case insenstive

        if not mathematician:
            raise NotFound(detail='Mathematician not found')

        prompt = f"Tell me briefly about {mathematician.name}, who worked in {mathematician.fields}. Mention topics such as {mathematician.name}'s history, contributions, fun facts, etc."

        llama_response = get_llama_response(prompt)

        return response.Response({
            "mathematician": mathematician.name,
            "llama_response": llama_response
        })

    @action(detail=False, methods=['get'])
    def query_llama(self, request):
        prompt = request.query_params.get('prompt', "").strip()

        if not prompt:
            return response.Response({
                'error': "no prompt provided"
            }, status=400)
        
        llama_response = get_llama_response(prompt)

        return response.Response({
            "llama_response": llama_response
        })  
