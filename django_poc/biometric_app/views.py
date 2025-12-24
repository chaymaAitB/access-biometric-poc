from django.shortcuts import render

# Page principale : montre succès ou échec
def home(request):
    # Par défaut, pas encore testé
    result = request.GET.get('result', '')
    return render(request, 'home.html', {'result': result})

# Page pour intégrer les tests biométriques
def biometric_test(request):
    return render(request, 'biometric_test.html')