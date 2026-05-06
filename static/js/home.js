// Homepage functionality 
const openMenuBtn = document.getElementById("open-menu");
const closeMenuBtn = document.getElementById("close-menu");
const menu = document.getElementById("menu");
const menuItems = menu.querySelectorAll("a");

function openMenu() {
  menu.classList.remove("max-md:w-0");
  menu.classList.add("max-md:w-full");
}

function closeMenu() {
  menu.classList.remove("max-md:w-full");
  menu.classList.add("max-md:w-0");
}

openMenuBtn.addEventListener("click", openMenu);
closeMenuBtn.addEventListener("click", closeMenu);
menuItems.forEach((item) => {
  item.addEventListener("click", closeMenu);
});

