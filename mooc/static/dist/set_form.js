/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./node_modules/atoa/atoa.js":
/*!***********************************!*\
  !*** ./node_modules/atoa/atoa.js ***!
  \***********************************/
/***/ ((module) => {

module.exports = function atoa (a, n) { return Array.prototype.slice.call(a, n); }


/***/ }),

/***/ "./mooc/static/assets/set_form.js":
/*!****************************************!*\
  !*** ./mooc/static/assets/set_form.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var dragula__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! dragula */ "./node_modules/dragula/dragula.js");
/* harmony import */ var dragula__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(dragula__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _js_alertbox_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../js/alertbox.js */ "./mooc/static/js/alertbox.js");
function _createForOfIteratorHelper(r, e) { var t = "undefined" != typeof Symbol && r[Symbol.iterator] || r["@@iterator"]; if (!t) { if (Array.isArray(r) || (t = _unsupportedIterableToArray(r)) || e && r && "number" == typeof r.length) { t && (r = t); var _n = 0, F = function F() {}; return { s: F, n: function n() { return _n >= r.length ? { done: !0 } : { done: !1, value: r[_n++] }; }, e: function e(r) { throw r; }, f: F }; } throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method."); } var o, a = !0, u = !1; return { s: function s() { t = t.call(r); }, n: function n() { var r = t.next(); return a = r.done, r; }, e: function e(r) { u = !0, o = r; }, f: function f() { try { a || null == t["return"] || t["return"](); } finally { if (u) throw o; } } }; }
function _unsupportedIterableToArray(r, a) { if (r) { if ("string" == typeof r) return _arrayLikeToArray(r, a); var t = {}.toString.call(r).slice(8, -1); return "Object" === t && r.constructor && (t = r.constructor.name), "Map" === t || "Set" === t ? Array.from(r) : "Arguments" === t || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(t) ? _arrayLikeToArray(r, a) : void 0; } }
function _arrayLikeToArray(r, a) { (null == a || a > r.length) && (a = r.length); for (var e = 0, n = Array(a); e < a; e++) n[e] = r[e]; return n; }
// Voir : https://bevacqua.github.io/dragula/

var form = document.querySelector('form');
var elms = document.getElementById('elms');
var count = 0; // compteur pour identifier les nouvelles instances

// affiche le contenu dans le bon format selon la sélection (titre, sous-titre, paragraphe, image,...)
document.querySelectorAll('[data-elm-add="content"]').forEach(contentLineFormat);

// ! les fonctions displayAlertBox et hideAlertBox devraient être importées de js/alertbox.js !

function add_access(access_id) {
  form.querySelector("#list-".concat(access_id)).classList.remove("hidden");
  form.querySelector(".access-choice").querySelector("#".concat(access_id)).querySelector("p").classList.add("access-select");
  form.querySelector(".access-choice").querySelector("#".concat(access_id)).querySelector("p").classList.remove("access-noselect");
  if (access_id != "for-all") {
    var opt = form.querySelector("#option-".concat(access_id));
    opt.selected = true;
  }
}
function remove_access(access_id) {
  form.querySelector("#list-".concat(access_id)).classList.add("hidden");
  form.querySelector(".access-choice").querySelector("#".concat(access_id)).querySelector("p").classList.add("access-noselect");
  form.querySelector(".access-choice").querySelector("#".concat(access_id)).querySelector("p").classList.remove("access-select");
  if (access_id != "for-all") {
    var opt = form.querySelector("#option-".concat(access_id));
    opt.selected = false;
  }
}
function toggle_access(access_id) {
  var elt = form.querySelector(".access-choice").querySelector("#".concat(access_id));
  form.querySelector("#list-".concat(access_id)).classList.toggle("hidden");
  form.querySelector(".access-choice").querySelector("#".concat(access_id)).querySelector("p").classList.toggle("access-select");
  form.querySelector(".access-choice").querySelector("#".concat(access_id)).querySelector("p").classList.toggle("access-noselect");
  if (access_id != "for-all") {
    var opt = form.querySelector("#option-".concat(access_id));
    opt.selected = opt.selected ? false : true;
  }
}
function contentLineFormat(contentLine) {
  // pour chaque ligne de contenu, affiche le type de formulaire en fonction du champ sélectionné (titre, paragraphe, liste, image...)
  var selection = contentLine.querySelector('select');
  selectionDisplay(selection.value, contentLine);
  selection.addEventListener('change', function (e) {
    selectionDisplay(e.target.value, contentLine);
  });
}
function boxToDeleteFormat(el, toDelete) {
  el.querySelectorAll(".redcross").forEach(function (cross) {
    if (toDelete) {
      cross.classList.remove("hidden");
    } else {
      cross.classList.add("hidden");
    }
  });
  el.querySelectorAll(".greycross").forEach(function (cross) {
    if (toDelete) {
      cross.classList.add("hidden");
    } else {
      cross.classList.remove("hidden");
    }
  });
  el.querySelectorAll("p.headline > span").forEach(function (text) {
    return contentToDeleteFormat(text, toDelete);
  });
  el.querySelectorAll("textarea").forEach(function (text) {
    return contentToDeleteFormat(text, toDelete);
  });
  el.querySelectorAll(".cat-content > *").forEach(function (text) {
    return contentToDeleteFormat(text, toDelete);
  });
}
function contentToDeleteFormat(text, toDelete) {
  text.style.textDecoration = toDelete ? "line-through" : "";
  text.style.color = toDelete ? "#e7000b" : "";
}
function selectionDisplay(selectValue, contentLine) {
  // permet d'afficher les champs de contenu "contentFields" en fonction de la valeur sélectionnée "selectValue" (titre, paragraphe, image...)
  contentLine.querySelector(".load-image").style.display = selectValue === 'IM' ? "" : "none"; // affichage image    
  contentLine.querySelector(".load-video").style.display = selectValue === 'VI' ? "" : "none"; // affichage video   
  contentLine.querySelector("textarea").style.display = selectValue === "" | selectValue === "LI" ? "none" : ""; // pas d'affichage texte si liste
  contentLine.querySelector("textarea").style.fontWeight = selectValue === 'TI' ? "bold" : "normal"; // titre en gras
  contentLine.querySelector("textarea").style.height = selectValue === 'PA' ? "100px" : "35px"; // paragraphe sur 4 lignes
  contentLine.querySelector(".list").style.display = selectValue === "LI" ? "" : "none"; // affichage liste
  contentLine.querySelector("textarea").placeholder = selectValue === 'IM' ? "Légende de l'image ..." : "Ecrivez votre texte ..."; // affichage placeholder    
  contentLine.querySelector("textarea").placeholder = selectValue === 'VI' ? "Légende de la video ..." : "Ecrivez votre texte ..."; // affichage placeholder    
}
function imagePreview(e) {
  // affichage de l'image dès qu'elle est sélectionnée dans le browser, avant son téléchargement
  console.log("> imagePreview");
  e.target.parentNode.parentNode.querySelectorAll(".img-preview").forEach(function (output) {
    if (output && e.target.files) {
      output.src = URL.createObjectURL(e.target.files[0]);
      output.onload = function () {
        URL.revokeObjectURL(output.src);
      };
    }
  });
}
function videoPreview(e) {
  // affichage de la video dès qu'elle est sélectionnée dans le browser, avant son téléchargement
  var output = e.target.parentNode.querySelector("video");
  if (output && e.target.files) {
    output.src = URL.createObjectURL(e.target.files[0]);
    output.onload = function () {
      URL.revokeObjectURL(output.src);
    };
  }
}
function testDuplicatedCategory(e) {
  // fonction qui évite de valider 2 catégories avec le même nom, ce qui générerait une erreur 500 :
  // - doublon passe en rouge dans le formulaire
  // - validation rejetée à la soumission
  var submitButton = form.querySelector(".catSubmit");
  var preventValidation = false;
  var _iterator = _createForOfIteratorHelper(form.querySelectorAll("[data-elm-add]")),
    _step;
  try {
    var _loop = function _loop() {
      var lineCat = _step.value;
      var inputCat = lineCat.querySelector(".cat-form");
      var catNameList = Array.from(form.querySelectorAll(".cat-form")).filter(function (c) {
        return c != inputCat;
      }).map(function (c) {
        return c.value;
      }).filter(function (v) {
        return v != '';
      });
      var doublon = catNameList.includes(inputCat.value);
      var willBeDeleted = lineCat.querySelector(".remove input").checked || (e.target.classList.contains("remove") && e.type) == "pointerenter";
      inputCat.style.color = doublon || willBeDeleted ? "#e7000b" : "";
      preventValidation = preventValidation | doublon;
      inputCat.disabled = willBeDeleted ? true : false;
    };
    for (_iterator.s(); !(_step = _iterator.n()).done;) {
      _loop();
    }
  } catch (err) {
    _iterator.e(err);
  } finally {
    _iterator.f();
  }
  submitButton.disabled = preventValidation ? true : false;
  submitButton.style.backgroundColor = preventValidation ? "#aaa" : "";
  form.querySelector(".messageDoublon").classList.toggle("hidden", !preventValidation);
}
function rescaleImage(e) {
  // modifie l'échelle d'une image quand on actionne le slider et affiche la valeur en %
  e.target.closest("div").querySelector(".scale-display").innerText = e.target.value + "%";
  e.target.closest(".load-image").querySelector(".relative").style.width = e.target.value + "%";
}

// pour rescaler une image en actionnant le slider ;
var range = document.querySelectorAll(".load-image > .scale > [type='range']");
range.forEach(function (r) {
  return r.addEventListener("input", rescaleImage);
});
form.addEventListener('click', function (e) {
  // menu déroulant pour le choix des catégories (formulaire dans vignette_tuto.html)
  if (e.target.classList.contains('change-category')) {
    // fold_unfold category
    form.querySelector(".change-category").classList.toggle("rotate-180");
    form.querySelector(".category-choice").classList.toggle("hidden");
    // fold access
    form.querySelector(".change-access").classList.add("rotate-180");
    form.querySelector(".access-choice").classList.add("hidden");
  }

  // choix des catégories dans (champ Tutorial.category, formulaire dans vignette_tuto.html)
  if (e.target.classList.contains('category-choice')) {
    // recherche de l'id de la catégorie concernée
    var cat_id = e.target.closest("li").id;
    // réinitialisation du choix des catégorie (on déselectionne tout)
    form.querySelector(".category-list").querySelectorAll("span").forEach(function (elt) {
      elt.classList.add("hidden");
    });
    form.querySelector(".category-choice").querySelectorAll("p").forEach(function (elt) {
      elt.classList.remove("font-bold");
      elt.classList.remove("bg-slate-200");
    });
    form.querySelector(".category-option").querySelectorAll("option").forEach(function (elt) {
      elt.selected = false;
    });
    // sélection de la nouvelle catégorie choisie
    form.querySelector("#list-".concat(cat_id)).classList.remove("hidden");
    form.querySelector(".category-choice").querySelector("#".concat(cat_id)).querySelector("p").classList.add("font-bold");
    form.querySelector(".category-choice").querySelector("#".concat(cat_id)).querySelector("p").classList.add("bg-slate-200");
    var opt = form.querySelector("#option-".concat(cat_id));
    opt.selected = true;
    // fold category
    form.querySelector(".change-category").classList.add("rotate-180");
    form.querySelector(".category-choice").classList.add("hidden");
  }

  // menu déroulant pour le choix des accès dans (champ Tutorial.restriction, formulaire dans vignette_tuto.html)
  if (e.target.classList.contains('change-access')) {
    // fold_unfold access
    form.querySelector(".change-access").classList.toggle("rotate-180");
    form.querySelector(".access-choice").classList.toggle("hidden");
    // fold category
    form.querySelector(".change-category").classList.add("rotate-180");
    form.querySelector(".category-choice").classList.add("hidden");
  }

  // choix des accès dans (champ Tutorial.restriction, formulaire dans vignette_tuto.html)
  if (e.target.classList.contains('restriction-choice')) {
    // recherche de l'id de la restriction d'accès concernée
    var access_id = e.target.closest("li").id;
    if (access_id == "for-all") {
      // si on clique sur "Tout public" : déactivation de toutes les restrictions
      form.querySelector(".access-choice").querySelectorAll("li").forEach(function (elt) {
        return remove_access(elt.id);
      });
      add_access(access_id);
    } else {
      // si on ne clique pas sur "Tout public", activation ou désactivation de la restriction
      toggle_access(access_id);
      // si toutes les restrictions sont désactivées, on s'assure que "Tout public" apparait bien :
      var opt_list = form.querySelector(".access-option").querySelectorAll("option");
      if (Array.from(opt_list).map(function (elt) {
        return elt.selected;
      }).every(function (val) {
        return !val;
      })) {
        add_access("for-all");
      } else {
        remove_access("for-all");
      }
    }
  }

  // repliement / dépliement des contenus :
  if (e.target.classList.contains('fold')) {
    e.target.closest('[data-elm-add]').querySelectorAll(":scope > *").forEach(function (child) {
      if (child.contains(e.target)) {
        // child.querySelectorAll(".fold").forEach( f => f.style.display = (f.style.display == "none") ? "": "none")
        child.querySelectorAll(".fold").forEach(function (f) {
          return f.classList.toggle("rotate-180");
        });
        child.querySelectorAll(".headline").forEach(function (f) {
          f.style.display = f.style.display == "none" ? "" : "none";
          var select = f.closest('[data-elm-add]').querySelector("select");
          var option = select.options[select.selectedIndex].text;
          // type de contenu sélectionné (Titre, Liste, Image, Question, Réponse...)
          var em = f.closest('[data-elm-add]').querySelector("p.headline > em");
          // contenu (saisi dans textarea)
          var span = f.closest('[data-elm-add]').querySelector("p.headline > span");
          if (option == "Liste") {
            em.innerText = option;
            span.textContent = "- " + f.closest('[data-elm-add]').querySelector(".list textarea").value + "...";
          } else {
            em.innerText = option;
            span.textContent = f.closest('[data-elm-add]').querySelector("textarea").value;
          }
          if (option == "Titre") {
            span.classList.add("font-bold");
          } else {
            span.classList.remove("font-bold");
          }
        });
      } else {
        child.style.display = child.style.display == "none" ? "" : "none";
      }
    });
  }

  // modification des catégories :
  if (e.target.classList.contains('cat-change')) {
    var catName = e.target.closest('[data-elm-add]').querySelector(".cat-content");
    catName.querySelector("span").style.display = catName.querySelector("span").style.display == "inline" ? "none" : "inline";
    catName.querySelector("input").style.display = catName.querySelector("input").style.display == "inline" ? "none" : "inline";
    var inputCat = catName.querySelector("input");
    inputCat.value = catName.querySelector("span").innerHTML;
    testDuplicatedCategory(e);
    inputCat.addEventListener("input", testDuplicatedCategory);
  }

  // suppression d'un élément existant
  if (e.target.classList.contains('removecross')) {
    // test pour savoir si le bloc à supprimer fait partie d'un bloc déjà coché pour la suppression :
    var bloc = e.target.closest('[data-elm-add]');
    var box = bloc.querySelector(".remove > input");
    if (bloc.parentNode.closest('[data-elm-add]') == null || !bloc.parentNode.closest('[data-elm-add]').querySelector(".remove > input").checked) {
      box.checked = !box.checked;
      e.target.closest('[data-elm-add]').querySelectorAll(".remove > input").forEach(function (b) {
        b.checked = box.checked;
      });
      boxToDeleteFormat(e.target.closest('[data-elm-add]'), box.checked);
    }
    if (bloc.dataset.elmAdd == "category") {
      testDuplicatedCategory(e);
    }
  }

  // création d'un nouveau contenu:
  if (e.target.classList.contains('add-elms')) {
    e.preventDefault();
    e.stopPropagation();
    var ou = e.target.closest('[data-elm-add]');
    if (ou) {
      ou = ou.querySelector(e.target.dataset.ou);
    }
    if (!ou) {
      ou = document.querySelector(e.target.dataset.ou);
    }
    var elm = elms.querySelector('[data-elm-add=' + e.target.dataset.elm + ']').cloneNode(50);
    // dragList = list des éléments dragables qui sont sous un élément nouvellement créé 
    // exemple : pour une page créée : draglist = [ [data-ou=content], [data-ou=question] ] 
    var draglist = elm.querySelectorAll('[data-ou]');
    draglist.forEach(function (drag) {
      if (drag) {
        dragula__WEBPACK_IMPORTED_MODULE_0___default()([elm.querySelector(drag.dataset.ou)], {
          moves: function moves(el, container, handle) {
            return handle.classList.contains('handle') && handle.closest('[data-elm-add]').parentNode == container;
          }
        });
      }
    });

    // ajout d'une ligne de formulaire
    ou.append(elm);
    // attribution des input "name" pour identification des clés du request.POST:
    elm.querySelectorAll('input, textarea, select').forEach(function (i) {
      i.name = i.name.replace("xx", "".concat(count));
    });

    // documentation de la foreign key :
    if (elm.querySelector('.fk')) {
      elm.querySelector('.fk').value = elm.closest('[class^="add-"], [class*=" add-"]').id;
    }

    // nouveau parent : marquage de l'id dans la div parent, pour qu'il 
    // soit récupérable par les futurs enfants (foreign key)
    elm.querySelectorAll('[class^="add-"], [class*=" add-"]').forEach(function (par) {
      par.id = par.id.replace("xx", "".concat(count));
    });
    count++;

    // modification des images en cliquant sur le crayon + preview avant téléchargement
    if (elm.querySelector('.load-image')) {
      // attribution des for et id pour apairage entre le label (crayon cliquable) et l'input-image correspondante
      elm.querySelector('.load-image > div > label').htmlFor = elm.querySelector('.load-image > div > label').htmlFor.replace("xx", "".concat(count));
      elm.querySelector('.load-image > div > input').id = elm.querySelector('.load-image > div > input').id.replace("xx", "".concat(count));
      count++;
      // preview des nouvelles images avant téléchargement :
      elm.querySelector('.load-image > div > input').addEventListener("change", imagePreview);
      // modification de l'échelle de l'image :
      elm.querySelector(".load-image > .scale > [type='range']").addEventListener("input", rescaleImage);
    }

    // modification des videos en cliquant sur le crayon + preview avant téléchargement
    if (elm.querySelector('.load-video')) {
      // attribution des for et id pour apairage entre le label (crayon cliquable) et l'input-video correspondante
      elm.querySelector('.load-video > label').htmlFor = elm.querySelector('.load-video > label').htmlFor.replace("xx", "".concat(count));
      elm.querySelector('.load-video > input').id = elm.querySelector('.load-video > input').id.replace("xx", "".concat(count));
      count++;
      // preview des nouvelles videos avant téléchargement :
      elm.querySelector('.load-video > input').addEventListener("change", videoPreview);
    }

    // mise en forme de la ligne de contenu en fonction de la sélection du type de contenu:
    if (elm.dataset.elmAdd == "content") {
      contentLineFormat(elm);
    }

    // nouveaux elm à supprimer (croix grise/rouge) : mise en rouge, biffage
    elm.querySelector('.remove').addEventListener('pointerenter', function (e) {
      e.preventDefault();
      e.stopPropagation();
      boxToDeleteFormat(elm, true);
      if (elm.classList.contains("add-cat")) {
        testDuplicatedCategory(e);
      }
    });
    elm.querySelector('.remove').addEventListener('pointerleave', function (e) {
      e.preventDefault();
      e.stopPropagation();
      boxToDeleteFormat(elm, false);
      if (elm.classList.contains("add-cat")) {
        testDuplicatedCategory(e);
      }
    });
    // nouveaux elm à supprimer (croix grise/rouge) : confirmation (popup) et suppression
    elm.querySelector('.remove').addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      // ---------------------------------------------------
      var elmHasNoData = Array.from(elm.querySelectorAll('textarea')).every(function (x) {
        return x.value === "";
      });
      if (elmHasNoData) {
        elm.remove();
      } else {
        (0,_js_alertbox_js__WEBPACK_IMPORTED_MODULE_1__.displayAlertBox)("alert-delete");
        document.querySelector(".remove-confirm").addEventListener('click', function (e) {
          elm.remove();
          (0,_js_alertbox_js__WEBPACK_IMPORTED_MODULE_1__.hideAlertBox)(e);
        });
      }
      if (elm.classList.contains("add-cat")) {
        testDuplicatedCategory(e);
      }
    });
    // si nouvelle catégorie : vérifier que son nom n'est pas déjà pris
    if (elm.classList.contains("add-cat")) {
      var _inputCat = elm.querySelector(".cat-content input");
      _inputCat.addEventListener("input", testDuplicatedCategory);
    }
  }
});

