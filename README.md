# Portfolio — Augustin Sande Idohou

Portfolio personnel d'**Augustin Sande Idohou** — Backend Developer · DevOps · AI Engineer,
fondateur de **ASITECH SOLUTION**.

Stack : **Django 5 · Tailwind CSS 3 · Alpine.js · GSAP / AOS**. Dark mode technique, animations
sobres, focus sur le code et les projets en production.

---

## 🚀 Démarrage rapide (développement)

```bash
# 1. Dépendances Python (venv recommandé)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Configuration
cp .env.example .env        # facultatif en dev : SQLite + DEBUG par défaut

# 3. Build du CSS Tailwind (Node requis)
npm install
npm run build:css           # ou `npm run watch:css` pendant le dev

# 4. Base de données + contenu réel
python manage.py migrate
python manage.py seed        # peuple projets, skills, services, FAQ, etc.
python manage.py createsuperuser

# 5. Lancer
python manage.py runserver
```

Site sur http://127.0.0.1:8000 · Admin sur http://127.0.0.1:8000/admin/

---

## 🧱 Structure

```
augustin_portfolio/   # config Django (settings, urls, wsgi, asgi)
core/                 # portfolio : Project, Skill, Service, Experience,
                      #   Testimonial, FAQ, Stat, About, Value + seed
blog/                 # blog : Category, Post (liste paginée, détail, sitemap)
templates/            # base, partials/, pages/, blog/
static/               # css (src + main compilé), js, img (logo/og SVG)
tailwind.config.js    # thème (couleurs : Sora display + Inter + JetBrains Mono)
package.json          # build Tailwind CLI
```

Typo : **Sora** (titres) · **Inter** (corps) · **JetBrains Mono** (code/tags).
Les icônes de compétences proviennent du CDN **Simple Icons** (slug défini par skill dans l'admin).

## 🎨 CSS Tailwind

Le CSS est compilé par le **CLI Tailwind v3** depuis `static/css/src.css` vers
`static/css/main.css` (déjà inclus). Après toute modification des templates :

```bash
npm run build:css
```

## 🗄️ Contenu

Tout le contenu (projets, compétences, services, expériences, témoignages, FAQ, stats) est
géré via l'**admin Django**. La commande `python manage.py seed` injecte les données réelles
de départ (idempotent ; `--fresh` pour réinitialiser). Les visuels de projets s'uploadent
depuis l'admin (un visuel de repli dégradé s'affiche en l'absence d'image).

---

## 📦 Production

```bash
# variables d'env via .env (DEBUG=False, SECRET_KEY, ALLOWED_HOSTS, DATABASE_URL...)
npm run build:css
python manage.py migrate
python manage.py collectstatic --noinput   # servi par WhiteNoise (gzip + manifest)
gunicorn augustin_portfolio.wsgi:application --bind 0.0.0.0:8000
```

- **Statiques** : WhiteNoise (`CompressedManifestStaticFilesStorage`).
- **Sécurité** : HSTS, cookies secure, SSL redirect, nosniff activés automatiquement quand
  `DEBUG=False`.
- **SEO** : `sitemap.xml`, `robots.txt`, meta OpenGraph/Twitter et JSON-LD `Person` par page.

## ✍️ Blog

Articles gérés dans l'admin (`Blog › Posts`). Le contenu est du **HTML** (rendu stylé via la
classe `.article-prose`). Catégories filtrables, article « à la une » (`is_featured`), pagination,
articles liés et sitemap automatiques. 5 articles de démo sont injectés par `seed`.

## 📄 CV dynamique

La page **`/cv/`** est générée depuis les modèles (`About`, `Experience`, `Education`,
`Certification`, `Language`, `Skill`) : mise en page imprimable (bouton **Imprimer / PDF**) +
**téléchargement du PDF** réel.

La **photo** (`maphoto.png`) et le **CV PDF** (`CV-DEV2025.pdf`) sont versionnés à la racine du
dépôt. `python manage.py seed` les (re)génère automatiquement dans `media/about/` (photo optimisée
en JPEG 640px) et les rattache au modèle `About` — donc rien à uploader sur un nouveau déploiement,
il suffit de lancer `seed`.

## ✅ À personnaliser

- **Photo + CV** : remplace `maphoto.png` / `CV-DEV2025.pdf` à la racine puis relance `seed`,
  ou upload direct dans l'admin → *À propos* (`photo`, `resume`). Sans photo, un avatar « IA »
  s'affiche.
- **Mission / approche / intro** : admin → *À propos* (ou `seed.py`).
- Email / WhatsApp / LinkedIn → `core/context_processors.py` (`site_info`).
- Icônes de skills : champ `icon` (slug Simple Icons) par compétence dans l'admin.
- Visuels projets / couvertures d'articles / avatars témoignages → admin.
