function handleTabClick(tab) {
  document.querySelectorAll('[role=tab]').forEach(el => el.setAttribute('aria-selected', 'false'));
  tab.setAttribute('aria-selected', 'true');
  const section = document.getElementById('resource-section');
  if (section) {
    section.setAttribute('aria-labelledby', tab.id);
  }
}
