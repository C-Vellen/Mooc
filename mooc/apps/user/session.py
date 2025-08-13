from datetime import datetime
from django.contrib.sessions.models import Session


def show_sessions():
    """Affiche les sessions stockées en bd"""
    print("\n******** LISTE DES SESSIONS ENREGISTREES EN BD : *************")
    print("Fields:")
    fieldList = Session._meta.get_fields()
    print(fieldList)

    print(f"{"session_key":<15}{"session_data":<15}{"expire_date":<15}")
    for s in Session.objects.all().order_by("expire_date"):
        print(
            f"{s.session_key[:8]:<15}{s.session_data[-10:]:<15}{s.expire_date.strftime('%d/%m/%y-%H:%M:%S"')}"
        )

    print("*********************************", end="\n\n")


def show_request(request: dict):
    """Affiche le dictionnaire de la session en cours

    Args:
        session (_type_): _dict
    """
    print("******** REQUEST : *************")

    if request.user:
        print("=> request.user:", request.user)

    if request.session:
        s = request.session
        print("=> request.session :")
        try:
            print(f"\t{'session_key':<15} : {s.session_key[:8]:<15}")
        except TypeError:
            print("\tSESSION EXPIREE: IMPOSSIBLE DE RECUPERER LA SESSION")
        for k, v in request.session.items():
            print(f"\t{k:<15} : {v}")

    print("=> session stockée en bd dans l'objet Session:")
    try:
        s = Session.objects.get(session_key=request.session.session_key)
        print(f"\t{"session_key":<15}{"session_data":<15}{"expire_date":<15}")
        print(
            f"\t{s.session_key[:8]:<15}{s.session_data[-10:]:<15}{s.expire_date.strftime('%d/%m/%y-%H:%M:%S"')}"
        )
    except Session.DoesNotExist:
        print("\tSESSION EXPIREE: IMPOSSIBLE DE RECUPERER LA SESSION")

    print("*********************************")
