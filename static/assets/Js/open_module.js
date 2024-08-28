const openModalButton = document.querySelectorAll(".openModalButton");
const closeModalButton = document.getElementById("closeModalButton");
const modal_section = document.getElementById("modal");

// Add an event listener to each button
openModalButton.forEach(function (button) {
  button.addEventListener("click", function () {
    modal_section.classList.remove("hidden");
  });
});

closeModalButton.addEventListener("click", () => {
  modal_section.classList.add("hidden");
});

window.addEventListener("click", (event) => {
  if (event.target == modal) {
    modal_section.classList.add("hidden");
  }
});


