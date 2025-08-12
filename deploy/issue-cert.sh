#!/bin/sh
# Issue Let's Encrypt certificate (run once, after DNS points to YOUR_DOMAIN)
DOMAIN=$1
EMAIL=$2
if [ -z "$DOMAIN" ] || [ -z "$EMAIL" ]; then
  echo "Usage: ./issue-cert.sh your-domain.com admin@your-domain.com"
  exit 1
fi

docker compose up -d nginx
docker run --rm -v certbot-webroot:/var/www/certbot -v letsencrypt:/etc/letsencrypt certbot/certbot certonly --webroot -w /var/www/certbot -d $DOMAIN --email $EMAIL --agree-tos --non-interactive
# After success, replace nginx config with SSL version
cp deploy/nginx/conf.d/app-ssl.conf deploy/nginx/conf.d/default.conf
sed -i "s/YOUR_DOMAIN/$DOMAIN/g" deploy/nginx/conf.d/default.conf
docker compose restart nginx