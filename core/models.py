from django.db import models
from django.urls import reverse


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Application Web'),
        ('saas', 'SaaS / Plateforme'),
        ('fintech', 'Fintech'),
        ('ecommerce', 'E-commerce'),
        ('mobile', 'Mobile'),
        ('devops', 'DevOps / Infra'),
        ('ai', 'IA / Automatisation'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    short_desc = models.CharField(max_length=255, help_text="Pitch en une ligne")
    description = models.TextField()
    tech_stack = models.CharField(
        max_length=300,
        help_text="Django, PostgreSQL, Docker... (séparés par virgule)",
    )
    image = models.ImageField(upload_to='projects/', blank=True)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    is_live = models.BooleanField(default=False, help_text="Projet en production ?")
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',') if t.strip()]

    def get_absolute_url(self):
        return reverse('projects')

    def __str__(self):
        return self.title


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('devops', 'DevOps / Système'),
        ('cloud', 'Cloud & Infra'),
        ('monitoring', 'Supervision'),
        ('database', 'Bases de données'),
        ('ai', 'IA / Data'),
        ('tools', 'Outils'),
    ]
    name = models.CharField(max_length=80)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    level = models.PositiveSmallIntegerField(default=80, help_text="Maîtrise en % (0-100)")
    icon = models.CharField(
        max_length=60, blank=True,
        help_text="Slug Simple Icons (ex: django, docker, postgresql). Vide = icône générique.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['category', 'order']

    def icon_url(self):
        """URL SVG monochrome (Simple Icons CDN) ou None si pas de slug."""
        if self.icon:
            return f"https://cdn.simpleicons.org/{self.icon}/94a3b8"
        return None

    def __str__(self):
        return self.name


class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, blank=True, help_text="Nom de l'icône SVG")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Experience(models.Model):
    role = models.CharField(max_length=120)
    company = models.CharField(max_length=120)
    period = models.CharField(max_length=60, help_text="ex: 2024 — Présent")
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.role} @ {self.company}"


class Education(models.Model):
    school = models.CharField(max_length=160)
    degree = models.CharField(max_length=200)
    period = models.CharField(max_length=60, help_text="ex: 2019 — 2023")
    detail = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Formation'
        verbose_name_plural = 'Formations'

    def __str__(self):
        return f"{self.degree} — {self.school}"


class Certification(models.Model):
    name = models.CharField(max_length=200)
    status = models.CharField(
        max_length=60, blank=True, help_text="ex: Obtenue, En cours",
    )
    issuer = models.CharField(max_length=160, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Certification'

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=80)
    level = models.CharField(max_length=80, blank=True, help_text="ex: Natif, Technique")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Langue'
        verbose_name_plural = 'Langues'

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_role = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    avatar = models.ImageField(upload_to='testimonials/', blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.client_name


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'

    def __str__(self):
        return self.question


class Stat(models.Model):
    label = models.CharField(max_length=80)
    value = models.PositiveIntegerField(default=0)
    suffix = models.CharField(max_length=10, blank=True, help_text="ex: +, %, k")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.value}{self.suffix} {self.label}"


class About(models.Model):
    """Contenu narratif de la page « À propos » (instance unique)."""
    full_name = models.CharField(max_length=120, default='Idohou Augustin')
    headline = models.CharField(
        max_length=200, default='Backend Developer · DevOps · AI Engineer',
        help_text="Sous-titre affiché sous le nom",
    )
    photo = models.ImageField(upload_to='about/', blank=True, help_text="Photo de profil")
    location = models.CharField(max_length=120, default='Cotonou, Bénin')
    available = models.BooleanField(default=True, help_text="Disponible pour de nouveaux projets")
    resume = models.FileField(upload_to='about/', blank=True, help_text="CV téléchargeable (PDF)")

    intro = models.TextField(help_text="Court paragraphe d'introduction (le pitch).")
    mission = models.TextField(help_text="Ma mission — pourquoi je fais ce métier.")
    approach = models.TextField(blank=True, help_text="Mon approche / ma méthode de travail.")

    class Meta:
        verbose_name = 'À propos'
        verbose_name_plural = 'À propos'

    def save(self, *args, **kwargs):
        self.pk = 1  # singleton
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.full_name


class Value(models.Model):
    """Principe / valeur affiché en carte sur la page À propos."""
    title = models.CharField(max_length=120)
    description = models.TextField()
    icon = models.CharField(
        max_length=60, blank=True,
        help_text="Slug d'icône (rendu via template, ex: shield, rocket, code, server)",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    project_type = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.subject or self.project_type or 'message'}"
