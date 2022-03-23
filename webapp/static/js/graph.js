var selectDiocese;
var selectPersonOfDiocese;

window.addEventListener('DOMContentLoaded', function codeAddress() {
    mainChart();
    chartByDiocese();
    chartOfDiocese();
    actions();
})

$(document).ready(function () {
    $('#participants').DataTable({
        "order": [],
        "language": {
            "lengthMenu": "Afficher _MENU_ par page",
            "zeroRecords": "Aucun participant",
            "info": "Affichage page _PAGE_ sur _PAGES_ de _TOTAL_",
            "infoEmpty": "Aucun participant",
            "emptyTable": "Aucun participant",
            "infoFiltered": "(filtered from _MAX_ total records)",
            "search": "Rechercher : ",
            "paginate": {
                "first": "Première page",
                "last": "Dernière page",
                "next": "Suivant",
                "previous": "Précédent"
            },
        }
    });
});

function actions() {
    selectDiocese = document.getElementById('diocese')
    selectDiocese.onchange = build_url
    selectPersonOfDiocese = document.getElementById('person-of-diocese');
    selectPersonOfDiocese.onchange = build_url
}

function build_url() {
    var params = [];

    if(selectDiocese.value) {
        params.push('diocese='+selectDiocese.value)
    }


    console.log(selectPersonOfDiocese.value)


    if(selectPersonOfDiocese.value && selectPersonOfDiocese.value != 'all') {
        params.push('person_of_diocese='+selectPersonOfDiocese.value)
    }

    window.location = '/inscrits/'+ (params.length > 0 ? '?'+ params.join('&') : '' )

}

function chartOfDiocese() {
    "use strict";
    var chart = document.getElementById('chart-diocese');
    new Chart(chart, {
        type: 'line',
        options: {
            responsive: true,
        },
        data: {
            labels: chart_of_diocese_labels,
            datasets: [
                {
                    label: 'Progression',
                    data: chart_of_diocese_datas,
                    fill: false,
                    borderColor: 'rgb(128,128,255)',

                }
            ]
        }
    });
}

function chartByDiocese() {
    "use strict";
    var chart = document.getElementById('chart-by-diocese');
    new Chart(chart, {
        type: 'pie',
        options: {
            responsive: true,
            maintainAspectRatio: false
        },
        data: {
            labels: chart_by_diocese_labels,
            datasets: [
                {
                    data: chart_by_diocese_datas,
                    fill: true,
                    backgroundColor: ['red', 'orange', 'yellow', 'green', 'blue']
                }
            ]
        }
    });
}

function mainChart() {
    "use strict";
    var chart = document.getElementById('main-chart');
    new Chart(chart, {
        type: 'line',
        data: {
            labels: main_chart_labels,
            datasets: [
                {
                    label: 'Progression',
                    data: main_chart_datas,
                    fill: false,
                    borderColor: 'rgb(255,128,128)',
                }
            ]
        }
    });
}