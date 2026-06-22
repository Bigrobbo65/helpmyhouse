// Help My House — front-end interactions
(function () {
  // Footer year
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();

  // Mobile nav toggle
  var toggle = document.getElementById('navToggle');
  var nav = document.getElementById('nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }
})();

// Form handling (front-end demo — wire up to email/backend before going live)
window.HMH = {
  submitForm: function (e, type) {
    e.preventDefault();
    var form = e.target;
    var data = Object.fromEntries(new FormData(form).entries());
    console.log('[Help My House] ' + type + ' submission:', data);

    if (type === 'contact') {
      var note = document.getElementById('formNote');
      if (note) {
        note.textContent = 'Thanks ' + (data.name || '') + '! Your request has been received — we\'ll be in touch shortly.';
        note.classList.add('ok');
      }
    } else {
      alert('Thanks ' + (data.name || '') + '! We\'ll call you back shortly.');
    }
    form.reset();
    return false;
  }
};
