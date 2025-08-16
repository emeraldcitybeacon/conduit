document.addEventListener('htmx:afterSwap', function (e) {
  // Target: only <dialog> elements (could refine for a class e.g., '.dialog')
  if (e.target.tagName === 'DIALOG' || e.target.classList.contains('dialog')) {
    try {
      // Use dialog API if supported
      e.target.showModal();
    } catch (err) {
      // Optionally fallback or log if dialog can't be opened
      console.warn('Dialog element not ready or unsupported:', err);
    }
  }
});
