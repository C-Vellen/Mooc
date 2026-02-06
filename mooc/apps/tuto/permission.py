
from django.shortcuts import redirect, get_object_or_404
from user.models import Restriction
from progress.context import progresscontext

from .models import CONTENTTYPE, Category, TutoBase, Tutorial



# valeurs des boutons de redirection après création ou mise à jour tuto :
nextValue = {
    "cont": "Enregistrer et continuer les modifications",
    "visu": "Enregistrer et visualiser le tutoriel",
    "back": "Enregistrer et retourner à mon compte",
    "canc": "Annuler les modifications",
    "create": "Créer et ajouter des pages",
    "createback": "Créer et revenir au menu",
    "createcanc": "Annuler et revenir au menu",
}


def permission_check(view):
    """ decorator : management of permission and context for views"""
    def wrapper(request, *args, **kwargs):
               
        role = kwargs.get("role", request.session.get("role"))
        if "tuto_slug" in kwargs:
            tuto = get_object_or_404(Tutorial, slug=kwargs.get("tuto_slug"))
        context = kwargs.get("context", dict())
        
        
        # context
        context.update(progresscontext(request))
        context.update({
            "categories": Category.objects.all().order_by("position"),
            "role": role,
        })
        context.update(nextValue)
           
        match view.__name__:
            case "admin":
                
                if not((role == "auteur" and request.user.is_author) or (role == "gestionnaire" and request.user.is_gestionnaire)):
                    return redirect("user:nonautorise")
                request.session['role'] = role
                context.update(
                    {
                        "titre_onglet": f"Mon compte {{role}}",
                        "tuto_form": False,
                        "tuto_header": "admin",
                        "role": role,
                    }
                )
                if role == "auteur":
                    context.update(
                        {
                            "tutobases": [
                            tb for tb in TutoBase.objects.all() if tb.has_author(request.user)
                            ],
                            "author_link": False,
                            "gestionnaire_link": request.user.is_gestionnaire,
                        }
                    )
                elif role == "gestionnaire":
                    context.update(
                        {
                            "tutobases": TutoBase.objects.all(),
                            "author_link": request.user.is_author,
                            "gestionnaire_link": False,
                        }
                    )
                kwargs.update({"context":context})          

            
            case "read_tuto":
                tuto_slug = kwargs.get("tuto_slug")
                page = kwargs.get("page")
                context.update({"role": role})
                kwargs = {
                    "tuto_slug":tuto_slug,
                    "page": page,
                    "role": ''
                    }
                
                
            
            case "create_tuto":
                # permissions                
                if not (request.user.is_author):
                    return redirect("user:nonautorise")
                context.update(
                    {
                        "titre_onglet": "Nouveau tutoriel",
                        "username": request.user.username,
                        "tuto_restrictions": Restriction.objects.none(),
                        "tuto_form": True,
                        "tuto_header": "create",
                    }
                )
                kwargs.update({"context":context})          
            
            case "update_tuto":
                """ 
                update authorized to:
                - the tutorial author
                - the gestionnaire (only if tutorial is submitted)
                """
                # permissions                
                if not (((tuto.in_progress or tuto.rejected) and request.user in tuto.author.all()) or (tuto.submitted and request.user.is_gestionnaire)):
                    return redirect("user:nonautorise")
                
                # context
                context.update(progresscontext(request))
                context.update({
                    "titre_onglet": tuto.thumbnail,
                    "tuto": tuto,
                    "tuto_restrictions": tuto.restriction.all(),
                    "tuto_form": True,
                    "tuto_header": "update",
                    "CONTENTTYPES": CONTENTTYPE,
                })
                kwargs.update({"context":context})
                                                 
            case "delete_tuto":
                if not ((tuto.in_progress and request.user in tuto.author.all()) or ((not tuto.published and tuto.archived) and request.user.is_gestionnaire)):
                    return redirect("user:nonautorise")
            
            case "submit_tuto":
                if not ((tuto.in_progress and tuto.get_all_pages) and request.user in tuto.author.all()) :
                    return redirect("user:nonautorise")
           
            case "reject_tuto":
                if not (tuto.submitted and request.user.is_gestionnaire):
                    return redirect("user:nonautorise")
        
            case "publish_tuto":
                if not ((tuto.submitted or tuto.rejected or (not tuto.published and tuto.archived)) and request.user.is_gestionnaire):
                    return redirect("user:nonautorise")
                
            case "archive_tuto":
                if not ((tuto.published and not tuto.archived) and request.user.is_gestionnaire):
                    return redirect("user:nonautorise")
                
            case "dearchive_tuto":
                if not ((tuto.published and tuto.archived) and request.user.is_gestionnaire):
                    return redirect("user:nonautorise")
                
            case "depublish_tuto":
                if not ((tuto.published and tuto.archived) and request.user.is_gestionnaire):
                    return redirect("user:nonautorise")
   
            case "duplicate_tuto":
                if not ((tuto.published or tuto.archived) and request.user in tuto.author.all()):
                    return redirect("user:nonautorise")
   
        
        return view(request, *args, **kwargs)       
        
        
    return wrapper


                
                
           
        
            
            