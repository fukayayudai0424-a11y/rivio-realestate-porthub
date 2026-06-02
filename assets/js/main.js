(() => {
  const burger = document.querySelector("[data-burger]");
  const drawer = document.querySelector("[data-drawer]");

  if (burger && drawer) {
    const toggle = (open) => {
      drawer.classList.toggle("is-open", open);
      burger.classList.toggle("is-open", open);
      burger.setAttribute("aria-expanded", String(open));
      document.body.style.overflow = open ? "hidden" : "";
    };
    burger.addEventListener("click", () => toggle(!drawer.classList.contains("is-open")));
    drawer.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => toggle(false)));
  }

  const form = document.querySelector("[data-contact-form]");
  const consent = document.querySelector("[data-consent]");
  const submitButton = document.querySelector("[data-submit]");
  const message = document.querySelector("[data-message]");

  if (form && consent && submitButton && message) {
    const sync = () => { submitButton.disabled = !consent.checked; };
    sync();
    consent.addEventListener("change", sync);
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!consent.checked) {
        message.className = "form-message is-error";
        message.textContent = "プライバシーポリシーへの同意が必要です。";
        return;
      }
      const invalid = Array.from(form.querySelectorAll("[required]")).some((i) => !i.value.trim());
      if (invalid) {
        message.className = "form-message is-error";
        message.textContent = "必須項目を入力してください。";
        return;
      }
      submitButton.disabled = true;
      message.className = "form-message";
      message.textContent = "送信中です...";
      setTimeout(() => {
        message.className = "form-message is-success";
        message.textContent = "送信ありがとうございました（仮サイトのため実送信はしていません）。";
        form.reset();
        sync();
        submitButton.disabled = false;
      }, 850);
    });
  }
})();
