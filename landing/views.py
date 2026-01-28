from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import json


def landing_page(request):
    return render(request, 'landing/index.html')

@csrf_exempt
def contact_form(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '')
            email = data.get('email', '')
            message = data.get('message', '')
            
            if not all([name, email, message]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Todos os campos são obrigatórios'
                })
            
            # Email content
            subject = f'Novo Contato de {name}'
            body = f"""
Nome: {name}
Email: {email}

Mensagem:
{message}
            """
            
            # Send email
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                ['davincigestaotech@gmail.com'],
                fail_silently=False,
            )
            
            return JsonResponse({
                'status': 'success',
                'message': 'Mensagem enviada com sucesso! Entraremos em contato em breve.'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Erro ao enviar mensagem: {str(e)}'
            }, status=500)
    return JsonResponse({'status': 'error', 'message': 'Método não permitido'})