// Initialisation des éléments draguables
var listou = [];
document.querySelectorAll('form [data-ou]').forEach(function (elm) {
  listou.push(elm.dataset.ou);
});
listou.filter(function (value, index, array) {
  return array.indexOf(value) === index;
}) // uniq
.forEach(function (ou) {
  document.querySelectorAll(ou).forEach(function (a) {
    dragula__WEBPACK_IMPORTED_MODULE_0___default()([a], {
      moves: function moves(el, container, handle) {
        return handle.classList.contains('handle') && handle.closest('[data-elm-add]').parentNode == container;
      }
    });
  });
});

// Gestion dynamique de la numérotation des pages et contenus
form.addEventListener('click', function (e) {
  form.querySelectorAll('[class^="add-"], [class*=" add-"]').forEach(function (elmAdd) {
    var number = 1;
    elmAdd.querySelectorAll(":scope > [data-elm-add]").forEach(function (elm) {
      if (!elm.querySelector(".remove > input").checked) {
        elm.querySelector("input.position").value = number++;
      }
    });
  });
});

// preview des images avant téléchargement :
document.querySelectorAll('.load-image > div > input').forEach(function (el) {
  addEventListener("change", imagePreview);
});

// -------------------------------
// preview des videos avant téléchargement :
document.querySelectorAll('.load-video > input').forEach(function (el) {
  addEventListener("change", videoPreview);
});

