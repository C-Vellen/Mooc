// Voir : https://bevacqua.github.io/dragula/
import dragula from 'dragula'

const form = document.querySelector('form')
const elms = document.getElementById('elms')

let count = 0 // compteur pour identifier les nouvelles instances

// affiche le contenu dans le bon format selon la sélection (titre, sous-titre, paragraphe, image,...)
document.querySelectorAll('[data-elm-add="content"]').forEach(contentLineFormat)


// ! les fonctions displayAlertBox et hideAlertBox devraient être importées de js/alertbox.js !
import { displayAlertBox, hideAlertBox } from '../js/alertbox.js'

function add_access(access_id) {
  form.querySelector(`#list-${access_id}`).classList.remove("hidden")
  form.querySelector(".access-choice").querySelector(`#${access_id}`).querySelector("p").classList.add("access-select")
  form.querySelector(".access-choice").querySelector(`#${access_id}`).querySelector("p").classList.remove("access-noselect")
  if (access_id != "for-all") {
    const opt = form.querySelector(`#option-${access_id}`)
    opt.selected = true
  }
}
function remove_access(access_id) {
  form.querySelector(`#list-${access_id}`).classList.add("hidden")
  form.querySelector(".access-choice").querySelector(`#${access_id}`).querySelector("p").classList.add("access-noselect")
  form.querySelector(".access-choice").querySelector(`#${access_id}`).querySelector("p").classList.remove("access-select")
  if (access_id != "for-all") {
    const opt = form.querySelector(`#option-${access_id}`)
    opt.selected = false
  }
}
function toggle_access(access_id) {
  const elt = form.querySelector(".access-choice").querySelector(`#${access_id}`)
  form.querySelector(`#list-${access_id}`).classList.toggle("hidden")
  form.querySelector(".access-choice").querySelector(`#${access_id}`).querySelector("p").classList.toggle("access-select")
  form.querySelector(".access-choice").querySelector(`#${access_id}`).querySelector("p").classList.toggle("access-noselect")
  if (access_id != "for-all") {
    const opt = form.querySelector(`#option-${access_id}`)
    opt.selected = (opt.selected) ? false : true
  }
}


function contentLineFormat(contentLine) {
  // pour chaque ligne de contenu, affiche le type de formulaire en fonction du champ sélectionné (titre, paragraphe, liste, image...)
  const selection = contentLine.querySelector('select')
  selectionDisplay(selection.value, contentLine)
  selection.addEventListener('change', e => {
    selectionDisplay(e.target.value, contentLine)
  })
}

function boxToDeleteFormat(el, toDelete) {
  el.querySelectorAll(".redcross").forEach(cross => {
    if (toDelete) { cross.classList.remove("hidden") } else { cross.classList.add("hidden") }
  })
  el.querySelectorAll(".greycross").forEach(cross => {
    if (toDelete) { cross.classList.add("hidden") } else { cross.classList.remove("hidden") }
  })
  el.querySelectorAll("p.headline > span").forEach(text => contentToDeleteFormat(text, toDelete))
  el.querySelectorAll("textarea").forEach(text => contentToDeleteFormat(text, toDelete))
  el.querySelectorAll(".cat-content > *").forEach(text => contentToDeleteFormat(text, toDelete))

}

function contentToDeleteFormat(text, toDelete) {
  text.style.textDecoration = (toDelete) ? "line-through" : ""
  text.style.color = (toDelete) ? "#e7000b" : ""

}

