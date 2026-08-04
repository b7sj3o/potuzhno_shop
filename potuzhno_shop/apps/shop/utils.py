from django.contrib import messages


def form_errors_to_messages(request, form):
    for field, errors in form.errors.items():
        prefix = "" if field == "__all__" else f"{form.fields[field].label}: "

        for error in errors:
            messages.error(request, f"{prefix}{error}")
