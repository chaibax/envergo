from django.conf import settings


def settings_context(_request):
    """Settings available by default to the templates context."""
    # Note: we intentionally do NOT expose the entire settings
    # to prevent accidental leaking of sensitive information
    return {
        "DEBUG": settings.DEBUG,
        "ANALYTICS": settings.ANALYTICS,
        "SENTRY_DSN": settings.SENTRY_DSN,
        "ENV_NAME": settings.ENV_NAME,
        "CRISP_CHATBOX_ENABLED": settings.CRISP_CHATBOX_ENABLED,
        "CRISP_WEBSITE_ID": settings.CRISP_WEBSITE_ID,
    }
