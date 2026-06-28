from django.conf import settings


def site_info(request):
    """Infos de marque/contact disponibles dans tous les templates."""
    return {
        'SITE': {
            'name': 'Idohou Augustin',
            'role': 'Développeur Full Stack · DevOps · Admin Système Linux',
            'agency': 'ASITECH SOLUTION',
            'email': getattr(settings, 'CONTACT_EMAIL', 'asidev7@gmail.com'),
            'email_alt': 'contact@idohouaugustin.com',
            'phone': '+229 01 90 77 68 88',
            'phone_alt': '+229 01 64 00 36 75',
            'location': 'Parakou, Bénin',
            'whatsapp': '+229 01 90 77 68 88',
            'whatsapp_link': 'https://wa.me/2290190776888',
            'github': 'https://github.com/asidev7',
            'github_handle': 'github.com/asidev7',
            'linkedin': 'https://www.linkedin.com/in/idohou-augustin',
            'website': 'https://idohouaugustin.com',
            'website_handle': 'idohouaugustin.com',
            'agency_url': 'https://asitechsolution.com',
        }
    }
