console.log("aaa");

// Insertar nueva fila
function insertCriterion() {
    var tBodyRef = document.getElementById('criteria-table').getElementsByTagName('tbody')[0];
    var row = tBodyRef.insertRow();
    const arr = [];
    for (let i = 0; i < 2; i++) {
        arr.push(row.insertCell());
        arr[i].innerHTML = "CELDA";
    }
    console.log("hola");
}

// eventListener sobre el boton de confirmar nuevo criterio.
var criterionConfirmBtn = document.getElementById('new-criterion-finish-btn');
criterionConfirmBtn.addEventListener("click",insertCriterion());