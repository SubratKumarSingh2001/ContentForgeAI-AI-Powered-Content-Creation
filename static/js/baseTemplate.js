// Dashboard functionality 
const mobileMenuBtn = document.getElementById("mobileMenuBtn");
const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("overlay");

mobileMenuBtn.addEventListener("click", () => {
  sidebar.classList.toggle("open");
  sidebar.classList.toggle("hidden");
  overlay.classList.toggle("hidden");
});

overlay.addEventListener("click", () => {
  sidebar.classList.add("hidden");
  sidebar.classList.remove("open");
  overlay.classList.add("hidden");
});