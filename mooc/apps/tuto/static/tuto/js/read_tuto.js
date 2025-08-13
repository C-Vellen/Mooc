
// -------------------------------------------------------------------------
// GESTION DU MENU SOMMAIRE DEROULANT ET DE L'AFFICHAGE DES CORRECTIONS QUIZ
// -------------------------------------------------------------------------

// -----------------------------------------------------------------------
// SOMMAIRE DEROULANT

const sommaire = document.getElementById("sommaire_box");
const caret = document.getElementById("caret");
const sommaire_menu_deroulant = document.querySelector("#sommaire_menu_deroulant")
let sommaire_deroule = false;

sommaire_menu_deroulant.style.maxHeight = "0px"
sommaire .addEventListener('click', afficherSommaire);

// affichage / masquage du sommaire déroulant si clic sur la flèche
function afficherSommaire(event) {
    event.preventDefault()
    if (sommaire_deroule) {
        sommaire_menu_deroulant.style.maxHeight = "0px"
    } else if (!sommaire_deroule) {
        sommaire_menu_deroulant.style.display = "block" 
        setTimeout( () => {
            sommaire_menu_deroulant.style.maxHeight = "1000px"
        }, 30)
    }
    sommaire_deroule = !sommaire_deroule
    caret.style.transform = (sommaire_deroule)? "rotate(180deg)" : ""
}

// -----------------------------------------------------------------------
// AFFICHAGE / MASQUAGE DES CORRECTIONS DU QUIZ

const displayButton = document.querySelector(".display-correction")
const hideButton = document.querySelector(".hide-correction")
const correctionList = document.querySelectorAll(".correction")


displayButton.addEventListener('click', e =>{
    displayButton.classList.add("hidden")
    hideButton.classList.remove("hidden")
    correctionList.forEach(c => {
        c.classList.remove("hidden")
    })

    document.getElementById('quiz').scrollIntoView({
        block: "start",
        })
})
hideButton.addEventListener('click', e =>{
 
    displayButton.classList.remove("hidden")
    hideButton.classList.add("hidden")
    correctionList.forEach(c => {
        c.classList.add("hidden")
    })
    // document.getElementById('quiz').scrollIntoView({
    displayButton.scrollIntoView({
            behaviour:"smooth", 
        block: "end",
        })

})
        






