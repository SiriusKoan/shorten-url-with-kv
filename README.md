# Shorten URL with KV
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)  
A URL shortener made with Cloudflare KV and Flask.

## deploy
You should set
```
FLASK_ENV="PRODUCTION"
FLASK_APP="manage.py"
EMAIL=<YOUR CLOUDFLARE EMAIL>
KV_ACCOUNT_IDENTIFIER=<YOUR KV ACCOUNT IDENTIFIER>
KV_NAMESPACE_IDENTIFIER=<YOUR KV NAMESPACE IDENTIFIER>
X_AUTH_KEY=<YOUR CLOUDFLARE X-AUTH-KEY>
```
and then run `flask run` or use gunicorn