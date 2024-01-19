function delete_pa(id){
    // console.log(`{% url 'patient:delete_patient' id=${id} %}`)
    document.querySelector('#patient-delete-btn').setAttribute('href',`delete/${id}`)
}