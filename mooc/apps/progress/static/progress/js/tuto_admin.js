// -----------------------------------------------------------------------
// GESTION DU MENU DEROULANT DES VERSIONS DES TUTOS ET DES POPUPS D'ALERTE 
// -----------------------------------------------------------------------

// -----------------------------------------------------------------------
// MENUS DEROULANTS DES PAGES TUTO_ADMIN_AUTEUR ET GESTIONNAIRE (VERSIONS DES TUTOS)

const tutobases = document.getElementsByClassName("tutobase")
const dropdowns = document.getElementsByClassName("dropdown")
const menus = document.getElementsByClassName("menu")
const selectVersions = document.getElementsByClassName("selection")

let menuDeroule = false

// Initialisation de l'affichage : dernière version affichée
for(let tutobaseNode of tutobases){
    const tutos = tutobaseNode.getElementsByClassName("tutorial")
    const lastVersion = Math.max(...Array.from(tutos).map( t => parseInt(t.id)))
    displayTutoVersion(tutobaseNode, lastVersion)
}
for(let dropdown of dropdowns) {
    dropdown.addEventListener('click', deroulerMenu)
}
for(let selectVersion of selectVersions) {
    selectVersion.addEventListener('click', selectTutoVersion)
}

function deroulerMenu(e) {
    e.preventDefault()
    if (menuDeroule) {
        for(let menu of menus){
            menu.classList.add("collapse")
        }
    } else {
        const menuSelection = e.currentTarget.parentNode.querySelector(".menu")
        menuSelection.classList.remove("collapse")
    }
    menuDeroule = ! menuDeroule
}
function dropMenu(e) {
    e.preventDefault()
    const menuList = e.currentTarget.parentNode.querySelector("ul")
    menuList.classList.remove("collapse")
}
function collapseMenu(e) {
    e.preventDefault()
    const menuList = e.currentTarget.parentNode.querySelector("ul")
    menuList.classList.add("collapse")
}
function selectTutoVersion(e) {
    e.preventDefault()
    const tutoSelect = e.currentTarget.id
    const tutobaseId = tutoSelect.split("-")[0]
    const tutoVersion = tutoSelect.split("-")[1]
    const tutobaseNode = document.getElementById("tb"+"-"+tutobaseId)
    displayTutoVersion(tutobaseNode, tutoVersion)
    deroulerMenu(e)
}
function displayTutoVersion(tutobaseNode, tutoVersion) {
    for(let node of tutobaseNode.getElementsByClassName("tutorial")){
        if(node.id == tutoVersion) {
            node.classList.remove("hidden")
        } else {
            node.classList.add("hidden")
        }
    }
}

//--------------------------------------------------------------------------------
// POPUPS DE CONFIRMATION DES BOUTONS D'ACTION DES PAGES USER/TUTO_ADMIN_AUTEUR ET GESTIONNAIRE
// AINSI QUE DE LA PAGE TUTO/UPDATE_TUTO POUR LE BOUTON D'ANNULATION DES MODIFICATIONS

// ! les fonctions displayAlertBox et hideAlertBox devraient être importées de js/alertbox.js !
import {displayAlertBox} from '../../../../../static/js/alertbox.js'
  
const buttonList = ["submit", "new", "reject", "publish", "depublish", "republish", "archive", "dearchive", "delete", ].map(x => x+'-button')
setButtons("alert-update", buttonList)       // boutons de user/tuto_admin/gestionnaire.html
setButtons("alert-leave", ["leave-button"])  // boutons de user/tuto_admin/auteur.html

function setButtons(alertbox, buttonList) {
    for(let button of buttonList) {
        document.querySelectorAll("."+button).forEach(btn => {btn.addEventListener('click', e => {
            const message = e.target.getAttribute('data-message')
            const link = e.target.getAttribute('data-link')
            const act_text = e.target.innerHTML 
            const btn_style = e.target.classList[1]
            console.log("btn_style= ", btn_style)
            const alertBox = document.querySelector('#'+alertbox)
            alertBox.querySelector("p").innerHTML = message
            alertBox.querySelector("a").href = link
            if (alertbox != "alert-leave") {
                // recopie le style et le contenu du bouton dans le bouton de confirmation du popup
                alertBox.querySelector("a").innerHTML = act_text
                alertBox.querySelector("a").classList.remove("red-button")
                alertBox.querySelector("a").classList.add(btn_style)
            }
            displayAlertBox(alertbox)
        })})     
    }
}




  