// Airport pages: the three-question "Quick check" quiz, and the search box on /airports/,
// which also searches the full list of IATA codes.
(function () {
  // Quiz: each question's buttons are in the HTML; the right one has data-right.
  var quiz = document.querySelector("[data-ap-quiz]");
  if (quiz) {
    var total = 0, right = 0, asked = quiz.querySelectorAll(".ap-q").length;
    var scoreEl = quiz.querySelector(".ap-quiz-score");
    Array.prototype.forEach.call(quiz.querySelectorAll(".ap-q"), function (q) {
      var buttons = q.querySelectorAll("button");
      var result = q.querySelector(".ap-q-result");
      Array.prototype.forEach.call(buttons, function (b) {
        b.addEventListener("click", function () {
          var ok = b.hasAttribute("data-right");
          var answer = "";
          Array.prototype.forEach.call(buttons, function (x) {
            x.disabled = true;
            if (x.hasAttribute("data-right")) { x.classList.add("is-right"); answer = x.textContent; }
          });
          if (!ok) b.classList.add("is-wrong");
          result.textContent = ok ? "Correct!" : "Not quite. It's " + answer + ".";
          total += 1;
          if (ok) right += 1;
          if (total === asked) {
            scoreEl.innerHTML = "You got " + right + "/" + asked + ". Keep going with a round of " +
              '<a href="/play">Quick Play</a> or today’s <a href="/daily">Daily Departure</a>.';
          }
        });
      });
    });
  }

  // A-Z search: hide airports that don't match the text typed.
  var input = document.getElementById("ap-filter");
  if (input) {
    var items = document.querySelectorAll(".ap-list li");
    var regions = document.querySelectorAll(".ap-region");
    var none = document.getElementById("ap-none");
    var strip = function (s) {
      return s.normalize ? s.normalize("NFKD").replace(/[̀-ͯ]/g, "").toLowerCase() : s.toLowerCase();
    };
    input.addEventListener("input", function () {
      var q = strip(input.value.trim());
      var shown = 0;
      Array.prototype.forEach.call(items, function (li) {
        var hit = !q || li.getAttribute("data-search").indexOf(q) !== -1;
        li.hidden = !hit;
        if (hit) shown += 1;
      });
      Array.prototype.forEach.call(regions, function (r) {
        r.hidden = !r.querySelector("li:not([hidden])");
      });
      none.hidden = shown !== 0;
      more(q, shown);
    });
    // Below the airports with pages, show matches from the full list of IATA codes
    // (assets/iata-codes.json, loaded the first time someone searches).
    var moreBox = document.getElementById("ap-more");
    var moreList = document.getElementById("ap-more-list");
    var moreNote = document.getElementById("ap-more-note");
    var hasPage = {};
    Array.prototype.forEach.call(items, function (li) { hasPage[li.querySelector("b").textContent] = true; });
    var all = null, loading = null;
    var esc = function (s) {
      return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
    };
    function more(q, shown) {
      if (!moreBox) return;
      if (q.length < 2) { moreBox.hidden = true; return; }
      if (!all) {
        loading = loading || fetch("/assets/iata-codes.json").then(function (r) { return r.json(); }).then(function (d) {
          all = d.codes;
          all.forEach(function (a) { a.hay = strip(a[0] + " " + a[1] + " " + a[2] + " " + a[3]); });
        });
        loading.then(function () { more(strip(input.value.trim()), shown); }).catch(function () {});
        return;
      }
      var hits = [];
      all.forEach(function (a) {
        if (hasPage[a[0]]) return;
        var code = a[0].toLowerCase();
        var rank = code === q ? 0 : code.indexOf(q) === 0 ? 1 : a.hay.indexOf(q) !== -1 ? 2 : -1;
        if (rank >= 0) hits.push([rank, a]);
      });
      hits.sort(function (x, y) { return x[0] - y[0] || (x[1][0] < y[1][0] ? -1 : 1); });
      moreList.innerHTML = hits.slice(0, 24).map(function (h) {
        var a = h[1];
        return '<li><div class="ap-row"><b>' + a[0] + "</b><span>" + esc(a[1]) + "<small>" +
          esc([a[2], a[3]].filter(Boolean).join(", ")) + "</small></span></div></li>";
      }).join("");
      var link = '<a href="/airports/all-codes?q=' + encodeURIComponent(input.value.trim()) + '">';
      moreNote.innerHTML = hits.length > 24 ? "Showing 24 of " + hits.length + ". " + link + "See them all</a>." :
        link + "Search the full list of IATA codes</a>.";
      moreBox.hidden = hits.length === 0;
      none.hidden = shown !== 0 || hits.length !== 0;
    }

    // Searches from the home page arrive as /airports/?q=...
    var m = /[?&]q=([^&]*)/.exec(location.search);
    if (m) {
      input.value = decodeURIComponent(m[1].replace(/\+/g, " "));
      input.dispatchEvent(new Event("input"));
    }
  }
})();
