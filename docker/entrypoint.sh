#!/usr/bin/env bash
# Entrypoint de production : migrations + statiques, puis lancement de la commande.
set -e

echo "→ Migrations de la base de données..."
python manage.py migrate --noinput

echo "→ Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Seed optionnel au démarrage (mettre SEED_ON_START=true dans .env pour la 1re mise en ligne)
if [ "${SEED_ON_START:-false}" = "true" ]; then
  echo "→ Seed du contenu initial..."
  python manage.py seed
fi

echo "→ Lancement : $*"
exec "$@"
