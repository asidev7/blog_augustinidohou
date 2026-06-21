from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.articles.models import Article, Auteur, Categorie, Tag
from apps.core.models import ParametresSite
from apps.core.seed_utils import fetch_cover

# --- Rubriques orientées "développeur / tech" -------------------------------
RUBRIQUES = [
    ("Portrait", "#F5A623", "Qui est Augustin Idohou : parcours, vision et engagements."),
    ("ASITECH", "#FF8C00", "L'entreprise et ses solutions numériques pour l'Afrique."),
    ("Projets", "#FFC107", "Applications web, mobiles et fintech réalisées."),
    ("Développement", "#E0A100", "Django, React, Flutter : pratiques et retours d'expérience."),
    ("Intelligence Artificielle", "#D98E00", "Chatbots, automatisation et IA appliquée."),
    ("Tutoriels", "#FFB300", "Guides pas-à-pas pour développeurs."),
]

ARTICLES = [
    {
        "titre": "Qui est Augustin Idohou, développeur full-stack et fondateur d'ASITECH",
        "rub": "Portrait",
        "tags": ["Augustin Idohou", "Bénin", "Carrière"],
        "chapeau": "Développeur full-stack passionné par le web, le mobile et l'intelligence artificielle, "
                   "Augustin Sandé Idohou construit depuis le Bénin des solutions numériques intelligentes "
                   "à travers son entreprise ASITECH.",
        "une": True, "epingle": True,
        "contenu": """<p><strong>Augustin Sandé Idohou</strong> est un développeur full-stack béninois, fondateur d'<strong>ASITECH</strong>, une structure spécialisée dans la création de solutions numériques intelligentes. Originaire de Parakou, il met la technologie au service des entreprises et des particuliers en Afrique de l'Ouest.</p>
<p>Étudiant en Informatique de gestion à l'IUT de l'Université de Parakou, il a très tôt développé une passion pour le code. Il conçoit aussi bien des sites web que des applications de bureau et mobiles, et aime explorer en continu de nouveaux langages et frameworks.</p>
<blockquote>« Construire des solutions numériques intelligentes depuis le Bénin » — telle est la ligne directrice de son travail.</blockquote>
<p>Son terrain de jeu favori : <strong>Python / Django</strong> pour le back-end, les frameworks JavaScript modernes (<strong>React, Vue.js</strong>) pour le front-end, et <strong>Flutter</strong> pour le mobile. Il s'intéresse également de près à l'intelligence artificielle et à la conception de chatbots.</p>
<p>En quelques années, il a travaillé sur des plateformes e-learning, des sites e-commerce, des systèmes fintech, des chatbots IA et des plateformes sociales — un parcours qui mêle créativité, rigueur technique et esprit entrepreneurial.</p>"""
    },
    {
        "titre": "ASITECH : des solutions numériques intelligentes depuis le Bénin",
        "rub": "ASITECH",
        "tags": ["ASITECH", "Entreprise", "Bénin"],
        "chapeau": "Fondée par Augustin Idohou, ASITECH accompagne entreprises et porteurs de projets dans "
                   "leur transformation numérique : sites web, applications mobiles, fintech et IA.",
        "une": True,
        "contenu": """<p><strong>ASITECH</strong> est née d'une conviction simple : l'Afrique a besoin d'outils numériques pensés pour ses réalités. L'entreprise conçoit des produits sur mesure, du site vitrine à la plateforme métier complète.</p>
<p>Son offre couvre plusieurs domaines :</p>
<ul>
<li><strong>Développement web</strong> : sites institutionnels, plateformes e-commerce et applications métier sous Django et React.</li>
<li><strong>Applications mobiles</strong> : développement multiplateforme avec Flutter et Firebase.</li>
<li><strong>Fintech</strong> : systèmes de paiement, de change et de gestion financière.</li>
<li><strong>Intelligence artificielle</strong> : chatbots, automatisation et intégration d'API d'IA.</li>
</ul>
<p>Au-delà de la technique, ASITECH se veut un partenaire de proximité : accompagnement, formation et maintenance font partie intégrante de ses prestations.</p>
<p>L'objectif reste constant : <em>mettre la puissance du numérique entre les mains des acteurs locaux</em>.</p>"""
    },
    {
        "titre": "GoChange : une application d'échange FCFA ⇄ crypto",
        "rub": "Projets",
        "tags": ["Fintech", "Projets", "Django"],
        "chapeau": "Parmi les projets phares d'Augustin Idohou, GoChange propose une expérience simple et "
                   "sécurisée pour convertir des francs CFA en cryptomonnaies et inversement.",
        "une": False,
        "contenu": """<p><strong>GoChange</strong> illustre l'approche fintech d'Augustin Idohou : rendre accessible un service souvent perçu comme complexe. L'application permet d'échanger des <strong>francs CFA contre des cryptomonnaies</strong>, et inversement, avec un parcours utilisateur épuré.</p>
<p>Côté technique, le projet s'appuie sur un back-end <strong>Django</strong> exposant une API REST, couplé à une application mobile. La sécurité et la vérification d'identité (KYC) y occupent une place centrale.</p>
<p>Ce type de projet répond à un besoin réel en Afrique de l'Ouest : faciliter l'accès aux actifs numériques tout en respectant les contraintes réglementaires et de sécurité.</p>
<p>GoChange s'inscrit dans une série de réalisations fintech, aux côtés d'autres projets explorant la blockchain et les paiements numériques.</p>"""
    },
    {
        "titre": "Construire une API de gestion de dépenses avec Django",
        "rub": "Développement",
        "tags": ["Django", "API", "Tutoriels"],
        "chapeau": "Retour d'expérience sur la conception d'une API fintech de suivi des dépenses : "
                   "architecture, sécurité et bonnes pratiques avec Django REST Framework.",
        "une": False,
        "contenu": """<p>Une <strong>API de gestion de dépenses</strong> bien conçue repose sur quelques principes solides. Voici les grandes lignes d'une architecture éprouvée avec <strong>Django</strong> et Django REST Framework.</p>
<p><strong>1. Modélisation claire.</strong> On distingue les comptes, les catégories de dépenses et les transactions. Chaque transaction est rattachée à un utilisateur, horodatée et catégorisée.</p>
<p><strong>2. Authentification robuste.</strong> Les jetons (JWT) sécurisent l'accès, et chaque requête est filtrée pour qu'un utilisateur ne voie que ses propres données.</p>
<p><strong>3. Endpoints REST.</strong> Des routes claires (<code>/transactions/</code>, <code>/categories/</code>, <code>/stats/</code>) avec pagination et filtres facilitent l'intégration côté mobile ou web.</p>
<blockquote>La règle d'or : valider côté serveur, ne jamais faire confiance au client.</blockquote>
<p>Enfin, des statistiques agrégées (dépenses par mois, par catégorie) offrent une vraie valeur ajoutée à l'utilisateur final. C'est ce genre de détails qui transforme une API fonctionnelle en produit réellement utile.</p>"""
    },
    {
        "titre": "Mon parcours : du no-code Kodular au full-stack Django et IA",
        "rub": "Portrait",
        "tags": ["Carrière", "Augustin Idohou", "Bénin"],
        "chapeau": "De ses premières applications créées avec Kodular à la maîtrise de Django et de "
                   "l'intelligence artificielle, retour sur un parcours guidé par la curiosité.",
        "une": False,
        "contenu": """<p>Tout a commencé par la curiosité. Mes premiers pas dans le développement se sont faits avec <strong>Kodular</strong>, une plateforme no-code permettant de créer des applications Android par glisser-déposer. J'y ai appris la logique applicative avant même d'écrire du code « classique ».</p>
<p>Très vite, l'envie d'aller plus loin m'a poussé vers la programmation : PHP, Java, C#, puis <strong>Python</strong>, devenu mon langage de prédilection. Django m'a ouvert les portes du développement web professionnel.</p>
<p>En parallèle de mes études en Informatique de gestion à l'<strong>IUT de Parakou</strong>, j'ai multiplié les expériences : design de chatbots, missions freelance, gestion de projets numériques.</p>
<p>Aujourd'hui, je conjugue back-end Django, front-end React/Vue, mobile Flutter et <strong>intelligence artificielle</strong>. Chaque projet est l'occasion d'apprendre quelque chose de nouveau — et c'est précisément ce qui me passionne.</p>
<p><em>« Apprendre, construire, recommencer » : c'est le moteur de toute ma démarche.</em></p>"""
    },
    {
        "titre": "Ma stack technique : Django, React, Flutter et l'intelligence artificielle",
        "rub": "Développement",
        "tags": ["Django", "React", "IA"],
        "chapeau": "Tour d'horizon des technologies au cœur de mon travail quotidien, du back-end à "
                   "l'intelligence artificielle, en passant par le mobile.",
        "une": False,
        "contenu": """<p>Choisir ses outils, c'est déjà la moitié du travail. Voici la <strong>stack technique</strong> que j'utilise au quotidien pour livrer des produits fiables et maintenables.</p>
<ul>
<li><strong>Back-end :</strong> Python et <strong>Django</strong> (avec Django REST Framework pour les API).</li>
<li><strong>Front-end :</strong> <strong>React</strong>, Vue.js, TypeScript, HTML5/CSS3 et Bootstrap.</li>
<li><strong>Mobile :</strong> <strong>Flutter</strong> et Firebase pour des applications multiplateformes.</li>
<li><strong>Bases de données :</strong> PostgreSQL et MySQL.</li>
<li><strong>Intelligence artificielle :</strong> intégration d'API d'IA et conception de chatbots.</li>
<li><strong>Outils :</strong> Git, Postman, et des plateformes de design comme Adobe XD.</li>
</ul>
<p>Cette combinaison me permet de couvrir l'ensemble du cycle de vie d'un projet : de la maquette à la mise en production, en passant par l'automatisation et le déploiement.</p>
<p>L'essentiel n'est pas d'empiler les technologies, mais de choisir la bonne pour chaque besoin — et de livrer des solutions qui apportent une réelle valeur.</p>"""
    },
]