/***/ }),

/***/ "./mooc/static/js/alertbox.js":
/*!************************************!*\
  !*** ./mooc/static/js/alertbox.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   displayAlertBox: () => (/* binding */ displayAlertBox),
/* harmony export */   hideAlertBox: () => (/* binding */ hideAlertBox)
/* harmony export */ });
// ---------------------------------------------------------
// GESTION DES POPUPS DE CONFIRMATION DES BOUTONS D'ACTION
// ---------------------------------------------------------

// ! les fonctions displayAlertBox et hideAlertBox devraient être exportées vers user/tuto_admin.js et assets/set_form.js !

function displayAlertBox(alertbox) {
  // affiche une boite de confirmation avant de supprimer un nouveau contenu
  var alertBox = document.querySelector("#" + alertbox);
  var shadowMask = document.getElementById("shadow-mask");
  var backButton = alertBox.querySelector("#back-button");
  alertBox.classList.remove("hidden");
  shadowMask.classList.remove("hidden");
  backButton.addEventListener('click', hideAlertBox);
}
function hideAlertBox(e) {
  // masque la boite de confirmation après suppression ou annulation de suppression d'un nouveau contenu
  var alertBox = e.target.closest(".alert-box");
  var shadowMask = document.getElementById("shadow-mask");
  alertBox.classList.add("hidden");
  shadowMask.classList.add("hidden");
}

