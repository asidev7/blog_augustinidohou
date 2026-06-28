from pathlib import Path

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import (
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

STATS = [
    {'label': 'Projets livrés', 'value': 25, 'suffix': '+'},
    {'label': "Années d'expérience", 'value': 5, 'suffix': '+'},
    {'label': 'Clients accompagnés', 'value': 15, 'suffix': '+'},
    {'label': 'Serveurs administrés', 'value': 20, 'suffix': '+'},
]

# Compétences réelles (CV) regroupées par catégorie.
SKILLS = {
    'backend': ['Python', 'Django', 'Flask', 'Laravel', 'FastAPI'],
    'frontend': ['HTML', 'CSS', 'JavaScript', 'Tailwind'],
    'devops': ['Linux', 'Bash', 'Ansible', 'Docker', 'Nginx', 'CI/CD'],
    'cloud': ['Google Cloud', 'AWS', 'Google Workspace'],
    'monitoring': ['Prometheus', 'Grafana', 'Zabbix'],
    'database': ['PostgreSQL', 'MySQL', 'Redis'],
    'tools': ['Git', 'GitHub', 'SSH', 'Active Directory'],
}

# Slugs Simple Icons (https://simpleicons.org). Vide = icône générique.
SKILL_ICONS = {
    'Python': 'python', 'Django': 'django', 'Flask': 'flask', 'Laravel': 'laravel', 'FastAPI': 'fastapi',
    'HTML': 'html5', 'CSS': 'css3', 'JavaScript': 'javascript', 'Tailwind': 'tailwindcss',
    'Linux': 'linux', 'Bash': 'gnubash', 'Ansible': 'ansible', 'Docker': 'docker',
    'Nginx': 'nginx', 'CI/CD': 'githubactions',
    'Google Cloud': 'googlecloud', 'AWS': 'amazonwebservices', 'Google Workspace': 'google',
    'Prometheus': 'prometheus', 'Grafana': 'grafana', 'Zabbix': 'zabbix',
    'PostgreSQL': 'postgresql', 'MySQL': 'mysql', 'Redis': 'redis',
    'Git': 'git', 'GitHub': 'github', 'SSH': 'openssh', 'Active Directory': '',
}

# Niveaux indicatifs par compétence (sinon 80 par défaut)
SKILL_LEVELS = {
    'Python': 92, 'Django': 92, 'Flask': 85, 'Laravel': 80, 'FastAPI': 78,
    'HTML': 92, 'CSS': 88, 'JavaScript': 80, 'Tailwind': 90,
    'Linux': 93, 'Bash': 90, 'Ansible': 82, 'Docker': 86, 'Nginx': 85, 'CI/CD': 82,
    'Google Cloud': 82, 'AWS': 70, 'Google Workspace': 88,
    'Prometheus': 80, 'Grafana': 80, 'Zabbix': 78,
    'PostgreSQL': 88, 'MySQL': 85, 'Redis': 75,
    'Git': 92, 'GitHub': 92, 'SSH': 90, 'Active Directory': 78,
}

SERVICES = [
    {
        'title': 'Développement Web Full-Stack',
        'description': "Applications web complètes avec Django et Tailwind CSS — interfaces "
                       "soignées, backend solide et code maintenable, du prototype à la production.",
    },
    {
        'title': 'Architecture Backend & API REST',
        'description': "Conception de modèles de données robustes, APIs REST documentées et "
                       "sécurisées, prêtes à alimenter web et mobile à grande échelle.",
    },
    {
        'title': 'DevOps & Déploiement',
        'description': "Mise en production reproductible : Docker, Nginx, VPS Linux, pipelines "
                       "CI/CD, sauvegardes et monitoring pour des plateformes fiables.",
    },
    {
        'title': 'Intégration IA & Automatisation',
        'description': "Intégration de LLM et d'APIs d'IA, automatisation de processus métier et "
                       "scripts sur-mesure pour gagner du temps et réduire les erreurs.",
    },
]

PROJECTS = [
    {
        'title': 'ISEMI.SHOP', 'category': 'saas',
        'short_desc': "SaaS e-commerce multi-boutiques avec paiement FedaPay (XOF).",
        'description': "Plateforme SaaS permettant à chaque marchand de lancer sa propre boutique "
                       "en ligne : catalogue, panier, commandes et paiements mobile money via FedaPay. "
                       "Architecture multi-tenant, tableau de bord vendeur et gestion des stocks.",
        'tech_stack': 'Django, PostgreSQL, FedaPay, Tailwind, Docker',
        'is_live': True, 'is_featured': True,
    },
    {
        'title': 'AgriCredit', 'category': 'fintech',
        'short_desc': "Fintech de crédit agricole : scoring, décaissement et suivi des remboursements.",
        'description': "Solution de financement pour le secteur agricole : dossiers de crédit, "
                       "scoring, échéanciers de remboursement et suivi des producteurs. Pensée pour "
                       "la traçabilité et la fiabilité des données financières.",
        'tech_stack': 'Django, Django REST, PostgreSQL, Redis',
        'is_live': True, 'is_featured': True,
    },
    {
        'title': 'GoChange', 'category': 'fintech',
        'short_desc': "Change NGN ↔ FCFA avec parcours KYC et suivi des transactions.",
        'description': "Plateforme d'échange de devises entre le naira (NGN) et le franc CFA (FCFA) : "
                       "création de compte, vérification d'identité (KYC), demandes de change et "
                       "historique des opérations sécurisé.",
        'tech_stack': 'Django, PostgreSQL, KYC, Docker, Nginx',
        'is_live': True, 'is_featured': True,
    },
    {
        'title': 'SOGETID', 'category': 'web',
        'short_desc': "Plateforme immobilière multi-rôles : biens, agents et clients.",
        'description': "Solution immobilière complète gérant plusieurs rôles (administrateurs, "
                       "agents, clients) : catalogue de biens, demandes de visite, gestion des "
                       "mandats et suivi commercial.",
        'tech_stack': 'Django, PostgreSQL, Tailwind, Alpine.js',
        'is_live': True, 'is_featured': True,
    },
    {
        'title': 'PandaTicket', 'category': 'web',
        'short_desc': "Billetterie événementielle avec billets QR Code et contrôle d'accès.",
        'description': "Système de billetterie en ligne pour événements : création d'événements, "
                       "vente de billets, génération de QR Codes uniques et contrôle d'accès à "
                       "l'entrée via scan.",
        'tech_stack': 'Django, PostgreSQL, QR Code, FedaPay',
        'is_live': True, 'is_featured': False,
    },
    {
        'title': 'FormaPro', 'category': 'web',
        'short_desc': "Gestion de centre de formation : sessions, apprenants et présences.",
        'description': "Application de gestion pour centres de formation : catalogue de formations, "
                       "inscriptions, sessions, suivi des présences et génération d'attestations.",
        'tech_stack': 'Django, PostgreSQL, Tailwind',
        'is_live': False, 'is_featured': False,
    },
    {
        'title': 'boutik.shop', 'category': 'ecommerce',
        'short_desc': "E-commerce SaaS pensé pour les marchands d'Afrique de l'Ouest.",
        'description': "Solution e-commerce SaaS clé en main pour lancer une boutique en ligne "
                       "rapidement : thèmes, catalogue, paiements mobile money et gestion des "
                       "commandes adaptée au marché ouest-africain.",
        'tech_stack': 'Django, PostgreSQL, Tailwind, Docker',
        'is_live': True, 'is_featured': True,
    },
]

ABOUT = {
    'full_name': 'Idohou Sande Augustin',
    'headline': 'Développeur Full Stack · DevOps · Administrateur Système Linux',
    'location': 'Parakou, Bénin',
    'available': True,
    'intro': "Administrateur Linux & développeur web, j'allie la gestion d'infrastructures et le "
             "développement d'applications. Expertise en systèmes Linux, automatisation, cloud "
             "(Google Workspace, GCP) et développement web. Fondateur de ASITECH SOLUTION.",
    'mission': "Ma mission : rendre la technologie utile et fiable pour les entreprises africaines. "
               "J'optimise les infrastructures IT, j'automatise les processus et je développe des "
               "outils performants — du serveur Linux jusqu'à l'application web livrée en production.\n"
               "Backend (Django, Flask, Laravel), administration système, sécurité et supervision : "
               "je couvre toute la chaîne, du premier commit au monitoring en production.",
    'approach': "Rigueur, automatisation et sécurité par défaut. Je cadre, je documente, je livre par "
                "itérations et je supervise ce que je déploie. Des résultats mesurables, pas des "
                "promesses.",
}

EDUCATION = [
    {'school': 'Université de Parakou', 'degree': 'Licence en Informatique de Gestion',
     'period': '2019 — 2023', 'detail': ''},
    {'school': 'CEG 1 Kétou', 'degree': 'Baccalauréat série C',
     'period': '2021 — 2022', 'detail': 'Sciences & Techniques'},
]

CERTIFICATIONS = [
    {'name': 'Linux Professional Institute Certification (LPIC-1)', 'status': 'Obtenue',
     'issuer': 'LPI'},
    {'name': 'Google Workspace Administrator', 'status': 'En cours', 'issuer': 'Google'},
    {'name': 'Google Cloud & Microsoft Administrator', 'status': 'En cours', 'issuer': ''},
]

LANGUAGES = [
    {'name': 'Français', 'level': 'Natif'},
    {'name': 'Anglais', 'level': 'Technique & professionnel'},
    {'name': 'Yoruba', 'level': 'Courant'},
    {'name': 'Nago', 'level': 'Courant'},
]

VALUES = [
    {'title': 'Rigueur d\'ingénieur', 'icon': 'shield', 'order': 0,
     'description': "Code testé, architecture propre, sécurité par défaut. Le détail qui fait la différence en production."},
    {'title': 'Pensé pour scaler', 'icon': 'rocket', 'order': 1,
     'description': "Des fondations solides dès le départ : modèles de données et infra qui tiennent la charge."},
    {'title': 'Du concept au déploiement', 'icon': 'server', 'order': 2,
     'description': "Un interlocuteur unique pour le backend, l'API et l'infrastructure — du premier commit à la prod."},
    {'title': 'Toujours en veille', 'icon': 'sparkles', 'order': 3,
     'description': "IA, automatisation, nouveaux outils : j'intègre ce qui apporte une vraie valeur, pas la hype."},
]

EXPERIENCES = [
    {
        'role': 'Développeur Backend', 'company': 'AFT Group', 'period': '2023 — 2024',
        'description': "Développement et maintenance d'applications web avec Laravel.\n"
                       "Gestion des serveurs Linux et configuration des services.\n"
                       "Mise en place de solutions Google Workspace pour la collaboration interne.\n"
                       "Surveillance des performances et application des correctifs de sécurité.",
    },
    {
        'role': 'Administrateur Système (Stage · USA remote)', 'company': 'BTECHNACADEMY',
        'period': '2022 — 2024',
        'description': "Administration de serveurs Linux.\n"
                       "Configuration de Google Workspace pour les utilisateurs.\n"
                       "Automatisation des sauvegardes et des mises à jour.\n"
                       "Développement et déploiement d'applications web internes.",
    },
    {
        'role': 'Développeur (Stage)', 'company': 'Light Innovation', 'period': '2021 — 2023',
        'description': "Développement et intégration de solutions web pour les clients.\n"
                       "Optimisation des performances et de la sécurité des plateformes.\n"
                       "Gestion de bases de données et d'API.\n"
                       "Tests et déploiement d'applications.",
    },
    {
        'role': 'Développeur Web — Freelance', 'company': 'Fiverr / Upwork', 'period': '2019 — 2024',
        'description': "Prestations en développement web sur Fiverr et Upwork.\n"
                       "Création de sites web et d'applications pour divers clients.\n"
                       "Gestion et optimisation des infrastructures web.",
    },
]

TESTIMONIALS = [
    {
        'client_name': 'Un client e-commerce', 'client_role': 'Marchand · ISEMI.SHOP',
        'content': "Augustin a transformé mon idée en une vraie plateforme de vente en ligne. "
                   "Le paiement mobile fonctionne parfaitement et le site est rapide.",
    },
    {
        'client_name': 'Porteur de projet fintech', 'client_role': 'Fondateur · projet de change',
        'content': "Rigueur technique et sens du détail. La partie KYC et le suivi des "
                   "transactions ont été livrés exactement comme attendu.",
    },
    {
        'client_name': 'Responsable de centre', 'client_role': 'Direction · centre de formation',
        'content': "Un interlocuteur unique du cadrage au déploiement. La gestion des présences "
                   "nous fait gagner un temps fou chaque semaine.",
    },
]

FAQS = [
    {
        'question': "Quelles technologies utilisez-vous ?",
        'answer': "Principalement Django/Python côté backend, PostgreSQL en base de données, "
                  "Tailwind CSS et Alpine.js côté frontend, et Docker/Nginx pour le déploiement. "
                  "J'intègre aussi des APIs d'IA quand le projet s'y prête.",
    },
    {
        'question': "Travaillez-vous avec des clients hors du Bénin ?",
        'answer': "Oui. Je travaille à distance avec des clients partout, avec une communication "
                  "claire, des points réguliers et des livrables documentés.",
    },
    {
        'question': "Combien de temps prend un projet ?",
        'answer': "Cela dépend du périmètre. Un MVP solide prend généralement quelques semaines ; "
                  "une plateforme SaaS complète, davantage. Je propose un planning précis après le "
                  "cadrage initial.",
    },
    {
        'question': "Gérez-vous aussi le déploiement et la maintenance ?",
        'answer': "Oui. Je déploie en production (Docker, VPS Linux, CI/CD), je mets en place les "
                  "sauvegardes et le monitoring, et je propose un suivi de maintenance.",
    },
    {
        'question': "Intégrez-vous les paiements mobile money ?",
        'answer': "Absolument. J'ai intégré FedaPay et des parcours de paiement en XOF sur "
                  "plusieurs plateformes e-commerce et de billetterie.",
    },
    {
        'question': "Comment démarrer un projet avec vous ?",
        'answer': "Écrivez-moi via la page contact ou WhatsApp avec une description de votre "
                  "besoin. On planifie un échange de cadrage, puis je reviens avec une proposition.",
    },
]


BLOG_CATEGORIES = [
    {'name': 'Django'},
    {'name': 'DevOps'},
    {'name': 'Fintech'},
    {'name': 'IA'},
]

BLOG_POSTS = [
    {
        'title': 'Déployer Django en production avec Docker, Nginx et Gunicorn',
        'category': 'DevOps', 'reading_time': 8, 'is_featured': True,
        'excerpt': "Un guide concret pour passer du serveur de dev à une mise en production "
                   "fiable : conteneurisation, reverse proxy et fichiers statiques.",
        'content': """
<p>Faire tourner <code>runserver</code> en local, c'est facile. Mettre une application Django en
production de façon fiable, c'est une autre histoire. Voici l'architecture que j'utilise sur mes
projets ASITECH.</p>
<h2>L'architecture en trois couches</h2>
<p>Le trio classique reste imbattable pour la plupart des projets :</p>
<ul>
  <li><strong>Gunicorn</strong> : le serveur d'application WSGI qui exécute Django.</li>
  <li><strong>Nginx</strong> : le reverse proxy qui termine le TLS et sert les fichiers statiques.</li>
  <li><strong>Docker</strong> : pour un déploiement reproductible, identique en staging et en prod.</li>
</ul>
<h2>Un Dockerfile minimal</h2>
<pre><code>FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]</code></pre>
<h2>Les fichiers statiques</h2>
<p>WhiteNoise simplifie énormément la donne : pas besoin de configurer Nginx pour servir le
statique, tout passe par l'application avec compression et cache busting. En activant
<code>CompressedManifestStaticFilesStorage</code>, vos assets sont versionnés automatiquement.</p>
<blockquote>Règle d'or : ne jamais déployer avec <code>DEBUG=True</code>. Vos secrets passent par des
variables d'environnement, jamais dans le code.</blockquote>
<h2>Et ensuite ?</h2>
<p>Ajoutez un pipeline CI/CD (GitHub Actions), des sauvegardes automatiques de la base et un
monitoring basique. C'est ce qui transforme un projet « qui marche » en plateforme de confiance.</p>
""",
    },
    {
        'title': 'Intégrer les paiements mobile money en XOF avec FedaPay',
        'category': 'Fintech', 'reading_time': 6, 'is_featured': False,
        'excerpt': "Mobile money est roi en Afrique de l'Ouest. Voici comment intégrer FedaPay "
                   "proprement dans une application Django, des webhooks à la réconciliation.",
        'content': """
<p>En Afrique de l'Ouest, le paiement par carte reste minoritaire. Le <strong>mobile money</strong>
(MTN, Moov) domine. FedaPay est l'un des agrégateurs les plus pratiques pour encaisser en XOF.</p>
<h2>Le flux de paiement</h2>
<ol>
  <li>L'utilisateur valide son panier, on crée une transaction côté FedaPay.</li>
  <li>On redirige vers la page de paiement (ou on utilise le widget).</li>
  <li>FedaPay notifie notre serveur via un <strong>webhook</strong> quand le paiement aboutit.</li>
  <li>On met à jour la commande uniquement après vérification du webhook.</li>
</ol>
<h2>Ne jamais faire confiance au retour client</h2>
<p>Le piège classique : valider la commande sur la redirection de retour. Un utilisateur peut
forger cette URL. La <strong>source de vérité, c'est le webhook signé</strong>, vérifié côté
serveur.</p>
<pre><code># Vérifier l'événement reçu avant de créditer la commande
if event.type == "transaction.approved":
    order = Order.objects.get(reference=event.data["reference"])
    order.mark_paid()</code></pre>
<h2>Réconciliation</h2>
<p>Gardez toujours un journal des transactions et une tâche cron qui re-vérifie les paiements en
attente. C'est indispensable pour la comptabilité et la confiance des marchands.</p>
""",
    },
    {
        'title': 'Structurer un projet Django qui passe à l\'échelle',
        'category': 'Django', 'reading_time': 7, 'is_featured': False,
        'excerpt': "Apps découplées, settings par environnement, services métier : les choix "
                   "d'architecture qui évitent la dette technique sur le long terme.",
        'content': """
<p>Un projet Django qui démarre bien mais devient ingérable au bout de six mois, c'est presque
toujours un problème d'architecture initiale. Quelques principes simples changent tout.</p>
<h2>Des apps qui ont une seule responsabilité</h2>
<p>Chaque app devrait répondre à une question claire : <em>« de quoi parle-t-elle ? »</em>. Une app
<code>payments</code>, une app <code>catalog</code>, une app <code>accounts</code>. Évitez l'app
fourre-tout <code>core</code> qui finit par tout contenir.</p>
<h2>Settings par environnement</h2>
<p>Séparez dev, staging et prod. J'utilise <code>python-decouple</code> + <code>.env</code> pour
sortir tous les secrets du code et basculer le comportement selon <code>DEBUG</code>.</p>
<h2>La logique métier hors des vues</h2>
<p>Les vues orchestrent, elles ne décident pas. La logique va dans des fonctions de service ou des
méthodes de modèle. Résultat : du code testable et réutilisable.</p>
<ul>
  <li>Vues fines, modèles riches.</li>
  <li>Migrations versionnées et relues.</li>
  <li>Tests sur la logique critique (paiement, droits d'accès).</li>
</ul>
<p>Ces choix ne coûtent rien au début et font gagner des semaines plus tard.</p>
""",
    },
    {
        'title': 'Intégrer un LLM dans une application web, sans se brûler',
        'category': 'IA', 'reading_time': 5, 'is_featured': False,
        'excerpt': "Brancher un modèle de langage sur son produit est tentant. Voici comment le "
                   "faire avec des garde-fous : coûts, latence, prompts et sécurité.",
        'content': """
<p>Ajouter de l'IA à un produit, ce n'est pas appeler une API et croiser les doigts. C'est un
composant à traiter avec les mêmes exigences que le reste de l'architecture.</p>
<h2>Maîtriser les coûts et la latence</h2>
<p>Un appel LLM est lent et facturé au token. Mettez en cache les réponses récurrentes, fixez des
limites par utilisateur et traitez les appels longs en tâche de fond (Celery, RQ).</p>
<h2>Le prompt est du code</h2>
<p>Versionnez vos prompts, testez-les, mesurez la qualité des sorties. Un prompt n'est pas une
chaîne magique : c'est une partie de votre logique métier.</p>
<blockquote>Ne faites jamais confiance à la sortie d'un modèle pour une action sensible sans
validation. Le LLM propose, votre code dispose.</blockquote>
<h2>Sécurité</h2>
<p>Attention à l'injection de prompt et à la fuite de données. Ne transmettez au modèle que ce qui
est nécessaire, et journalisez les échanges pour pouvoir auditer.</p>
""",
    },
    {
        'title': 'Mettre en place un pipeline CI/CD simple avec GitHub Actions',
        'category': 'DevOps', 'reading_time': 6, 'is_featured': False,
        'excerpt': "Automatiser tests et déploiement sans usine à gaz : un workflow GitHub Actions "
                   "qui lint, teste et déploie sur votre VPS à chaque push.",
        'content': """
<p>Le CI/CD n'est pas réservé aux grandes équipes. Même en solo, automatiser les tests et le
déploiement évite des erreurs idiotes et fait gagner un temps précieux.</p>
<h2>Trois étapes suffisent</h2>
<ol>
  <li><strong>Lint &amp; tests</strong> à chaque push et pull request.</li>
  <li><strong>Build</strong> de l'image Docker sur la branche principale.</li>
  <li><strong>Déploiement</strong> sur le VPS via SSH si tout est vert.</li>
</ol>
<pre><code>name: deploy
on:
  push:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: python manage.py test</code></pre>
<h2>Secrets et sécurité</h2>
<p>Les clés SSH et variables sensibles vivent dans les <em>GitHub Secrets</em>, jamais dans le
dépôt. Le serveur ne reçoit qu'un déploiement validé.</p>
<p>Commencez simple. Vous étofferez le pipeline au fur et à mesure que le projet grandit.</p>
""",
    },
]


class Command(BaseCommand):
    help = "Peuple la base avec le contenu réel du portfolio d'Idohou Augustin."

    def add_arguments(self, parser):
        parser.add_argument(
            '--fresh', action='store_true',
            help="Vide les tables de contenu avant de re-seeder.",
        )

    def handle(self, *args, **options):
        if options['fresh']:
            self.stdout.write(self.style.WARNING('Suppression du contenu existant...'))
            for model in (Project, Skill, Service, Experience, Testimonial, FAQ, Stat, Value,
                          Education, Certification, Language):
                model.objects.all().delete()

        # Stats
        for i, s in enumerate(STATS):
            Stat.objects.update_or_create(
                label=s['label'],
                defaults={'value': s['value'], 'suffix': s['suffix'], 'order': i},
            )

        # Skills
        order = 0
        for category, names in SKILLS.items():
            for name in names:
                Skill.objects.update_or_create(
                    name=name, category=category,
                    defaults={
                        'level': SKILL_LEVELS.get(name, 80),
                        'icon': SKILL_ICONS.get(name, ''),
                        'order': order,
                    },
                )
                order += 1

        # Services
        for i, sv in enumerate(SERVICES):
            Service.objects.update_or_create(
                title=sv['title'],
                defaults={'description': sv['description'], 'order': i, 'is_active': True},
            )

        # Projects
        for i, p in enumerate(PROJECTS):
            Project.objects.update_or_create(
                slug=slugify(p['title']),
                defaults={
                    'title': p['title'],
                    'category': p['category'],
                    'short_desc': p['short_desc'],
                    'description': p['description'],
                    'tech_stack': p['tech_stack'],
                    'is_live': p['is_live'],
                    'is_featured': p['is_featured'],
                    'order': i,
                },
            )

        # Experiences
        for i, e in enumerate(EXPERIENCES):
            Experience.objects.update_or_create(
                role=e['role'], company=e['company'],
                defaults={'period': e['period'], 'description': e['description'], 'order': i},
            )

        # Education
        for i, ed in enumerate(EDUCATION):
            Education.objects.update_or_create(
                school=ed['school'], degree=ed['degree'],
                defaults={'period': ed['period'], 'detail': ed['detail'], 'order': i},
            )

        # Certifications
        for i, c in enumerate(CERTIFICATIONS):
            Certification.objects.update_or_create(
                name=c['name'],
                defaults={'status': c['status'], 'issuer': c['issuer'], 'order': i},
            )

        # Langues
        for i, lg in enumerate(LANGUAGES):
            Language.objects.update_or_create(
                name=lg['name'], defaults={'level': lg['level'], 'order': i},
            )

        # Testimonials
        for i, t in enumerate(TESTIMONIALS):
            Testimonial.objects.update_or_create(
                client_name=t['client_name'],
                defaults={
                    'client_role': t['client_role'],
                    'content': t['content'],
                    'is_active': True,
                    'order': i,
                },
            )

        # FAQ
        for i, f in enumerate(FAQS):
            FAQ.objects.update_or_create(
                question=f['question'],
                defaults={'answer': f['answer'], 'order': i},
            )

        # About (singleton) — la photo et le CV sont (re)générés depuis les
        # fichiers source à la racine du projet (maphoto.png, CV-DEV2025.pdf).
        about = About.get()
        for field, value in ABOUT.items():
            setattr(about, field, value)
        photo_path, resume_path = self._ensure_media()
        if photo_path:
            about.photo = photo_path
        if resume_path:
            about.resume = resume_path
        about.save()

        # Valeurs / principes
        for v in VALUES:
            Value.objects.update_or_create(
                title=v['title'],
                defaults={'description': v['description'], 'icon': v['icon'], 'order': v['order']},
            )

        # Blog (si l'app est installée)
        try:
            self._seed_blog()
        except Exception as exc:  # pragma: no cover
            self.stdout.write(self.style.WARNING(f"Blog non seedé : {exc}"))

        self.stdout.write(self.style.SUCCESS(
            f"Seed terminé : {Project.objects.count()} projets, {Skill.objects.count()} skills, "
            f"{Service.objects.count()} services, {Experience.objects.count()} expériences, "
            f"{Testimonial.objects.count()} témoignages, {FAQ.objects.count()} FAQ, "
            f"{Stat.objects.count()} stats, {Value.objects.count()} valeurs, "
            f"{Education.objects.count()} formations, {Certification.objects.count()} certifs, "
            f"{Language.objects.count()} langues."
        ))

    def _ensure_media(self):
        """(Re)génère media/about/ depuis les fichiers source du dépôt.

        Retourne (chemin_photo, chemin_cv) relatifs à MEDIA_ROOT, ou None si absent.
        """
        import shutil

        from django.conf import settings

        about_dir = Path(settings.MEDIA_ROOT) / 'about'
        about_dir.mkdir(parents=True, exist_ok=True)

        photo_rel = resume_rel = None

        # Photo : optimisée en JPEG carré 640px
        src_photo = Path(settings.BASE_DIR) / 'maphoto.png'
        dest_photo = about_dir / 'idohou-augustin.jpg'
        if src_photo.exists():
            try:
                from PIL import Image
                im = Image.open(src_photo).convert('RGB').resize((640, 640), Image.LANCZOS)
                im.save(dest_photo, 'JPEG', quality=85, optimize=True)
            except Exception as exc:  # pragma: no cover
                self.stdout.write(self.style.WARNING(f"Photo non traitée : {exc}"))
        if dest_photo.exists():
            photo_rel = 'about/idohou-augustin.jpg'

        # CV : copie du PDF source
        src_cv = Path(settings.BASE_DIR) / 'CV-DEV2025.pdf'
        dest_cv = about_dir / 'CV-Idohou-Augustin.pdf'
        if src_cv.exists():
            shutil.copyfile(src_cv, dest_cv)
        if dest_cv.exists():
            resume_rel = 'about/CV-Idohou-Augustin.pdf'

        return photo_rel, resume_rel

    def _seed_blog(self):
        from blog.models import Category, Post

        for i, c in enumerate(BLOG_CATEGORIES):
            Category.objects.update_or_create(
                slug=slugify(c['name']),
                defaults={'name': c['name'], 'order': i},
            )

        for i, p in enumerate(BLOG_POSTS):
            category = Category.objects.filter(slug=slugify(p['category'])).first()
            Post.objects.update_or_create(
                slug=slugify(p['title']),
                defaults={
                    'title': p['title'],
                    'category': category,
                    'excerpt': p['excerpt'],
                    'content': p['content'],
                    'reading_time': p['reading_time'],
                    'is_published': True,
                    'is_featured': p.get('is_featured', False),
                    'order': i,
                },
            )
        count = Post.objects.count()
        self.stdout.write(self.style.SUCCESS(f"Blog seedé : {count} articles."))
