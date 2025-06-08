function onSearch(e) {
  alert(e.target.form.q);
}

function modalDelete(e) {
  let elem = document.querySelector(".modal-delete");
  elem.style.display = "block";
}
