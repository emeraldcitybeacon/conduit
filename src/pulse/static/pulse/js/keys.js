// Keyboard shortcuts and form submission helpers for Pulse resource editor.

function flattenErrors(obj, prefix) {
  const res = {};
  for (const key in obj) {
    if (!Object.prototype.hasOwnProperty.call(obj, key)) continue;
    const val = obj[key];
    const path = prefix ? prefix + '.' + key : key;
    if (Array.isArray(val)) {
      res[path] = val.join(', ');
    } else if (val && typeof val === 'object') {
      Object.assign(res, flattenErrors(val, path));
    }
  }
  return res;
}

let goPrefix = false;

document.addEventListener('keydown', function (e) {
  const tag = e.target.tagName.toLowerCase();
  if (tag === 'input' || tag === 'textarea') return;

  const key = e.key.toLowerCase();

  if ((e.metaKey || e.ctrlKey) && key === 's') {
    e.preventDefault();
    const modal = document.getElementById('diff-modal');
    if (modal && typeof modal.showModal === 'function') {
      modal.showModal();
    }
    return;
  }

  if ((e.metaKey || e.ctrlKey) && key === 'k') {
    e.preventDefault();
    const picker = document.getElementById('worklist-picker');
    if (picker && typeof picker.showModal === 'function') {
      picker.showModal();
    }
    return;
  }

  if (key === '?') {
    e.preventDefault();
    const overlay = document.getElementById('key-overlay');
    if (overlay && typeof overlay.showModal === 'function') {
      overlay.showModal();
    }
    return;
  }

  if (goPrefix) {
    if (key === 'o' || key === 'l') {
      e.preventDefault();
      const nav = document.getElementById('siblings-nav');
      if (nav) {
        const target = key === 'o' ? nav.dataset.firstOrg : nav.dataset.firstLoc;
        if (target) {
          window.location.href = '/pulse/r/' + target + '/';
        }
      }
    }
    goPrefix = false;
    return;
  }

  if (key === 'g') {
    goPrefix = true;
    setTimeout(function () { goPrefix = false; }, 1000);
    return;
  }

  const nav = document.getElementById('siblings-nav');
  if (!nav) return;

  if (key === '[' || key === 'k') {
    const prev = nav.dataset.prev;
    if (prev) {
      window.location.href = '/pulse/r/' + prev + '/';
    }
  } else if (key === ']' || key === 'j') {
    const next = nav.dataset.next;
    if (next) {
      window.location.href = '/pulse/r/' + next + '/';
    }
  }
});

document.addEventListener('DOMContentLoaded', function () {
  const confirm = document.getElementById('diff-modal-confirm');
  if (confirm) {
    confirm.addEventListener('click', function () {
      document.querySelectorAll('form[data-resource-form]').forEach(function (form) {
        if (form.requestSubmit) {
          form.requestSubmit();
        } else {
          form.submit();
        }
      });
      const modal = document.getElementById('diff-modal');
      if (modal) {
        modal.close();
      }
    });
  }
});

document.body.addEventListener('htmx:responseError', function (evt) {
  let data;
  try {
    data = JSON.parse(evt.detail.xhr.responseText);
  } catch (err) {
    return;
  }
  // Update validation errors
  const flat = flattenErrors(data);
  for (const path in flat) {
    const el = document.querySelector('.validator[data-field="' + path + '"]');
    if (el) {
      el.textContent = '';
      const span = document.createElement('span');
      span.className = 'label-text-alt text-error';
      span.textContent = flat[path];
      el.appendChild(span);
    }
  }
  // Insert merge chips for current server values on version mismatches
  if (data.current) {
    for (const path in data.current) {
      const container = document.querySelector('.merge-chip-container[data-field="' + path + '"]');
      if (container) {
        const url = '/pulse/c/merge_chip/?path=' + encodeURIComponent(path) + '&current=' + encodeURIComponent(safeStringForUrl(data.current[path]));
        htmx.ajax('GET', url, {target: container, swap: 'innerHTML'});
      }
    }
  }
});

// Delegate click handling for merge chips to apply server values
document.body.addEventListener('click', function (evt) {
  const chip = evt.target.closest('.merge-chip');
  if (!chip) return;
  const field = chip.dataset.field;
  const value = chip.dataset.value;
  const input = document.querySelector('[name="' + CSS.escape(field) + '"]');
  if (input) {
    input.value = value;
    input.dispatchEvent(new Event('input', { bubbles: true }));
  }
  chip.remove();
});
