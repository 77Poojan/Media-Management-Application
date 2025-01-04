from django.shortcuts import render

# Create your views here.
def example_view(request):
    return render(request, 'main.html')  # Path to your HTML file in templates folder