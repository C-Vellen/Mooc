from .models import modelClass


# liste des champs ForeignKey par model, afin de transformer l'id provisoire de la foreign key en instance : 
foreignKeyFields = { model.__name__ .lower(): [
   field.name for field in model._meta.get_fields() if field.__class__.__name__ in["ForeignKey", "OneToOneField"] #and field.name in modelClass.keys()
   ] for model in modelClass.values() }

# liste des champs booléens par model, afin de transformer les valeurs (checkbox.checked) 'on' et '' de request.POST en True et False :
booleanFields = { model.__name__ .lower(): [
    field.name for field in model._meta.get_fields() if field.__class__.__name__ == "BooleanField"
    ] for model in modelClass.values() }

# liste des champs manytomany par model, afin de récupérer les listes de request.POST  :
manytomanyFields = { model.__name__ .lower(): [
    field.name for field in model._meta.get_fields() if field.__class__.__name__ == "ManyToManyField"
    ] for model in modelClass.values() }

# liste des champs fichiers (image, file) par model, afin de récupérer les infos dans le request.FILES
fileImgFields = { model.__name__ .lower(): [
    field.name for field in model._meta.get_fields() if field.__class__.__name__ in["ImageField", "FileField"]
    ] for model in modelClass.values() }



def parse_post(req_post, req_files):
    """
    analyse et décompose les dictionnaire request.POST et request.FILES :
        request.POST = {
            "{a}-{m}-{i}-{f}" : "{v}",
        } 
        où : 
            a = action (create, update, delete)
            m = model (category, tutorial, page, content, listitem, question, proposition)
            i = id de l'objet
            f = champ (ex : titre, texte, image, restriction...)
            v = valeur du champ
    est décomposé en :
        res_post = { 
            'create' : {'tutorial':{'id':{'titre':'Le titre', 'category':'2', 'restriction':['1', '2'], ...}},
                        'page':{'id':{'tuto':'id', ...}, 'id':{...}},
                        ...},
            'update': {'tutorial':{'id':{'titre':'Autre titre', ...}},
                        'page':{'id':{'tuto':'id', ...}, 'id':{...}},
                        ...},
            'delete': { ... },
        }
    idem pour request.FILES décomposé en res_files avec les fileFields / imageFields }
    """
    actions = ["create", "update", "delete"]
    
    print("#"*20)
    print(req_post)
    print("#"*20)


    # initialisation des dictionnaires :
    res_post = { a:{m:dict() for m in modelClass} for a in actions }
    res_files = { a:{m:dict() for m in modelClass} for a in actions }
    

    # remlissage dictionnaires res_post à partir de request.POST
    for k, v in req_post.items():
        print(".....", k, "   :   ", v)
        try : 
            a, m, i, f = k.split('-')
            if f in booleanFields[m]:
                v = (v == 'on')
            if f in fileImgFields[m]:
                raise ValueError
            if f in manytomanyFields[m]:
                v = req_post.getlist(k)
                print("     > v= ", v)
            res_post[a][m][i].update({f:v})
        except KeyError:
            res_post[a][m].update({i:{f:v}})
        except ValueError:
            pass

    # remlissage dictionnaire res_files à partir de request.FILES pour les chmaps spécifiques file/image (FileField et ImageField)
    for k, vf in req_files.items():
        try :
            a, m, i, f = k.split('-')
            res_files[a][m][i].update({f:vf})
        except KeyError:
            res_files[a][m].update({i:{f:vf}})
        except ValueError:
            pass

    return res_post, res_files


def debugPrint(res_post, res_files):
    """ Impression dans le terminal des dictionnaires res_POST et res_FILES avec mise en forme lisible """
    print()
    print('>'*10, "Dictionnaire res_post :", '<'*10)
    print(res_post)
    for a, u in res_post.items():
        print("_"*20)
        print(a, " :")
        for m,v in u.items():
            for i, w in v.items():
                for f,value in w.items():
                    print(f'{a:-<10} {m:-<15} {i:-<5} {f:-<15} : {value.__str__()[:20]}')
    print("-"*40)
    print()
    print('>'*10, "Dictionnaire res_files :", '<'*10)
    for a, u in res_files.items():
        print("_"*20)
        print(a, " :")
        for m,v in u.items():
            for i, w in v.items():
                for f,value in w.items():
                    print(f'{a:-<10} {m:-<15} {i:-<5} {f:-<15} : {type(value)}')
    print("-"*40)
    print()