function selectionDisplay(selectValue, contentLine) {
  // permet d'afficher les champs de contenu "contentFields" en fonction de la valeur sélectionnée "selectValue" (titre, paragraphe, image...)
  contentLine.querySelector(".load-image").style.display = (selectValue === 'IM') ? "" : "none" // affichage image    
  contentLine.querySelector(".load-video").style.display = (selectValue === 'VI') ? "" : "none" // affichage video   
  contentLine.querySelector("textarea").style.display = (selectValue === "" | selectValue === "LI") ? "none" : "" // pas d'affichage texte si liste
  contentLine.querySelector("textarea").style.fontWeight = (selectValue === 'TI') ? "bold" : "normal" // titre en gras
  contentLine.querySelector("textarea").style.height = (selectValue === 'PA') ? "100px" : "35px" // paragraphe sur 4 lignes
  contentLine.querySelector(".list").style.display = (selectValue === "LI") ? "" : "none" // affichage liste
  contentLine.querySelector("textarea").placeholder = (selectValue === 'IM') ? "Légende de l'image ..." : "Ecrivez votre texte ..." // affichage placeholder    
  contentLine.querySelector("textarea").placeholder = (selectValue === 'VI') ? "Légende de la video ..." : "Ecrivez votre texte ..." // affichage placeholder    
}

function imagePreview(e) {
  // affichage de l'image dès qu'elle est sélectionnée dans le browser, avant son téléchargement
  console.log("> imagePreview")
  e.target.parentNode.parentNode.querySelectorAll(".img-preview").forEach(output => {
    if (output && e.target.files) {
      output.src = URL.createObjectURL(e.target.files[0])
      output.onload = function () {
        URL.revokeObjectURL(output.src)
      }
    }
  })
}

function videoPreview(e) {
  // affichage de la video dès qu'elle est sélectionnée dans le browser, avant son téléchargement
  const output = e.target.parentNode.querySelector("video")
  if (output && e.target.files) {
    output.src = URL.createObjectURL(e.target.files[0])
    output.onload = function () {
      URL.revokeObjectURL(output.src)
    }
  }
}

function testDuplicatedCategory(e) {
  // fonction qui évite de valider 2 catégories avec le même nom, ce qui générerait une erreur 500 :
  // - doublon passe en rouge dans le formulaire
  // - validation rejetée à la soumission
  const submitButton = form.querySelector(".catSubmit")
  let preventValidation = false
  for (const lineCat of form.querySelectorAll("[data-elm-add]")) {
    const inputCat = lineCat.querySelector(".cat-form")
    const catNameList = Array.from(form.querySelectorAll(".cat-form")).filter(c => c != inputCat).map(c => c.value).filter(v => v != '')
    const doublon = catNameList.includes(inputCat.value)
    const willBeDeleted = (lineCat.querySelector(".remove input").checked || ((e.target.classList.contains("remove") && e.type) == "pointerenter"))
    inputCat.style.color = (doublon || willBeDeleted) ? "#e7000b" : ""

    preventValidation = preventValidation | doublon
    inputCat.disabled = (willBeDeleted) ? true : false
  }
  submitButton.disabled = (preventValidation) ? true : false
  submitButton.style.backgroundColor = (preventValidation) ? "#aaa" : ""
  form.querySelector(".messageDoublon").classList.toggle("hidden", !preventValidation)
}

function rescaleImage(e) {
  // modifie l'échelle d'une image quand on actionne le slider et affiche la valeur en %
  e.target.closest("div").querySelector(".scale-display").innerText = e.target.value + "%"
  e.target.closest(".load-image").querySelector(".relative").style.width = e.target.value + "%"
}

// pour rescaler une image en actionnant le slider ;
const range = document.querySelectorAll(".load-image > .scale > [type='range']")
range.forEach(r => r.addEventListener("input", rescaleImage))



