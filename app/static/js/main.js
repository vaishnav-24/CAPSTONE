setTimeout(() => {
  document.querySelectorAll(".alert").forEach((el) => {
    if (el.classList.contains("alert-success") || el.classList.contains("alert-info")) {
      el.classList.remove("show");
    }
  });
}, 4000);
