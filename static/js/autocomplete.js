document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("id_brano");
  if (!input) return;

  const suggestionBox = document.createElement("ul");
  suggestionBox.style.position = "absolute";
  suggestionBox.style.background = "#111";
  suggestionBox.style.border = "1px solid #555";
  suggestionBox.style.zIndex = "1000";
  suggestionBox.style.listStyle = "none";
  suggestionBox.style.padding = "0";
  suggestionBox.style.margin = "0";
  suggestionBox.style.width = input.offsetWidth + "px";
  suggestionBox.style.display = "none";
  suggestionBox.style.color = "#fff";
  suggestionBox.style.fontFamily = "monospace";
  document.body.appendChild(suggestionBox);

  input.addEventListener("input", function () {
    const query = input.value;
    if (query.length < 1) {
      suggestionBox.style.display = "none";
      return;
    }

    fetch(`/ajax/suggerisci-brani/?term=${encodeURIComponent(query)}`)
      .then(res => res.json())
      .then(data => {
        suggestionBox.innerHTML = "";
        data.forEach(item => {
          const li = document.createElement("li");
          li.textContent = item;
          li.style.padding = "0.4rem 0.7rem";
          li.style.cursor = "pointer";
          li.addEventListener("click", function () {
            input.value = item;
            suggestionBox.style.display = "none";
          });
          suggestionBox.appendChild(li);
        });
        const rect = input.getBoundingClientRect();
        suggestionBox.style.top = window.scrollY + rect.bottom + "px";
        suggestionBox.style.left = window.scrollX + rect.left + "px";
        suggestionBox.style.width = rect.width + "px";
        suggestionBox.style.display = "block";
      });
  });

  document.addEventListener("click", function (e) {
    if (!suggestionBox.contains(e.target) && e.target !== input) {
      suggestionBox.style.display = "none";
    }
  });
});