# Security Notes for advanced_features_and_security

## Settings
- DEBUG should be `False` in production.
- `SECURE_BROWSER_XSS_FILTER`, `X_FRAME_OPTIONS`, `SECURE_CONTENT_TYPE_NOSNIFF` set to protect browsers.
- `CSRF_COOKIE_SECURE` and `SESSION_COOKIE_SECURE` ensure cookies are only sent on HTTPS.

## CSRF Protection
- All forms include `{% csrf_token %}` in templates to guard against CSRF.

## SQL injection / Input validation
- Views use Django ModelForms (`BookForm`) which validate and clean user inputs.
- No raw SQL is used; Django ORM parameterizes queries.

## Content Security Policy
- Minimal CSP header provided by `LibraryProject.middleware.CSPMiddleware`.
- Adjust `CSP_SCRIPT_SRC` / `CSP_STYLE_SRC` in settings to reflect trusted domains.

## Testing
- Use Django admin to create users and assign groups/permissions.
- Test different users for allowed/forbidden actions (403 if not permitted).
