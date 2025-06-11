let index = 0;
const images = document.querySelectorAll(".carousel-image");
const prevBtn = document.getElementById("prev");
const nextBtn = document.getElementById("next");

function showImage(i) {
  images.forEach(img => img.classList.remove("active"));
  images[i].classList.add("active");
}

function nextImage() {
  index = (index + 1) % images.length;
  showImage(index);
}

function prevImage() {
  index = (index - 1 + images.length) % images.length;
  showImage(index);
}

// Auto play
let interval = setInterval(nextImage, 3000);

// Reinicia o intervalo após clique
function resetInterval() {
  clearInterval(interval);
  interval = setInterval(nextImage, 3000);
}

prevBtn.addEventListener("click", () => {
  prevImage();
  resetInterval();
});

nextBtn.addEventListener("click", () => {
  nextImage();
  resetInterval();
});
