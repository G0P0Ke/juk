
function confirm(tenant_id) {
    let confirm = document.getElementById('confirm-id');
    let notconfirm = document.getElementById('notconfirm-id');
    confirm.value = tenant_id;
    notconfirm.value = 0;
}


function notconfirm(tenant_id) {
    let confirm = document.getElementById('confirm-id');
    let notconfirm = document.getElementById('notconfirm-id');
    confirm.value = 0;
    notconfirm.value = tenant_id;
}