const themeToggle = document.getElementById("theme-toggle");
const htmlEl = document.documentElement;
const content = document.getElementById("content");

themeToggle.onclick = () => {
  const current = htmlEl.getAttribute("data-theme");
  htmlEl.setAttribute("data-theme", current === "dark" ? "light" : "dark");
  themeToggle.textContent = current === "dark" ? "🌙" : "☀️";
};

// function loadPage(page) {
//   fetch(`html/${page}.html`)
//     .then(res => res.text())
//     .then(html => {
//       content.innerHTML = html;

//       // Load JS riêng nếu có
//       if (page === "chat") import("../html/");
//       if (page === "upload") import("./upload.js");
//       if (page === "settings") import("./settings.js");
//     })
//     .catch(err => {
//       content.innerHTML = `<p>❌ Không thể tải trang "${page}"</p>`;
//       console.error(err);
//     });
// }

// Mặc định tải trang chat khi khởi động
window.onload = () => {
  // loadPage("chat");
};