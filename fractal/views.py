from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from rest_framework import views
import json
from .utils import generate_fractal

# Create your views here.
class FractalGeneratorView(views.APIView):
    def post(self, request):
        try:
            #get user inputted stuff
            data = json.loads(request.body)

            formula_str = data.get('formula')
            width = data.get('width', 800)
            height = data.get('height', 800)
            div_thresh = data.get('div_thresh', 2)
            real_bounds = data.get('realBounds', [-2.0, 1.0])
            imag_bounds = data.get('imagBounds', [-1.5, 1.5])
            max_itr = data.get('maxItr', 100)

            fractal = generate_fractal(formula_str, width, height, div_thresh, real_bounds, imag_bounds, max_itr)

            return JsonResponse({
                'fractal': fractal
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)