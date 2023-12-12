####  setup environment variables outside docker system

create `setup-env.sh` script in the poject root.

in development
# ---------- [ setup-env.sh ] ----------
#!/usr/bin/env bash

set -a
source ./env_vars/dev/.env
set +a
# ---------- [ setup-env.sh ] ----------

in production
# ---------- [ setup-env.sh ] ----------
#!/usr/bin/env bash

set -a
source ./env_vars/prod/.env
set +a
# ---------- [ setup-env.sh ] ----------

then run script with `./setup-env.sh`


#### folder structure for seting up environment variables

env_vars/
    |- dev/  ## for development
        |- .db
        |- .env
    |- prod/ ## for production
        |- .db
        |- .env


# ---------- [ .env ] ----------
SECRET_KEY=""
DEBUG=True

ALLOWED_HOSTS=*

DB_NAME="dev_db"
DB_USER="admin"
DB_PASSWORD="psw12345"
DB_PORT=5432
DB_HOST=db

REDIS_HOST=redis
REDIS_PORT=6379

SETTINGS=config.settings.dev

SERVER_DOMAIN='127.0.0.1:8000'
CSRF_COOKIE_DOMAIN='127.0.0.1:8000'

EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=''
EMAIL_HOST_PASSWORD=''
RECIPIENT_ADDRESS=''

ESKIZ_EMAIL=''
ESKIZ_PASSWORD=''

SERVER_DOMAIN='tinder-backend.elearn.uz'

PROFILE_IMAGE_LIMIT=''

GOOGLE_APPLICATION_CREDENTIALS='<file_name>.json'
# ---------- [ .env ] ----------


# ---------- [ .db ] -----------
POSTGRES_USER=admin
POSTGRES_PASSWORD=psw12345
POSTGRES_DB=dev_db
# ---------- [ .db ] -----------


in staging mode
# ---------- [ .staging.proxy-companion ] -----------
DEFAULT_EMAIL=youremail@yourdomain.com
ACME_CA_URI=https://acme-staging-v02.api.letsencrypt.org/directory
NGINX_PROXY_CONTAINER=nginx-proxy
# ---------- [ .staging.proxy-companion ] -----------


in production mode
# ---------- [ .proxy-companion ] -----------
DEFAULT_EMAIL=youremail@yourdomain.co
NGINX_PROXY_CONTAINER=nginx-proxy
# ---------- [ .proxy-companion ] -----------