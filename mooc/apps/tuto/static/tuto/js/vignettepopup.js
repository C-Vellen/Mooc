// ---------------------------------------------------------
// AFFICHAGE DE LA VIGNETTE D'UN TUTORIEL EN POPUP
// ---------------------------------------------------------

const vignettePopup = document.querySelector("#vignette-popup")
const shadowMask = document.getElementById("shadow-mask")
const tutoTitre = document.querySelector("#tutoTitre")

tutoTitre.addEventListener('click', displayVignettePopup)
vignettePopup.addEventListener('click', hideVignettePopup)


function displayVignettePopup(e) {
    // affiche le popup de la vignette
    vignettePopup.classList.remove("hidden")
    shadowMask.classList.remove("hidden")
}

function hideVignettePopup(e) {
    // masque le popup de la vignette
    vignettePopup.classList.add("hidden")
    shadowMask.classList.add("hidden")
}
