var NB_DORTOIR = 1;

(function () {
    var btn_form_ajouter_site = document.getElementById('btn_form_ajouter_site');
    var ajouter_dortoir = document.getElementById("ajouter_dortoir");
    var tbody_dortoitrs = document.getElementById("tbody_dortoitrs");

    btn_form_ajouter_site.onclick = handle_ajouter_site;
    ajouter_dortoir.onclick = handle_ajouter_dortoir;

    // dortoirs
    if (typeof dortoirs_du_site != 'undefined') {
        dortoirs_du_site.forEach(function (dort) {
            handle_ajouter_dortoir(dort)
        });
    }
})()

function handle_ajouter_site() {
    var form_element = document.getElementById("form_ajouter_site")
    if (form_element.style.display == 'block') {
        if(typeof dortoirs_du_site != 'undefined') {
            window.location = '/sites'
        }
        form_element.style.display = 'none';
        btn_form_ajouter_site.innerHTML = 'Ajouter un site';
        btn_form_ajouter_site.classList.add('btn-primary');
        btn_form_ajouter_site.classList.remove('btn-secondary');
    } else {
        form_element.style.display = 'block';
        btn_form_ajouter_site.innerHTML = 'Annuler';
        btn_form_ajouter_site.classList.remove('btn-primary');
        btn_form_ajouter_site.classList.add('btn-secondary');
    }
}

function handle_ajouter_dortoir(dort) {
    var ligne = document.createElement('tr');
    ligne.setAttribute('id', 'dortoir_' + NB_DORTOIR);
    dort = dort.id ? dort : false;

    var btn_delete = dort ? 
    `<form action="/sites/supprimer-dortoir" style="display: inline-block;" method="post">
        ${csrf}
        <input type="hidden" name="id" value="${dort.id}">
        <input type="hidden" name="id_site" value="${document.getElementById('id_site').value}">
        <button class="btn btn-danger" type="submit"> Supprimer </button>
    </form>` : 
    `<button class="btn btn-danger" type="button" onclick="supprimer_dortoir(${NB_DORTOIR})"> Supprimer </button>`

    ligne.innerHTML = `
        <td>
        <div class="mb-1">
            <input type="hidden" ${dort ? 'value="' + dort.id + '"' : ''} name="dortoir.id_${NB_DORTOIR}">
            <input type="text" name="dortoir.code_${NB_DORTOIR}" ${dort ? 'value="' + dort.code + '"' : ''} required="required" class="form-control">
        </div>
        </td>
        <td>
        <div class="mb-1">
            <input type="text" name="dortoir.capacite_${NB_DORTOIR}" ${dort ? 'value="' + dort.capacite + '"' : ''} required="required" class="form-control">
        </div>
        </td>
        <td>
        ${btn_delete}
        </td>`;

    tbody_dortoitrs.appendChild(ligne);
    NB_DORTOIR++;
}

function supprimer_dortoir(index) {
    document.getElementById('dortoir_' + index).remove();
}

function annuler_modifier() {
    
}