class Command(BaseCommand):
    help = "Contenu réel : site d'Augustin Idohou (remplace la démo Ensoleillé)."

    def handle(self, *args, **opts):
        # --- Paramètres du site -------------------------------------------
        params = ParametresSite.load()
        params.nom_site = "Augustin Idohou"
        params.slogan = "Développeur full-stack & fondateur d'ASITECH"
        params.description = (
            "Le blog d'Augustin Idohou : développement web et mobile, Django, "
            "intelligence artificielle et solutions numériques depuis le Bénin."
        )
        params.email_contact = "sandeaugustinidohou@gmail.com"
        params.facebook = "https://www.facebook.com/"
        params.twitter = "https://twitter.com/"
        params.youtube = "https://www.youtube.com/"
        params.save()
        self.stdout.write(self.style.SUCCESS("Paramètres du site mis à jour → Augustin Idohou"))

        # --- On repart sur des rubriques propres --------------------------
        Article.objects.all().delete()
        Categorie.objects.all().delete()
        cats = {}
        for i, (nom, couleur, desc) in enumerate(RUBRIQUES):
            cats[nom] = Categorie.objects.create(nom=nom, couleur=couleur, description=desc, ordre=i)
        self.stdout.write(self.style.SUCCESS(f"{len(cats)} rubriques."))

        # --- Auteur = Augustin Idohou -------------------------------------
        admin = User.objects.filter(is_superuser=True).first()
        auteur, _ = Auteur.objects.get_or_create(
            nom="Augustin Sandé Idohou",
            defaults={
                "role": "Développeur full-stack — Fondateur d'ASITECH",
                "bio": "Développeur full-stack passionné par le web, le mobile et l'IA. "
                       "Fondateur d'ASITECH, je construis des solutions numériques intelligentes depuis le Bénin.",
                "user": admin,
                "facebook": "https://www.facebook.com/",
                "twitter": "https://twitter.com/",
            },
        )

        # --- Tags ---------------------------------------------------------
        tag_cache = {}

        def get_tags(noms):
            objs = []
            for n in noms:
                if n not in tag_cache:
                    tag_cache[n] = Tag.objects.get_or_create(nom=n)[0]
                objs.append(tag_cache[n])
            return objs

        # --- Articles -----------------------------------------------------
        kw_par_rub = {
            "Portrait": "developer,laptop,startup",
            "ASITECH": "startup,office,technology",
            "Projets": "fintech,cryptocurrency,money",
            "Développement": "programming,code,computer",
            "Intelligence Artificielle": "artificial-intelligence,technology",
            "Tutoriels": "code,programming,keyboard",
        }
        now = timezone.now()
        created = 0
        for i, data in enumerate(ARTICLES):
            art = Article(
                titre=data["titre"],
                chapeau=data["chapeau"],
                contenu=data["contenu"],
                categorie=cats[data["rub"]],
                auteur=auteur,
                statut="publie",
                a_la_une=data.get("une", False),
                epingle=data.get("epingle", False),
                credit_image="© ASITECH",
                date_publication=now - timedelta(days=i, hours=i * 2),
                nombre_vues=(len(ARTICLES) - i) * 95,
            )
            art.image_couverture.save(
                "cover.jpg",
                fetch_cover(f"augustin-{i}", keywords=kw_par_rub.get(data["rub"], "developer,technology")),
                save=False,
            )
            art.save()
            art.tags.set(get_tags(data["tags"]))
            created += 1
        self.stdout.write(self.style.SUCCESS(f"{created} articles publiés."))
        self.stdout.write(self.style.SUCCESS("Contenu Augustin Idohou en place. → /"))
