```docker-compose build -d --no-cached```
- rebuild the system without any cache entries 
```docker-compose system prune```
- deletes unused images 

`#Create the Volume`

`docker volume create nbvolume`

`#Check for the volumes`

`docker volume` `ls`

`# Inspect the volume` 

`docker volume inspect nbvolume`

`docker volume inspect nbvolume`

```
**`docker system prune -a`** to remove any stopped container. This command deleted all the local docker images related to the dockerfile.


xUU5qwwXjW23wLTPHVdTk4rsPYbs3zwZbnjP33ifyHzRa4WFUV


 WARNINGS:
nautobot_1         | ?: (security.W004) You have not set a value for the SECURE_HSTS_SECONDS setting. If your entire site is served only over SSL, you may want to consider setting a value and enabling HTTP Strict Transport Security. Be sure to read the documentation first; enabling HSTS carelessly can cause serious, irreversible problems.
nautobot_1         | ?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True. Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
nautobot_1         | ?: (security.W009) Your SECRET_KEY has less than 50 characters, less than 5 unique characters, or it's prefixed with 'django-insecure-' indicating that it was generated automatically by Django. Please generate a long and random SECRET_KEY, otherwise many of Django's security-critical features will be vulnerable to attack.
nautobot_1         | ?: (security.W012) SESSION_COOKIE_SECURE is not set to True. Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.
nautobot_1         | ?: (security.W016) You have 'django.middleware.csrf.CsrfViewMiddleware' in your MIDDLEWARE, but you have not set CSRF_COOKIE_SECURE to True. Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.
nautobot_1         | 
nautobot_1         | System check identified 6 issues (0 silenced).
```

