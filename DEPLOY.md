# Déploiement — augustinidohou.site

Stack de prod : **Docker Compose** (web Gunicorn + PostgreSQL) derrière le **Nginx de l'hôte**
(reverse-proxy + TLS Let's Encrypt). Gunicorn écoute sur `127.0.0.1:8001`.

Pré-requis (déjà en place chez toi) : accès SSH+sudo, DNS de `augustinidohou.site` et
`www.augustinidohou.site` pointant vers l'IP du serveur, Docker + Docker Compose, Nginx + Certbot.

> Les commandes ci-dessous supposent le projet dans `/opt/augustinidohou`. Adapte si tu utilises
> un autre chemin (et la même valeur dans `deploy/nginx/augustinidohou.site.conf`).

---

## 1. Récupérer le code

```bash
sudo mkdir -p /opt/augustinidohou && sudo chown $USER:$USER /opt/augustinidohou
git clone https://github.com/asidev7/blog_augustinidohou.git /opt/augustinidohou
cd /opt/augustinidohou
```

## 2. Configurer l'environnement

```bash
cp deploy/env.production.example .env
# Génère une clé secrète :
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
nano .env   # colle SECRET_KEY, choisis POSTGRES_PASSWORD et reporte-le dans DATABASE_URL
```

Points à remplir dans `.env` : `SECRET_KEY`, `POSTGRES_PASSWORD` (identique dans `DATABASE_URL`).
Laisse `SEED_ON_START=true` pour la **première** mise en ligne.

## 3. Lancer l'application

```bash
docker compose up -d --build
docker compose logs -f web      # vérifier migrate + collectstatic + gunicorn (Ctrl-C pour quitter)
```

Au premier démarrage, l'app applique les migrations, collecte les statiques et (si
`SEED_ON_START=true`) injecte le contenu (projets, skills, blog, CV, photo, PDF).

Crée ton compte admin :

```bash
docker compose exec web python manage.py createsuperuser
```

Test rapide en local sur le serveur :

```bash
curl -I http://127.0.0.1:8001/        # doit répondre 200/301
```

> Ensuite, repasse `SEED_ON_START=false` dans `.env` (pour ne pas re-seeder à chaque redéploiement).

## 4. Nginx (hôte) + HTTPS

```bash
sudo cp deploy/nginx/augustinidohou.site.conf /etc/nginx/sites-available/augustinidohou.site
sudo ln -s /etc/nginx/sites-available/augustinidohou.site /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Certificat TLS (Certbot modifie le vhost pour ajouter le 443 + la redirection) :
sudo certbot --nginx -d augustinidohou.site -d www.augustinidohou.site
```

Le site est en ligne sur **https://augustinidohou.site** 🎉

---

## Mises à jour (redéploiement)

```bash
cd /opt/augustinidohou
git pull
docker compose up -d --build      # migrate + collectstatic relancés automatiquement
```

## Sauvegardes

```bash
# Base de données
docker compose exec -T db pg_dump -U augustin augustinidohou > backup-$(date +%F).sql
# Médias (uploads admin)
tar czf media-$(date +%F).tar.gz media/
```

## Commandes utiles

```bash
docker compose ps                 # état des conteneurs
docker compose logs -f web        # logs application
docker compose exec web python manage.py seed --fresh   # ré-initialiser le contenu
docker compose down               # arrêter (les données DB restent dans le volume pgdata)
```

## Dépannage

- **502 Bad Gateway** : le conteneur web n'est pas prêt → `docker compose logs web`.
- **Statics/CSS absents** : vérifier que `./staticfiles` est rempli (`ls staticfiles/`) et que le
  chemin `alias` du vhost Nginx pointe bien dessus.
- **403 sur /media/** : Nginx (www-data) doit pouvoir lire `/opt/augustinidohou/media` ; assure-toi
  que `/opt` et les dossiers sont traversables (`chmod o+rx`).
- **CSRF / DisallowedHost** : vérifier `ALLOWED_HOSTS` et `CSRF_TRUSTED_ORIGINS` dans `.env`.
