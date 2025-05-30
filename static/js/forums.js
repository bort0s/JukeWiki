document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".forum-link").forEach(link => {
    link.addEventListener("click", () => {
      const id = link.dataset.id;
      fetch(`/forums/${id}/`, {
        headers: { "X-Requested-With": "XMLHttpRequest" }
      })
      .then(r => r.text())
      .then(html => {
        document.getElementById("forum-detail").innerHTML = html;
        attachCommentForm();
        attachDeleteForm();
        attachDeleteComment();
      });
    });
  });

  attachCommentForm();
  attachDeleteForm();
  attachDeleteComment();
});

function attachCommentForm() {
  const form = document.querySelector(".forum-comment-form");
  if (!form) return;

  // RISPOSTA
  document.querySelectorAll(".rispondi-button").forEach(btn => {
    btn.addEventListener("click", () => {
      document.getElementById("risposta-a-input").value = btn.dataset.id;

      const username = btn.dataset.author;
      const textarea = form.querySelector("textarea");
      if (textarea && username) {
        textarea.value = `@${username} `;
        textarea.focus();
      }

      window.scrollTo({ top: form.offsetTop - 80, behavior: 'smooth' });
    });
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    const forumId = this.dataset.forumId;
    const formData = new FormData(this);

    fetch(`/forums/${forumId}/`, {
      method: "POST",
      headers: { "X-Requested-With": "XMLHttpRequest" },
      body: formData
    })
    .then(r => r.text())
    .then(html => {
      document.getElementById("forum-detail").innerHTML = html;
      attachCommentForm();
      attachDeleteForm();
      attachDeleteComment();
    });
  });
}

function attachDeleteForm() {
  const delForm = document.getElementById("delete-forum-form");
  if (!delForm) return;

  delForm.addEventListener("submit", function (e) {
    e.preventDefault();
    if (confirm("Vuoi davvero eliminare questo forum?")) {
      fetch(this.action, {
        method: 'POST',
        headers: {
          'X-CSRFToken': this.querySelector('[name=csrfmiddlewaretoken]').value
        }
      }).then(r => {
        if (r.ok) location.reload();
      });
    }
  });
}

function attachDeleteComment() {
  document.querySelectorAll(".form-elimina-commento").forEach(form => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (confirm("Vuoi davvero eliminare questo commento?")) {
        fetch(this.action, {
          method: "POST",
          headers: {
            "X-CSRFToken": this.querySelector('[name=csrfmiddlewaretoken]').value,
            "X-Requested-With": "XMLHttpRequest"
          }
        })
        .then(r => r.text())
        .then(html => {
          document.getElementById("forum-detail").innerHTML = html;
          attachCommentForm();
          attachDeleteForm();
          attachDeleteComment();
        });
      }
    });
  });
}
