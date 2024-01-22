function delete_pa(id){
    // console.log(`{% url 'patient:delete_patient' id=${id} %}`)
    document.querySelector('#patient-delete-btn').setAttribute('href',`delete/${id}`)
}
let isMenuOpen = false;

function toggleDropdown() {
  let dropdown = document.getElementById("myDropdown");
  dropdown.classList.toggle("show-dropdown");


}

// Additionally, we’ve added functionality to close the dropdown when the user clicks outside of it.

// Close the dropdown if the user clicks outside of it
window.onclick = function (event) {
  if (!event.target.matches(".dropdown-btn")) {
    let dropdowns = document.getElementsByClassName("dropdown-content");
  

    for (let i = 0; i < dropdowns.length; i++) {
      let openDropdown = dropdowns[i];
      if (openDropdown.classList.contains("show-dropdown")) {
        openDropdown.classList.remove("show-dropdown");
        isMenuOpen = false;
      }
    }
  }
};