// document.querySelector("#deconnect-button").addEventListener('click', (e) => displayAlertBox("alert-deconnect"))

/***/ }),

/***/ "./node_modules/contra/debounce.js":
/*!*****************************************!*\
  !*** ./node_modules/contra/debounce.js ***!
  \*****************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";


var ticky = __webpack_require__(/*! ticky */ "./node_modules/ticky/ticky-browser.js");

module.exports = function debounce (fn, args, ctx) {
  if (!fn) { return; }
  ticky(function run () {
    fn.apply(ctx || null, args || []);
  });
};


/***/ }),

/***/ "./node_modules/contra/emitter.js":
/*!****************************************!*\
  !*** ./node_modules/contra/emitter.js ***!
  \****************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";


var atoa = __webpack_require__(/*! atoa */ "./node_modules/atoa/atoa.js");
var debounce = __webpack_require__(/*! ./debounce */ "./node_modules/contra/debounce.js");

module.exports = function emitter (thing, options) {
  var opts = options || {};
  var evt = {};
  if (thing === undefined) { thing = {}; }
  thing.on = function (type, fn) {
    if (!evt[type]) {
      evt[type] = [fn];
    } else {
      evt[type].push(fn);
    }
    return thing;
  };
  thing.once = function (type, fn) {
    fn._once = true; // thing.off(fn) still works!
    thing.on(type, fn);
    return thing;
  };
  thing.off = function (type, fn) {
    var c = arguments.length;
    if (c === 1) {
      delete evt[type];
    } else if (c === 0) {
      evt = {};
    } else {
      var et = evt[type];
      if (!et) { return thing; }
      et.splice(et.indexOf(fn), 1);
    }
    return thing;
  };
  thing.emit = function () {
    var args = atoa(arguments);
    return thing.emitterSnapshot(args.shift()).apply(this, args);
  };
  thing.emitterSnapshot = function (type) {
    var et = (evt[type] || []).slice(0);
    return function () {
      var args = atoa(arguments);
      var ctx = this || thing;
      if (type === 'error' && opts.throws !== false && !et.length) { throw args.length === 1 ? args[0] : args; }
      et.forEach(function emitter (listen) {
        if (opts.async) { debounce(listen, args, ctx); } else { listen.apply(ctx, args); }
        if (listen._once) { thing.off(type, listen); }
      });
      return thing;
    };
  };
  return thing;
};


/***/ }),

/***/ "./node_modules/crossvent/src/crossvent.js":
/*!*************************************************!*\
  !*** ./node_modules/crossvent/src/crossvent.js ***!
  \*************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";


var customEvent = __webpack_require__(/*! custom-event */ "./node_modules/custom-event/index.js");
var eventmap = __webpack_require__(/*! ./eventmap */ "./node_modules/crossvent/src/eventmap.js");
var doc = __webpack_require__.g.document;
var addEvent = addEventEasy;
var removeEvent = removeEventEasy;
var hardCache = [];

if (!__webpack_require__.g.addEventListener) {
  addEvent = addEventHard;
  removeEvent = removeEventHard;
}

module.exports = {
  add: addEvent,
  remove: removeEvent,
  fabricate: fabricateEvent
};

function addEventEasy (el, type, fn, capturing) {
  return el.addEventListener(type, fn, capturing);
}

function addEventHard (el, type, fn) {
  return el.attachEvent('on' + type, wrap(el, type, fn));
}

function removeEventEasy (el, type, fn, capturing) {
  return el.removeEventListener(type, fn, capturing);
}

function removeEventHard (el, type, fn) {
  var listener = unwrap(el, type, fn);
  if (listener) {
    return el.detachEvent('on' + type, listener);
  }
}

function fabricateEvent (el, type, model) {
  var e = eventmap.indexOf(type) === -1 ? makeCustomEvent() : makeClassicEvent();
  if (el.dispatchEvent) {
    el.dispatchEvent(e);
  } else {
    el.fireEvent('on' + type, e);
  }
  function makeClassicEvent () {
    var e;
    if (doc.createEvent) {
      e = doc.createEvent('Event');
      e.initEvent(type, true, true);
    } else if (doc.createEventObject) {
      e = doc.createEventObject();
    }
    return e;
  }
  function makeCustomEvent () {
    return new customEvent(type, { detail: model });
  }
}

