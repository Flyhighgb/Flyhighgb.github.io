// /airports/all-codes: every IATA airport code, from assets/iata-codes.json.
// Search by code, airport, city or country, or browse by first letter (#A ... #Z).
(function () {
  var root = document.getElementById("ac");
  if (!root) return;
  var input = document.getElementById("ac-q");
  var sched = document.getElementById("ac-sched");
  var list = document.getElementById("ac-list");
  var status = document.getElementById("ac-status");
  var letters = root.querySelectorAll(".ac-letter");
  var pages = {};
  root.getAttribute("data-pages").split(" ").forEach(function (c) { pages[c] = true; });
  var MAX = 300;
  var codes = [];
  var letter = "A";

  var strip = function (s) {
    return s.normalize ? s.normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase() : s.toLowerCase();
  };
  var esc = function (s) {
    return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  };
  var KIND = { H: "Heliport", W: "Seaplane base" };

  function row(a) {
    var place = [a[2], a[3]].filter(Boolean).join(", ");
    var extra = KIND[a[4][0]] ? " · " + KIND[a[4][0]] : "";
    var inner = "<b>" + a[0] + "</b><span>" + esc(a[1]) + "<small>" + esc(place) + extra + "</small></span>";
    if (pages[a[0]]) {
      return '<li><a href="/airports/' + a[0].toLowerCase() + '">' + inner + '<i class="ac-tag">Full page</i></a></li>';
    }
    return '<li><div class="ap-row">' + inner + "</div></li>";
  }

  function show(rows, label, max) {
    var shown = rows.slice(0, max);
    list.innerHTML = shown.map(row).join("");
    status.textContent = rows.length === 0 ? "No codes match " + label + ". Try a three-letter code, a city or a country." :
      rows.length + (rows.length === 1 ? " code " : " codes ") + label +
      (rows.length > max ? ". Showing the first " + max + ": type more to narrow it down." : ".");
  }

  function update() {
    var only = sched.checked;
    var pool = only ? codes.filter(function (a) { return a[4].slice(-1) !== "-"; }) : codes;
    var q = strip(input.value.trim());
    // One letter typed: same as picking that letter.
    if (/^[a-z]$/.test(q)) { letter = q.toUpperCase(); q = ""; }
    Array.prototype.forEach.call(letters, function (l) {
      l.classList.toggle("is-on", !q && l.getAttribute("data-letter") === letter);
    });
    if (!q) {
      show(pool.filter(function (a) { return a[0][0] === letter; }), "starting with " + letter, Infinity);
      return;
    }
    // Exact code first, then codes starting with the text, then everything else that matches.
    var hits = [];
    pool.forEach(function (a) {
      var rank;
      var code = a[0].toLowerCase();
      if (code === q) rank = 0;
      else if (code.indexOf(q) === 0) rank = 1;
      else if (a.hay.indexOf(q) !== -1) rank = pages[a[0]] ? 2 : 3;
      else return;
      hits.push([rank, a]);
    });
    hits.sort(function (x, y) { return x[0] - y[0] || (x[1][0] < y[1][0] ? -1 : 1); });
    show(hits.map(function (h) { return h[1]; }), "match “" + input.value.trim() + "”", MAX);
  }

  function fromHash() {
    var m = /^#([A-Za-z])$/.exec(location.hash);
    if (m) { letter = m[1].toUpperCase(); input.value = ""; }
  }

  fetch("/assets/iata-codes.json").then(function (r) { return r.json(); }).then(function (data) {
    codes = data.codes;
    codes.forEach(function (a) { a.hay = strip(a[0] + " " + a[1] + " " + a[2] + " " + a[3]); });
    fromHash();
    var m = /[?&]q=([^&]*)/.exec(location.search);
    if (m) input.value = decodeURIComponent(m[1].replace(/\+/g, " "));
    update();
  }).catch(function () {
    status.textContent = "Sorry, the code list didn't load. Check your connection and refresh the page.";
  });

  Array.prototype.forEach.call(letters, function (l) {
    l.addEventListener("click", function () {
      letter = l.getAttribute("data-letter");
      input.value = "";
      update();
    });
  });
  input.addEventListener("input", update);
  sched.addEventListener("change", update);
  window.addEventListener("hashchange", function () { fromHash(); update(); });
})();
