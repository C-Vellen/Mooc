from home.models import Libelles
from mooc.settings import DEBUG


def homecontext(request):
    context = {
        lib.description: lib
        for lib in Libelles.objects.exclude(description__contains="Lien_RS")
    }
    context.update(
        {
            "liensRS": Libelles.objects.filter(
                description__contains="Lien_RS"
            ).order_by("description"),
            "debug": DEBUG,
            "moi": "ok",
        }
    )

    if request.user:
        context.update(
            {
                "user": request.user,
            }
        )

    return context