function wrapperFactory (el, type, fn) {
  return function wrapper (originalEvent) {
    var e = originalEvent || __webpack_require__.g.event;
    e.target = e.target || e.srcElement;
    e.preventDefault = e.preventDefault || function preventDefault () { e.returnValue = false; };
    e.stopPropagation = e.stopPropagation || function stopPropagation () { e.cancelBubble = true; };
    e.which = e.which || e.keyCode;
    fn.call(el, e);
  };
}

function wrap (el, type, fn) {
  var wrapper = unwrap(el, type, fn) || wrapperFactory(el, type, fn);
  hardCache.push({
    wrapper: wrapper,
    element: el,
    type: type,
    fn: fn
  });
  return wrapper;
}

function unwrap (el, type, fn) {
  var i = find(el, type, fn);
  if (i) {
    var wrapper = hardCache[i].wrapper;
    hardCache.splice(i, 1); // free up a tad of memory
    return wrapper;
  }
}

function find (el, type, fn) {
  var i, item;
  for (i = 0; i < hardCache.length; i++) {
    item = hardCache[i];
    if (item.element === el && item.type === type && item.fn === fn) {
      return i;
    }
  }
}


/***/ }),

/***/ "./node_modules/crossvent/src/eventmap.js":
/*!************************************************!*\
  !*** ./node_modules/crossvent/src/eventmap.js ***!
  \************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";


var eventmap = [];
var eventname = '';
var ron = /^on/;

for (eventname in __webpack_require__.g) {
  if (ron.test(eventname)) {
    eventmap.push(eventname.slice(2));
  }
}

module.exports = eventmap;


/***/ }),

/***/ "./node_modules/custom-event/index.js":
/*!********************************************!*\
  !*** ./node_modules/custom-event/index.js ***!
  \********************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {


var NativeCustomEvent = __webpack_require__.g.CustomEvent;

function useNative () {
  try {
    var p = new NativeCustomEvent('cat', { detail: { foo: 'bar' } });
    return  'cat' === p.type && 'bar' === p.detail.foo;
  } catch (e) {
  }
  return false;
}

/**
 * Cross-browser `CustomEvent` constructor.
 *
 * https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent.CustomEvent
 *
 * @public
 */

module.exports = useNative() ? NativeCustomEvent :

// IE >= 9
'undefined' !== typeof document && 'function' === typeof document.createEvent ? function CustomEvent (type, params) {
  var e = document.createEvent('CustomEvent');
  if (params) {
    e.initCustomEvent(type, params.bubbles, params.cancelable, params.detail);
  } else {
    e.initCustomEvent(type, false, false, void 0);
  }
  return e;
} :

// IE <= 8
function CustomEvent (type, params) {
  var e = document.createEventObject();
  e.type = type;
  if (params) {
    e.bubbles = Boolean(params.bubbles);
    e.cancelable = Boolean(params.cancelable);
    e.detail = params.detail;
  } else {
    e.bubbles = false;
    e.cancelable = false;
    e.detail = void 0;
  }
  return e;
}


/***/ }),

/***/ "./node_modules/dragula/classes.js":
/*!*****************************************!*\
  !*** ./node_modules/dragula/classes.js ***!
  \*****************************************/
/***/ ((module) => {

"use strict";


var cache = {};
var start = '(?:^|\\s)';
var end = '(?:\\s|$)';

function lookupClass (className) {
  var cached = cache[className];
  if (cached) {
    cached.lastIndex = 0;
  } else {
    cache[className] = cached = new RegExp(start + className + end, 'g');
  }
  return cached;
}

function addClass (el, className) {
  var current = el.className;
  if (!current.length) {
    el.className = className;
  } else if (!lookupClass(className).test(current)) {
    el.className += ' ' + className;
  }
}

function rmClass (el, className) {
  el.className = el.className.replace(lookupClass(className), ' ').trim();
}

module.exports = {
  add: addClass,
  rm: rmClass
};


/***/ }),

/***/ "./node_modules/dragula/dragula.js":
/*!*****************************************!*\
  !*** ./node_modules/dragula/dragula.js ***!
  \*****************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";


var emitter = __webpack_require__(/*! contra/emitter */ "./node_modules/contra/emitter.js");
var crossvent = __webpack_require__(/*! crossvent */ "./node_modules/crossvent/src/crossvent.js");
var classes = __webpack_require__(/*! ./classes */ "./node_modules/dragula/classes.js");
var doc = document;
var documentElement = doc.documentElement;

