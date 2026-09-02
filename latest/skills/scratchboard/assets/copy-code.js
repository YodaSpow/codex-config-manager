(() => {
  if (!navigator.clipboard?.writeText) { document.querySelectorAll('[data-copy]').forEach((button) => button.hidden = true); return; }
  document.addEventListener('click', async (event) => {
    const button = event.target.closest('[data-copy]'); if (!button) return;
    const code = document.getElementById(button.dataset.copy); if (!code) return;
    await navigator.clipboard.writeText(code.textContent || '');
    const label = button.textContent; button.textContent = 'Copied'; setTimeout(() => { button.textContent = label; }, 1200);
  });
})();