form.addEventListener('click', e => {

  // menu déroulant pour le choix des catégories (formulaire dans vignette_tuto.html)
  if (e.target.classList.contains('change-category')) {
    // fold_unfold category
    form.querySelector(".change-category").classList.toggle("rotate-180")
    form.querySelector(".category-choice").classList.toggle("hidden")
    // fold access
    form.querySelector(".change-access").classList.add("rotate-180")
    form.querySelector(".access-choice").classList.add("hidden")
  }

  // choix des catégories dans (champ Tutorial.category, formulaire dans vignette_tuto.html)
  if (e.target.classList.contains('category-choice')) {
    // recherche de l'id de la catégorie concernée
    const cat_id = e.target.closest("li").id
    // réinitialisation du choix des catégorie (on déselectionne tout)
    form.querySelector(".category-list").querySelectorAll("span").forEach(elt => {
      elt.classList.add("hidden")
    })
    form.querySelector(".category-choice").querySelectorAll("p").forEach(elt => {
      elt.classList.remove("font-bold")
      elt.classList.remove("bg-slate-200")
    })
    form.querySelector(".category-option").querySelectorAll("option").forEach(elt => {
      elt.selected = false
    })
    // sélection de la nouvelle catégorie choisie
    form.querySelector(`#list-${cat_id}`).classList.remove("hidden")
    form.querySelector(".category-choice").querySelector(`#${cat_id}`).querySelector("p").classList.add("font-bold")
    form.querySelector(".category-choice").querySelector(`#${cat_id}`).querySelector("p").classList.add("bg-slate-200")
    const opt = form.querySelector(`#option-${cat_id}`)
    opt.selected = true
    // fold category
    form.querySelector(".change-category").classList.add("rotate-180")
    form.querySelector(".category-choice").classList.add("hidden")

  }


  // menu déroulant pour le choix des accès dans (champ Tutorial.restriction, formulaire dans vignette_tuto.html)
  if (e.target.classList.contains('change-access')) {
    // fold_unfold access
    form.querySelector(".change-access").classList.toggle("rotate-180")
    form.querySelector(".access-choice").classList.toggle("hidden")
    // fold category
    form.querySelector(".change-category").classList.add("rotate-180")
    form.querySelector(".category-choice").classList.add("hidden")

  }

  // choix des accès dans (champ Tutorial.restriction, formulaire dans vignette_tuto.html)
  if (e.target.classList.contains('restriction-choice')) {
    // recherche de l'id de la restriction d'accès concernée
    const access_id = e.target.closest("li").id
    if (access_id == "for-all") {
      // si on clique sur "Tout public" : déactivation de toutes les restrictions
      form.querySelector(".access-choice").querySelectorAll("li").forEach(elt => remove_access(elt.id))
      add_access(access_id)
    } else {
      // si on ne clique pas sur "Tout public", activation ou désactivation de la restriction
      toggle_access(access_id)
      // si toutes les restrictions sont désactivées, on s'assure que "Tout public" apparait bien :
      const opt_list = form.querySelector(".access-option").querySelectorAll("option")
      if (Array.from(opt_list).map(elt => elt.selected).every(val => !val)) {
        add_access("for-all")
      } else {
        remove_access("for-all")
      }
    }
  }

  // repliement / dépliement des contenus :
  if (e.target.classList.contains('fold')) {
    e.target.closest('[data-elm-add]').querySelectorAll(":scope > *").forEach(child => {
      if (child.contains(e.target)) {
        // child.querySelectorAll(".fold").forEach( f => f.style.display = (f.style.display == "none") ? "": "none")
        child.querySelectorAll(".fold").forEach(f => f.classList.toggle("rotate-180"))
        child.querySelectorAll(".headline").forEach(f => {
          f.style.display = (f.style.display == "none") ? "" : "none"
          const select = f.closest('[data-elm-add]').querySelector("select")
          const option = select.options[select.selectedIndex].text
          // type de contenu sélectionné (Titre, Liste, Image, Question, Réponse...)
          const em = f.closest('[data-elm-add]').querySelector("p.headline > em")
          // contenu (saisi dans textarea)
          const span = f.closest('[data-elm-add]').querySelector("p.headline > span")
          if (option == "Liste") {
            em.innerText = option
            span.textContent = "- " + f.closest('[data-elm-add]').querySelector(".list textarea").value + "..."
          } else {
            em.innerText = option
            span.textContent = f.closest('[data-elm-add]').querySelector("textarea").value
          }
          if (option == "Titre") { span.classList.add("font-bold") } else { span.classList.remove("font-bold") }
        })
      } else {
        child.style.display = (child.style.display == "none") ? "" : "none"
      }
    })
  }

  // modification des catégories :
  if (e.target.classList.contains('cat-change')) {
    const catName = e.target.closest('[data-elm-add]').querySelector(".cat-content")
    catName.querySelector("span").style.display = (catName.querySelector("span").style.display == "inline") ? "none" : "inline"
    catName.querySelector("input").style.display = (catName.querySelector("input").style.display == "inline") ? "none" : "inline"

    const inputCat = catName.querySelector("input")
    inputCat.value = catName.querySelector("span").innerHTML
    testDuplicatedCategory(e)
    inputCat.addEventListener("input", testDuplicatedCategory)
  }

  // suppression d'un élément existant
  if (e.target.classList.contains('removecross')) {

    // test pour savoir si le bloc à supprimer fait partie d'un bloc déjà coché pour la suppression :
    let bloc = e.target.closest('[data-elm-add]')
    let box = bloc.querySelector(".remove > input")

    if (bloc.parentNode.closest('[data-elm-add]') == null || !bloc.parentNode.closest('[data-elm-add]').querySelector(".remove > input").checked) {
      box.checked = !box.checked
      e.target.closest('[data-elm-add]').querySelectorAll(".remove > input").forEach(b => { b.checked = box.checked; })
      boxToDeleteFormat(e.target.closest('[data-elm-add]'), box.checked)
    }
    if (bloc.dataset.elmAdd == "category") {
      testDuplicatedCategory(e)
    }
  }

  // création d'un nouveau contenu:
  if (e.target.classList.contains('add-elms')) {
    e.preventDefault()
    e.stopPropagation()
    let ou = e.target.closest('[data-elm-add]')
    if (ou) {
      ou = ou.querySelector(e.target.dataset.ou)
    }
    if (!ou) {
      ou = document.querySelector(e.target.dataset.ou)
    }
    const elm = elms.
      querySelector('[data-elm-add=' + e.target.dataset.elm + ']').
      cloneNode(50)
    // dragList = list des éléments dragables qui sont sous un élément nouvellement créé 
    // exemple : pour une page créée : draglist = [ [data-ou=content], [data-ou=question] ] 
    const draglist = elm.querySelectorAll('[data-ou]')
    draglist.forEach((drag) => {
      if (drag) {
        dragula([elm.querySelector(drag.dataset.ou)], {
          moves: function (el, container, handle) {
            return handle.classList.contains('handle') && handle.closest('[data-elm-add]').parentNode == container
          }
        })
      }
    })

    // ajout d'une ligne de formulaire
    ou.append(elm)
    // attribution des input "name" pour identification des clés du request.POST:
    elm.querySelectorAll('input, textarea, select').forEach(i => {
      i.name = i.name.replace("xx", `${count}`)
    })

    // documentation de la foreign key :
    if (elm.querySelector('.fk')) {
      elm.querySelector('.fk').value = elm.closest('[class^="add-"], [class*=" add-"]').id
    }

    // nouveau parent : marquage de l'id dans la div parent, pour qu'il 
    // soit récupérable par les futurs enfants (foreign key)
    elm.querySelectorAll('[class^="add-"], [class*=" add-"]').forEach(par => {
      par.id = par.id.replace("xx", `${count}`)
    })
    count++

    // modification des images en cliquant sur le crayon + preview avant téléchargement
    if (elm.querySelector('.load-image')) {
      // attribution des for et id pour apairage entre le label (crayon cliquable) et l'input-image correspondante
      elm.querySelector('.load-image > div > label').htmlFor = elm.querySelector('.load-image > div > label').htmlFor.replace("xx", `${count}`)
      elm.querySelector('.load-image > div > input').id = elm.querySelector('.load-image > div > input').id.replace("xx", `${count}`)
      count++
      // preview des nouvelles images avant téléchargement :
      elm.querySelector('.load-image > div > input').addEventListener("change", imagePreview)
      // modification de l'échelle de l'image :
      elm.querySelector(".load-image > .scale > [type='range']").addEventListener("input", rescaleImage)
    }

    // modification des videos en cliquant sur le crayon + preview avant téléchargement
    if (elm.querySelector('.load-video')) {
      // attribution des for et id pour apairage entre le label (crayon cliquable) et l'input-video correspondante
      elm.querySelector('.load-video > label').htmlFor = elm.querySelector('.load-video > label').htmlFor.replace("xx", `${count}`)
      elm.querySelector('.load-video > input').id = elm.querySelector('.load-video > input').id.replace("xx", `${count}`)
      count++
      // preview des nouvelles videos avant téléchargement :
      elm.querySelector('.load-video > input').addEventListener("change", videoPreview)
    }

    // mise en forme de la ligne de contenu en fonction de la sélection du type de contenu:
    if (elm.dataset.elmAdd == "content") {
      contentLineFormat(elm)
    }

    // nouveaux elm à supprimer (croix grise/rouge) : mise en rouge, biffage
    elm.querySelector('.remove').addEventListener('pointerenter', e => {
      e.preventDefault()
      e.stopPropagation()
      boxToDeleteFormat(elm, true)
      if (elm.classList.contains("add-cat")) {
        testDuplicatedCategory(e)
      }
    })
    elm.querySelector('.remove').addEventListener('pointerleave', e => {
      e.preventDefault()
      e.stopPropagation()
      boxToDeleteFormat(elm, false)
      if (elm.classList.contains("add-cat")) {
        testDuplicatedCategory(e)
      }
    })
    // nouveaux elm à supprimer (croix grise/rouge) : confirmation (popup) et suppression
    elm.querySelector('.remove').addEventListener('click', e => {
      e.preventDefault()
      e.stopPropagation()
      // ---------------------------------------------------
      const elmHasNoData = Array.from(elm.querySelectorAll('textarea')).every((x) => x.value === "")
      if (elmHasNoData) {
        elm.remove()
      } else {
        displayAlertBox("alert-delete")
        document.querySelector(".remove-confirm").addEventListener('click', e => {
          elm.remove()
          hideAlertBox(e)
        })
      }
      if (elm.classList.contains("add-cat")) {
        testDuplicatedCategory(e)
      }
    })
    // si nouvelle catégorie : vérifier que son nom n'est pas déjà pris
    if (elm.classList.contains("add-cat")) {
      const inputCat = elm.querySelector(".cat-content input")
      inputCat.addEventListener("input", testDuplicatedCategory)
    }
  }
});

// Initialisation des éléments draguables
let listou = []
document.querySelectorAll('form [data-ou]').forEach(elm => {
  listou.push(elm.dataset.ou)
})
listou
  .filter((value, index, array) => array.indexOf(value) === index)  // uniq
  .forEach(ou => {
    document.querySelectorAll(ou).forEach(a => {
      dragula([a], {
        moves: function (el, container, handle) {
          return handle.classList.contains('handle') && handle.closest('[data-elm-add]').parentNode == container
        }
      })
    })
  })

// Gestion dynamique de la numérotation des pages et contenus
form.addEventListener('click', e => {
  form.querySelectorAll('[class^="add-"], [class*=" add-"]').forEach(elmAdd => {
    let number = 1
    elmAdd.querySelectorAll(":scope > [data-elm-add]").forEach(elm => {
      if (!elm.querySelector(".remove > input").checked) {
        elm.querySelector("input.position").value = number++
      }
    })
  })
})

// preview des images avant téléchargement :
document.querySelectorAll('.load-image > div > input').forEach(el => {
  addEventListener("change", imagePreview)
})

// -------------------------------
// preview des videos avant téléchargement :
document.querySelectorAll('.load-video > input').forEach(el => {
  addEventListener("change", videoPreview)

})






