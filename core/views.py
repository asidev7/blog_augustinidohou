from collections import OrderedDict

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from .forms import ContactForm
from .models import (
    About,
    Certification,
    Education,
    Experience,
    FAQ,
    Language,
    Project,
    Service,
    Skill,
    Stat,
    Testimonial,
    Value,
)


def _skills_by_category():
    """Regroupe les compétences par libellé de catégorie, dans l'ordre défini."""
    grouped = OrderedDict()
    label_map = dict(Skill.CATEGORY_CHOICES)
    for skill in Skill.objects.all():
        label = label_map.get(skill.category, skill.category)
        grouped.setdefault(label, []).append(skill)
    return grouped


def home(request):
    context = {
        'stats': Stat.objects.all(),
        'skills_by_category': _skills_by_category(),
        'featured_projects': Project.objects.filter(is_featured=True)[:4],
        'services': Service.objects.filter(is_active=True),
        'experiences': Experience.objects.all(),
        'testimonials': Testimonial.objects.filter(is_active=True),
    }
    return render(request, 'pages/home.html', context)


def about(request):
    context = {
        'about': About.get(),
        'values': Value.objects.all(),
        'skills_by_category': _skills_by_category(),
        'experiences': Experience.objects.all(),
        'stats': Stat.objects.all(),
        'services': Service.objects.filter(is_active=True),
    }
    return render(request, 'pages/about.html', context)


def projects(request):
    context = {
        'projects': Project.objects.all(),
        'categories': Project.CATEGORY_CHOICES,
    }
    return render(request, 'pages/projects.html', context)


def services(request):
    context = {
        'services': Service.objects.filter(is_active=True),
        'faqs': FAQ.objects.all(),
    }
    return render(request, 'pages/services.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            instance = form.save()
            try:
                send_mail(
                    subject=f"[Portfolio] {instance.subject or instance.project_type or 'Nouveau message'}",
                    message=(
                        f"De : {instance.name} <{instance.email}>\n"
                        f"Type de projet : {instance.project_type or '—'}\n\n"
                        f"{instance.message}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(
                request,
                "Merci ! Votre message a bien été envoyé. Je vous réponds très vite.",
            )
            return redirect('contact')
        messages.error(request, "Veuillez corriger les erreurs du formulaire.")
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})


def faq(request):
    return render(request, 'pages/faq.html', {'faqs': FAQ.objects.all()})


def cv(request):
    context = {
        'about': About.get(),
        'skills_by_category': _skills_by_category(),
        'experiences': Experience.objects.all(),
        'education': Education.objects.all(),
        'certifications': Certification.objects.all(),
        'languages': Language.objects.all(),
    }
    return render(request, 'pages/cv.html', context)