function dragula (initialContainers, options) {
  var len = arguments.length;
  if (len === 1 && Array.isArray(initialContainers) === false) {
    options = initialContainers;
    initialContainers = [];
  }
  var _mirror; // mirror image
  var _source; // source container
  var _item; // item being dragged
  var _offsetX; // reference x
  var _offsetY; // reference y
  var _moveX; // reference move x
  var _moveY; // reference move y
  var _initialSibling; // reference sibling when grabbed
  var _currentSibling; // reference sibling now
  var _copy; // item used for copying
  var _renderTimer; // timer for setTimeout renderMirrorImage
  var _lastDropTarget = null; // last container item was over
  var _grabbed; // holds mousedown context until first mousemove

  var o = options || {};
  if (o.moves === void 0) { o.moves = always; }
  if (o.accepts === void 0) { o.accepts = always; }
  if (o.invalid === void 0) { o.invalid = invalidTarget; }
  if (o.containers === void 0) { o.containers = initialContainers || []; }
  if (o.isContainer === void 0) { o.isContainer = never; }
  if (o.copy === void 0) { o.copy = false; }
  if (o.copySortSource === void 0) { o.copySortSource = false; }
  if (o.revertOnSpill === void 0) { o.revertOnSpill = false; }
  if (o.removeOnSpill === void 0) { o.removeOnSpill = false; }
  if (o.direction === void 0) { o.direction = 'vertical'; }
  if (o.ignoreInputTextSelection === void 0) { o.ignoreInputTextSelection = true; }
  if (o.mirrorContainer === void 0) { o.mirrorContainer = doc.body; }

  var drake = emitter({
    containers: o.containers,
    start: manualStart,
    end: end,
    cancel: cancel,
    remove: remove,
    destroy: destroy,
    canMove: canMove,
    dragging: false
  });

  if (o.removeOnSpill === true) {
    drake.on('over', spillOver).on('out', spillOut);
  }

  events();

  return drake;

  function isContainer (el) {
    return drake.containers.indexOf(el) !== -1 || o.isContainer(el);
  }

  function events (remove) {
    var op = remove ? 'remove' : 'add';
    touchy(documentElement, op, 'mousedown', grab);
    touchy(documentElement, op, 'mouseup', release);
  }

  function eventualMovements (remove) {
    var op = remove ? 'remove' : 'add';
    touchy(documentElement, op, 'mousemove', startBecauseMouseMoved);
  }

  function movements (remove) {
    var op = remove ? 'remove' : 'add';
    crossvent[op](documentElement, 'selectstart', preventGrabbed); // IE8
    crossvent[op](documentElement, 'click', preventGrabbed);
  }

  function destroy () {
    events(true);
    release({});
  }

  function preventGrabbed (e) {
    if (_grabbed) {
      e.preventDefault();
    }
  }

  function grab (e) {
    _moveX = e.clientX;
    _moveY = e.clientY;

    var ignore = whichMouseButton(e) !== 1 || e.metaKey || e.ctrlKey;
    if (ignore) {
      return; // we only care about honest-to-god left clicks and touch events
    }
    var item = e.target;
    var context = canStart(item);
    if (!context) {
      return;
    }
    _grabbed = context;
    eventualMovements();
    if (e.type === 'mousedown') {
      if (isInput(item)) { // see also: https://github.com/bevacqua/dragula/issues/208
        item.focus(); // fixes https://github.com/bevacqua/dragula/issues/176
      } else {
        e.preventDefault(); // fixes https://github.com/bevacqua/dragula/issues/155
      }
    }
  }

  function startBecauseMouseMoved (e) {
    if (!_grabbed) {
      return;
    }
    if (whichMouseButton(e) === 0) {
      release({});
      return; // when text is selected on an input and then dragged, mouseup doesn't fire. this is our only hope
    }

    // truthy check fixes #239, equality fixes #207, fixes #501
    if ((e.clientX !== void 0 && Math.abs(e.clientX - _moveX) <= (o.slideFactorX || 0)) &&
      (e.clientY !== void 0 && Math.abs(e.clientY - _moveY) <= (o.slideFactorY || 0))) {
      return;
    }

    if (o.ignoreInputTextSelection) {
      var clientX = getCoord('clientX', e) || 0;
      var clientY = getCoord('clientY', e) || 0;
      var elementBehindCursor = doc.elementFromPoint(clientX, clientY);
      if (isInput(elementBehindCursor)) {
        return;
      }
    }

    var grabbed = _grabbed; // call to end() unsets _grabbed
    eventualMovements(true);
    movements();
    end();
    start(grabbed);

    var offset = getOffset(_item);
    _offsetX = getCoord('pageX', e) - offset.left;
    _offsetY = getCoord('pageY', e) - offset.top;

    classes.add(_copy || _item, 'gu-transit');
    renderMirrorImage();
    drag(e);
  }

  function canStart (item) {
    if (drake.dragging && _mirror) {
      return;
    }
    if (isContainer(item)) {
      return; // don't drag container itself
    }
    var handle = item;
    while (getParent(item) && isContainer(getParent(item)) === false) {
      if (o.invalid(item, handle)) {
        return;
      }
      item = getParent(item); // drag target should be a top element
      if (!item) {
        return;
      }
    }
    var source = getParent(item);
    if (!source) {
      return;
    }
    if (o.invalid(item, handle)) {
      return;
    }

    var movable = o.moves(item, source, handle, nextEl(item));
    if (!movable) {
      return;
    }

    return {
      item: item,
      source: source
    };
  }

  function canMove (item) {
    return !!canStart(item);
  }

  function manualStart (item) {
    var context = canStart(item);
    if (context) {
      start(context);
    }
  }

  function start (context) {
    if (isCopy(context.item, context.source)) {
      _copy = context.item.cloneNode(true);
      drake.emit('cloned', _copy, context.item, 'copy');
    }

    _source = context.source;
    _item = context.item;
    _initialSibling = _currentSibling = nextEl(context.item);

    drake.dragging = true;
    drake.emit('drag', _item, _source);
  }

  function invalidTarget () {
    return false;
  }

  function end () {
    if (!drake.dragging) {
      return;
    }
    var item = _copy || _item;
    drop(item, getParent(item));
  }

  function ungrab () {
    _grabbed = false;
    eventualMovements(true);
    movements(true);
  }

  function release (e) {
    ungrab();

    if (!drake.dragging) {
      return;
    }
    var item = _copy || _item;
    var clientX = getCoord('clientX', e) || 0;
    var clientY = getCoord('clientY', e) || 0;
    var elementBehindCursor = getElementBehindPoint(_mirror, clientX, clientY);
    var dropTarget = findDropTarget(elementBehindCursor, clientX, clientY);
    if (dropTarget && ((_copy && o.copySortSource) || (!_copy || dropTarget !== _source))) {
      drop(item, dropTarget);
    } else if (o.removeOnSpill) {
      remove();
    } else {
      cancel();
    }
  }

  function drop (item, target) {
    var parent = getParent(item);
    if (_copy && o.copySortSource && target === _source) {
      parent.removeChild(_item);
    }
    if (isInitialPlacement(target)) {
      drake.emit('cancel', item, _source, _source);
    } else {
      drake.emit('drop', item, target, _source, _currentSibling);
    }
    cleanup();
  }

  function remove () {
    if (!drake.dragging) {
      return;
    }
    var item = _copy || _item;
    var parent = getParent(item);
    if (parent) {
      parent.removeChild(item);
    }
    drake.emit(_copy ? 'cancel' : 'remove', item, parent, _source);
    cleanup();
  }

  function cancel (revert) {
    if (!drake.dragging) {
      return;
    }
    var reverts = arguments.length > 0 ? revert : o.revertOnSpill;
    var item = _copy || _item;
    var parent = getParent(item);
    var initial = isInitialPlacement(parent);
    if (initial === false && reverts) {
      if (_copy) {
        if (parent) {
          parent.removeChild(_copy);
        }
      } else {
        _source.insertBefore(item, _initialSibling);
      }
    }
    if (initial || reverts) {
      drake.emit('cancel', item, _source, _source);
    } else {
      drake.emit('drop', item, parent, _source, _currentSibling);
    }
    cleanup();
  }

  function cleanup () {
    var item = _copy || _item;
    ungrab();
    removeMirrorImage();
    if (item) {
      classes.rm(item, 'gu-transit');
    }
    if (_renderTimer) {
      clearTimeout(_renderTimer);
    }
    drake.dragging = false;
    if (_lastDropTarget) {
      drake.emit('out', item, _lastDropTarget, _source);
    }
    drake.emit('dragend', item);
    _source = _item = _copy = _initialSibling = _currentSibling = _renderTimer = _lastDropTarget = null;
  }

  function isInitialPlacement (target, s) {
    var sibling;
    if (s !== void 0) {
      sibling = s;
    } else if (_mirror) {
      sibling = _currentSibling;
    } else {
      sibling = nextEl(_copy || _item);
    }
    return target === _source && sibling === _initialSibling;
  }

  function findDropTarget (elementBehindCursor, clientX, clientY) {
    var target = elementBehindCursor;
    while (target && !accepted()) {
      target = getParent(target);
    }
    return target;

    function accepted () {
      var droppable = isContainer(target);
      if (droppable === false) {
        return false;
      }

      var immediate = getImmediateChild(target, elementBehindCursor);
      var reference = getReference(target, immediate, clientX, clientY);
      var initial = isInitialPlacement(target, reference);
      if (initial) {
        return true; // should always be able to drop it right back where it was
      }
      return o.accepts(_item, target, _source, reference);
    }
  }

  function drag (e) {
    if (!_mirror) {
      return;
    }
    e.preventDefault();

    var clientX = getCoord('clientX', e) || 0;
    var clientY = getCoord('clientY', e) || 0;
    var x = clientX - _offsetX;
    var y = clientY - _offsetY;

    _mirror.style.left = x + 'px';
    _mirror.style.top = y + 'px';

    var item = _copy || _item;
    var elementBehindCursor = getElementBehindPoint(_mirror, clientX, clientY);
    var dropTarget = findDropTarget(elementBehindCursor, clientX, clientY);
    var changed = dropTarget !== null && dropTarget !== _lastDropTarget;
    if (changed || dropTarget === null) {
      out();
      _lastDropTarget = dropTarget;
      over();
    }
    var parent = getParent(item);
    if (dropTarget === _source && _copy && !o.copySortSource) {
      if (parent) {
        parent.removeChild(item);
      }
      return;
    }
    var reference;
    var immediate = getImmediateChild(dropTarget, elementBehindCursor);
    if (immediate !== null) {
      reference = getReference(dropTarget, immediate, clientX, clientY);
    } else if (o.revertOnSpill === true && !_copy) {
      reference = _initialSibling;
      dropTarget = _source;
    } else {
      if (_copy && parent) {
        parent.removeChild(item);
      }
      return;
    }
    if (
      (reference === null && changed) ||
      reference !== item &&
      reference !== nextEl(item)
    ) {
      _currentSibling = reference;
      dropTarget.insertBefore(item, reference);
      drake.emit('shadow', item, dropTarget, _source);
    }
    function moved (type) { drake.emit(type, item, _lastDropTarget, _source); }
    function over () { if (changed) { moved('over'); } }
    function out () { if (_lastDropTarget) { moved('out'); } }
  }

  function spillOver (el) {
    classes.rm(el, 'gu-hide');
  }

  function spillOut (el) {
    if (drake.dragging) { classes.add(el, 'gu-hide'); }
  }

  function renderMirrorImage () {
    if (_mirror) {
      return;
    }
    var rect = _item.getBoundingClientRect();
    _mirror = _item.cloneNode(true);
    _mirror.style.width = getRectWidth(rect) + 'px';
    _mirror.style.height = getRectHeight(rect) + 'px';
    classes.rm(_mirror, 'gu-transit');
    classes.add(_mirror, 'gu-mirror');
    o.mirrorContainer.appendChild(_mirror);
    touchy(documentElement, 'add', 'mousemove', drag);
    classes.add(o.mirrorContainer, 'gu-unselectable');
    drake.emit('cloned', _mirror, _item, 'mirror');
  }

  function removeMirrorImage () {
    if (_mirror) {
      classes.rm(o.mirrorContainer, 'gu-unselectable');
      touchy(documentElement, 'remove', 'mousemove', drag);
      getParent(_mirror).removeChild(_mirror);
      _mirror = null;
    }
  }

  function getImmediateChild (dropTarget, target) {
    var immediate = target;
    while (immediate !== dropTarget && getParent(immediate) !== dropTarget) {
      immediate = getParent(immediate);
    }
    if (immediate === documentElement) {
      return null;
    }
    return immediate;
  }

  function getReference (dropTarget, target, x, y) {
    var horizontal = o.direction === 'horizontal';
    var reference = target !== dropTarget ? inside() : outside();
    return reference;

    function outside () { // slower, but able to figure out any position
      var len = dropTarget.children.length;
      var i;
      var el;
      var rect;
      for (i = 0; i < len; i++) {
        el = dropTarget.children[i];
        rect = el.getBoundingClientRect();
        if (horizontal && (rect.left + rect.width / 2) > x) { return el; }
        if (!horizontal && (rect.top + rect.height / 2) > y) { return el; }
      }
      return null;
    }

    function inside () { // faster, but only available if dropped inside a child element
      var rect = target.getBoundingClientRect();
      if (horizontal) {
        return resolve(x > rect.left + getRectWidth(rect) / 2);
      }
      return resolve(y > rect.top + getRectHeight(rect) / 2);
    }

    function resolve (after) {
      return after ? nextEl(target) : target;
    }
  }

  function isCopy (item, container) {
    return typeof o.copy === 'boolean' ? o.copy : o.copy(item, container);
  }
}

