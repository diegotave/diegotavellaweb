(function () {
  var TC_KEY    = 'gl_tc_t0';
  var STATE_KEY = 'gl_state';

  if (!sessionStorage.getItem(TC_KEY)) {
    sessionStorage.setItem(TC_KEY, Date.now());
  }
  var t0Abs = parseInt(sessionStorage.getItem(TC_KEY));
  var state = sessionStorage.getItem(STATE_KEY) || '0';

  var css = document.createElement('style');
  css.textContent =
    '.gl{position:fixed;font-family:"Courier New",Courier,monospace;' +
    'font-size:13px;line-height:1.6;letter-spacing:0.04em;' +
    'color:#fff;mix-blend-mode:difference;white-space:nowrap;' +
    'pointer-events:none;z-index:999999;}' +
    '#gl-tl{top:14px;left:16px;}' +
    '#gl-tr{top:14px;right:16px;text-align:right;}' +
    '#gl-br{bottom:14px;right:16px;text-align:right;}';
  document.head.appendChild(css);

  function makeEl(id) {
    var el = document.createElement('div');
    el.id = id; el.className = 'gl';
    document.body.appendChild(el);
    return el;
  }

  var tl, tr, br;
  function inject() {
    tl = makeEl('gl-tl');
    tr = makeEl('gl-tr');
    br = makeEl('gl-br');
    applyState(state);
    requestAnimationFrame(updateTC);
  }

  var content = {
    '0': {
      tl: 'SMPTE \xB7 COLOR REFERENCE \xB7 1920\xD71080 \xB7 29.97fps<br>DT/WEB/IDENT \xB7 SIGNAL GENERATOR v1.0',
      tr: 'IRE 100<br>FORMAT: HD \xB7 BARS+TONE'
    },
    '1': {
      tl: 'SMPTE \xB7 WELCOME \xB7 1920\xD71080 \xB7 29.97fps<br>DT/WEB/IDENT \xB7 TRANSMISSION ACTIVE',
      tr: 'IRE 100<br>SIGNAL: LIVE \xB7 /INDEX'
    }
  };

  function applyState(s) {
    var c = content[s] || content['0'];
    tl.innerHTML = c.tl;
    tr.innerHTML = c.tr;
  }

  function updateTC() {
    var e  = Date.now() - t0Abs;
    var tf = Math.floor(e * 30 / 1000);
    var ff = String(tf % 30).padStart(2, '0');
    var s  = Math.floor(tf / 30);
    var ss = String(s % 60).padStart(2, '0');
    var m  = Math.floor(s / 60);
    var mm = String(m % 60).padStart(2, '0');
    var hh = String(Math.floor(m / 60)).padStart(2, '0');
    if (br) br.textContent = 'TC ' + hh + ':' + mm + ':' + ss + ':' + ff + '  CH-A';
    requestAnimationFrame(updateTC);
  }

  if (document.body) {
    inject();
  } else {
    document.addEventListener('DOMContentLoaded', inject);
  }

  window.globalLabels = {
    setState: function (s) {
      state = s;
      sessionStorage.setItem(STATE_KEY, s);
      applyState(s);
    },
    transition: function (s) {
      var dur = 250;
      [tl, tr].forEach(function (el) {
        el.animate([{ opacity: 1 }, { opacity: 0 }], { duration: dur, fill: 'forwards' });
      });
      var newC = content[s] || content['0'];
      setTimeout(function () {
        tl.innerHTML = newC.tl;
        tr.innerHTML = newC.tr;
        [tl, tr].forEach(function (el) {
          el.animate([{ opacity: 0 }, { opacity: 1 }], { duration: dur, fill: 'forwards' });
        });
        state = s;
        sessionStorage.setItem(STATE_KEY, s);
      }, dur);
    },
    fadeOut: function () {
      [tl, tr, br].forEach(function (el) {
        el.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 400, fill: 'forwards' });
      });
    }
  };
})();
