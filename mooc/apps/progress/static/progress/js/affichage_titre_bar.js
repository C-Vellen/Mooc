// -------------------------------------------------------------------
// AFFICHAGE DES TITRES DES PAGES AU SURVOL DE LA BARRE DE PROGRESSION 
// -------------------------------------------------------------------

const page_progress = document.querySelectorAll(".page-index")

page_progress.forEach(hoverTitre)
    
function hoverTitre(t) {

    t.querySelector(".page-bar").addEventListener("mouseover", (e) => {
        console.log('hover')
        titre = t.querySelector(".titre-page")
        titre.classList.remove("hidden")
    })

    t.querySelector(".page-bar").addEventListener("mouseout", (e) => {
        console.log('exit')
        titre = t.querySelector(".titre-page")
        titre.classList.add("hidden")
    })

}


