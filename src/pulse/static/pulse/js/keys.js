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

document.addEventListener('keydown', function (e) {
  if ((e.metaKey || e.ctrlKey) && e.key === 's') {
    e.preventDefault();
    const modal = document.getElementById('diff-modal');
    if (modal && typeof modal.showModal === 'function') {
      modal.showModal();
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
  const flat = flattenErrors(data);
  for (const path in flat) {
    const el = document.querySelector('.validator[data-field="' + path + '"]');
    if (el) {
      el.innerHTML = '<span class="label-text-alt text-error">' + flat[path] + '</span>';
    }
  }
});