function touchy (el, op, type, fn) {
  var touch = {
    mouseup: 'touchend',
    mousedown: 'touchstart',
    mousemove: 'touchmove'
  };
  var pointers = {
    mouseup: 'pointerup',
    mousedown: 'pointerdown',
    mousemove: 'pointermove'
  };
  var microsoft = {
    mouseup: 'MSPointerUp',
    mousedown: 'MSPointerDown',
    mousemove: 'MSPointerMove'
  };
  if (__webpack_require__.g.navigator.pointerEnabled) {
    crossvent[op](el, pointers[type], fn);
  } else if (__webpack_require__.g.navigator.msPointerEnabled) {
    crossvent[op](el, microsoft[type], fn);
  } else {
    crossvent[op](el, touch[type], fn);
    crossvent[op](el, type, fn);
  }
}

function whichMouseButton (e) {
  if (e.touches !== void 0) { return e.touches.length; }
  if (e.which !== void 0 && e.which !== 0) { return e.which; } // see https://github.com/bevacqua/dragula/issues/261
  if (e.buttons !== void 0) { return e.buttons; }
  var button = e.button;
  if (button !== void 0) { // see https://github.com/jquery/jquery/blob/99e8ff1baa7ae341e94bb89c3e84570c7c3ad9ea/src/event.js#L573-L575
    return button & 1 ? 1 : button & 2 ? 3 : (button & 4 ? 2 : 0);
  }
}

function getOffset (el) {
  var rect = el.getBoundingClientRect();
  return {
    left: rect.left + getScroll('scrollLeft', 'pageXOffset'),
    top: rect.top + getScroll('scrollTop', 'pageYOffset')
  };
}

function getScroll (scrollProp, offsetProp) {
  if (typeof __webpack_require__.g[offsetProp] !== 'undefined') {
    return __webpack_require__.g[offsetProp];
  }
  if (documentElement.clientHeight) {
    return documentElement[scrollProp];
  }
  return doc.body[scrollProp];
}

function getElementBehindPoint (point, x, y) {
  point = point || {};
  var state = point.className || '';
  var el;
  point.className += ' gu-hide';
  el = doc.elementFromPoint(x, y);
  point.className = state;
  return el;
}

function never () { return false; }
function always () { return true; }
function getRectWidth (rect) { return rect.width || (rect.right - rect.left); }
function getRectHeight (rect) { return rect.height || (rect.bottom - rect.top); }
function getParent (el) { return el.parentNode === doc ? null : el.parentNode; }
function isInput (el) { return el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.tagName === 'SELECT' || isEditable(el); }
function isEditable (el) {
  if (!el) { return false; } // no parents were editable
  if (el.contentEditable === 'false') { return false; } // stop the lookup
  if (el.contentEditable === 'true') { return true; } // found a contentEditable element in the chain
  return isEditable(getParent(el)); // contentEditable is set to 'inherit'
}

