// Home page: the Daily Departure board in the hero, and the airport code search box.
(function () {
  var D = window.AG1Daily;
  var board = document.getElementById("home-board");
  if (D && board) {
    var today = D.dayNumber(new Date());
    var puzzle = D.puzzleFor(today);
    var mine = null;
    try {
      var saved = JSON.parse(localStorage.getItem(D.storeKey));
      if (saved && saved.days) mine = saved.days[today];
      if (mine && mine.codes !== puzzle.map(function (q) { return q.code; }).join(",")) mine = null;
    } catch (e) {}
    var done = !!(mine && mine.done);
    var picks = (mine && mine.picks) || [];

    document.getElementById("home-board-num").textContent = "#" + today;
    var rows = document.getElementById("home-board-rows");
    rows.innerHTML = "";
    puzzle.forEach(function (q, i) {
      var li = document.createElement("li");
      var flt = document.createElement("span");
      flt.className = "board-flt";
      flt.textContent = "AG" + (i + 1);
      var code = document.createElement("span");
      code.className = "board-code";
      // Codes stay hidden until you've played today, so the board never spoils the puzzle.
      (done ? q.code : "???").split("").forEach(function (ch) {
        var f = document.createElement("span");
        f.textContent = ch;
        code.appendChild(f);
      });
      var status = document.createElement("span");
      status.className = "board-status";
      if (done) {
        var ok = picks[i] === q.name;
        status.textContent = ok ? "LANDED" : "DIVERTED";
        status.classList.add(ok ? "is-right" : "is-wrong");
      } else if (i < picks.length) {
        status.textContent = "DEPARTED";
      } else if (i === picks.length) {
        status.textContent = "BOARDING";
        status.classList.add("is-now");
      } else {
        status.textContent = "SCHEDULED";
      }
      li.appendChild(flt);
      li.appendChild(code);
      li.appendChild(status);
      rows.appendChild(li);
    });

    var foot = document.getElementById("home-board-foot");
    var cta = document.getElementById("home-board-cta");
    if (done) {
      var score = puzzle.filter(function (q, i) { return picks[i] === q.name; }).length;
      var left = D.secondsToUkMidnight(new Date());
      foot.textContent = "You scored " + score + "/5 today. Next departure in " +
        Math.floor(left / 3600) + "h " + Math.floor((left % 3600) / 60) + "m.";
      cta.textContent = "See my boarding pass";
    } else if (picks.length) {
      foot.textContent = "You're part way through today's puzzle.";
      cta.textContent = "Carry on";
    }
  }

  // Search: a known code goes straight to its page, anything else to the filtered A–Z.
  var form = document.getElementById("home-search");
  if (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var q = form.querySelector("input").value.trim();
      if (!q) return;
      var codes = (window.DAILY_AIRPORTS || []).map(function (a) { return a[0]; });
      if (/^[a-z]{3}$/i.test(q) && codes.indexOf(q.toUpperCase()) !== -1) {
        location.href = "/airports/" + q.toLowerCase();
      } else {
        location.href = "/airports/?q=" + encodeURIComponent(q);
      }
    });
  }
})();
