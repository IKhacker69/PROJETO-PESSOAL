document.addEventListener("DOMContentLoaded", () => {
  const arrow = document.getElementById("scroll-arrow");
  const icon = document.getElementById("arrow-icon");

  arrow.addEventListener("click", () => {
    if (window.scrollY + window.innerHeight >= document.body.scrollHeight - 10) {
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else {
      const sections = Array.from(document.querySelectorAll("section"));
      const nextSection = sections.find(sec => sec.getBoundingClientRect().top > 10);
      if (nextSection) {
        window.scrollTo({
          top: window.scrollY + nextSection.getBoundingClientRect().top,
          behavior: "smooth"
        });
      }
    }
  });

  window.addEventListener("scroll", () => {
    const nearBottom = window.innerHeight + window.scrollY >= document.body.scrollHeight - 10;
    if (nearBottom) {
      icon.style.transform = "rotate(180deg)";
    } else {
      icon.style.transform = "rotate(0deg)";
    }
  });
});