function nextEl (el) {
  return el.nextElementSibling || manually();
  function manually () {
    var sibling = el;
    do {
      sibling = sibling.nextSibling;
    } while (sibling && sibling.nodeType !== 1);
    return sibling;
  }
}

function getEventHost (e) {
  // on touchend event, we have to use `e.changedTouches`
  // see http://stackoverflow.com/questions/7192563/touchend-event-properties
  // see https://github.com/bevacqua/dragula/issues/34
  if (e.targetTouches && e.targetTouches.length) {
    return e.targetTouches[0];
  }
  if (e.changedTouches && e.changedTouches.length) {
    return e.changedTouches[0];
  }
  return e;
}

function getCoord (coord, e) {
  var host = getEventHost(e);
  var missMap = {
    pageX: 'clientX', // IE8
    pageY: 'clientY' // IE8
  };
  if (coord in missMap && !(coord in host) && missMap[coord] in host) {
    coord = missMap[coord];
  }
  return host[coord];
}

module.exports = dragula;


/***/ }),

/***/ "./mooc/static/assets/drag.css":
/*!*************************************!*\
  !*** ./mooc/static/assets/drag.css ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
// extracted by mini-css-extract-plugin


/***/ }),

/***/ "./node_modules/ticky/ticky-browser.js":
/*!*********************************************!*\
  !*** ./node_modules/ticky/ticky-browser.js ***!
  \*********************************************/
/***/ ((module) => {

var si = typeof setImmediate === 'function', tick;
if (si) {
  tick = function (fn) { setImmediate(fn); };
} else {
  tick = function (fn) { setTimeout(fn, 0); };
}

module.exports = tick;

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = __webpack_modules__;
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/chunk loaded */
/******/ 	(() => {
/******/ 		var deferred = [];
/******/ 		__webpack_require__.O = (result, chunkIds, fn, priority) => {
/******/ 			if(chunkIds) {
/******/ 				priority = priority || 0;
/******/ 				for(var i = deferred.length; i > 0 && deferred[i - 1][2] > priority; i--) deferred[i] = deferred[i - 1];
/******/ 				deferred[i] = [chunkIds, fn, priority];
/******/ 				return;
/******/ 			}
/******/ 			var notFulfilled = Infinity;
/******/ 			for (var i = 0; i < deferred.length; i++) {
/******/ 				var [chunkIds, fn, priority] = deferred[i];
/******/ 				var fulfilled = true;
/******/ 				for (var j = 0; j < chunkIds.length; j++) {
/******/ 					if ((priority & 1 === 0 || notFulfilled >= priority) && Object.keys(__webpack_require__.O).every((key) => (__webpack_require__.O[key](chunkIds[j])))) {
/******/ 						chunkIds.splice(j--, 1);
/******/ 					} else {
/******/ 						fulfilled = false;
/******/ 						if(priority < notFulfilled) notFulfilled = priority;
/******/ 					}
/******/ 				}
/******/ 				if(fulfilled) {
/******/ 					deferred.splice(i--, 1)
/******/ 					var r = fn();
/******/ 					if (r !== undefined) result = r;
/******/ 				}
/******/ 			}
/******/ 			return result;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/compat get default export */
/******/ 	(() => {
/******/ 		// getDefaultExport function for compatibility with non-harmony modules
/******/ 		__webpack_require__.n = (module) => {
/******/ 			var getter = module && module.__esModule ?
/******/ 				() => (module['default']) :
/******/ 				() => (module);
/******/ 			__webpack_require__.d(getter, { a: getter });
/******/ 			return getter;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/global */
/******/ 	(() => {
/******/ 		__webpack_require__.g = (function() {
/******/ 			if (typeof globalThis === 'object') return globalThis;
/******/ 			try {
/******/ 				return this || new Function('return this')();
/******/ 			} catch (e) {
/******/ 				if (typeof window === 'object') return window;
/******/ 			}
/******/ 		})();
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/jsonp chunk loading */
/******/ 	(() => {
/******/ 		// no baseURI
/******/ 		
/******/ 		// object to store loaded and loading chunks
/******/ 		// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 		// [resolve, reject, Promise] = chunk loading, 0 = chunk loaded
/******/ 		var installedChunks = {
/******/ 			"/set_form": 0,
/******/ 			"drag": 0
/******/ 		};
/******/ 		
/******/ 		// no chunk on demand loading
/******/ 		
/******/ 		// no prefetching
/******/ 		
/******/ 		// no preloaded
/******/ 		
/******/ 		// no HMR
/******/ 		
/******/ 		// no HMR manifest
/******/ 		
/******/ 		__webpack_require__.O.j = (chunkId) => (installedChunks[chunkId] === 0);
/******/ 		
/******/ 		// install a JSONP callback for chunk loading
/******/ 		var webpackJsonpCallback = (parentChunkLoadingFunction, data) => {
/******/ 			var [chunkIds, moreModules, runtime] = data;
/******/ 			// add "moreModules" to the modules object,
/******/ 			// then flag all "chunkIds" as loaded and fire callback
/******/ 			var moduleId, chunkId, i = 0;
/******/ 			if(chunkIds.some((id) => (installedChunks[id] !== 0))) {
/******/ 				for(moduleId in moreModules) {
/******/ 					if(__webpack_require__.o(moreModules, moduleId)) {
/******/ 						__webpack_require__.m[moduleId] = moreModules[moduleId];
/******/ 					}
/******/ 				}
/******/ 				if(runtime) var result = runtime(__webpack_require__);
/******/ 			}
/******/ 			if(parentChunkLoadingFunction) parentChunkLoadingFunction(data);
/******/ 			for(;i < chunkIds.length; i++) {
/******/ 				chunkId = chunkIds[i];
/******/ 				if(__webpack_require__.o(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 					installedChunks[chunkId][0]();
/******/ 				}
/******/ 				installedChunks[chunkId] = 0;
/******/ 			}
/******/ 			return __webpack_require__.O(result);
/******/ 		}
/******/ 		
/******/ 		var chunkLoadingGlobal = self["webpackChunkmooc"] = self["webpackChunkmooc"] || [];
/******/ 		chunkLoadingGlobal.forEach(webpackJsonpCallback.bind(null, 0));
/******/ 		chunkLoadingGlobal.push = webpackJsonpCallback.bind(null, chunkLoadingGlobal.push.bind(chunkLoadingGlobal));
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module depends on other loaded chunks and execution need to be delayed
/******/ 	__webpack_require__.O(undefined, ["drag"], () => (__webpack_require__("./mooc/static/assets/set_form.js")))
/******/ 	var __webpack_exports__ = __webpack_require__.O(undefined, ["drag"], () => (__webpack_require__("./mooc/static/assets/drag.css")))
/******/ 	__webpack_exports__ = __webpack_require__.O(__webpack_exports__);
/******/ 	
/******/ })()
;