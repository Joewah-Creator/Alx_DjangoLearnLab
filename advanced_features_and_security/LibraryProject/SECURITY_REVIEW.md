# Security Review for Django HTTPS & Secure Redirects

## HTTPS Enforcement
The following settings ensure all traffic is redirected to HTTPS:
- `SECURE_SSL_REDIRECT = True`
- `SECURE_HSTS_SECONDS = 31536000`
- `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
- `SECURE_HSTS_PRELOAD = True`

## Secure Cookies
These settings enforce cookies to be transmitted only over HTTPS:
- `SESSION_COOKIE_SECURE = True`
- `CSRF_COOKIE_SECURE = True`

## Secure Browser Headers
These headers protect against common attacks:
- `X_FRAME_OPTIONS = 'DENY'` (prevents clickjacking)
- `SECURE_CONTENT_TYPE_NOSNIFF = True` (prevents MIME-sniffing)
- `SECURE_BROWSER_XSS_FILTER = True` (activates browser XSS protection)

## Summary
All required HTTPS and secure headers have been configured in `settings.py` according to Django security best practices.
