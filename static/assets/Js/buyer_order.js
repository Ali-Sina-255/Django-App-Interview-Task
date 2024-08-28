const openBuyerModal = document.querySelectorAll(".openBuyerModal");
const closeBuyerModal = document.getElementById("closeBuyrModal");
const buyerModal = document.getElementById("modal_order");
openBuyerModal.forEach(function (button) {
  button.addEventListener("click", function () {
    buyerModal.classList.remove("hidden");
  });
});

closeBuyerModal.addEventListener("click", () => {
  buyerModal.classList.add("hidden");
});

window.addEventListener("click", (event) => {
  if (event.target == buyerModal) {
    buyerModal.classList.add("hidden");
  }
});

// Review section

const reviewBuyerModal = document.querySelectorAll(".reviewModal");
const reviewModal = document.getElementById("modal_review");
const closeReviewModal = document.getElementById("closeReviewModal");
reviewBuyerModal.forEach(function (button) {
  button.addEventListener("click", function () {
    reviewModal.classList.remove("hidden");
  });
});
closeReviewModal.addEventListener("click", () => {
  reviewModal.classList.add("hidden");
});

window.addEventListener("click", (event) => {
  if (event.target == reviewModal) {
    reviewModal.classList.add("hidden");
  }
});
