// Daily Departure: one airport-code puzzle a day, the same for everyone.
// The day is the calendar date in the UK (Europe/London), so it changes at UK midnight.
// Everything is worked out in the browser from the date: no server, no accounts.
// Progress and streaks are saved in this browser only (localStorage).
(function () {
  if (!window.DAILY_AIRPORTS) return;
  // Daily puzzles only use the first 140 airports in the list, so adding more
  // airports later (for the airport pages and Quick Play) never changes past or
  // future Daily Departure puzzles.
  var DAILY_POOL = 140;
  var AIRPORTS = window.DAILY_AIRPORTS.slice(0, DAILY_POOL);

  var PER_DAY = 5;
  var LAUNCH_UTC = Date.UTC(2026, 10, 4); // 4 Nov 2026 is Daily Departure #1
  var STORE_KEY = "ag1-daily-v1";
  var SITE_URL = "amateurgames1.com/daily";

  // ---------- Dates (UK time) ----------
  function ukParts(date) {
    var parts = {};
    new Intl.DateTimeFormat("en-GB", {
      timeZone: "Europe/London", year: "numeric", month: "2-digit", day: "2-digit",
      hour: "2-digit", minute: "2-digit", second: "2-digit", hourCycle: "h23"
    }).formatToParts(date).forEach(function (p) { parts[p.type] = parseInt(p.value, 10); });
    return parts;
  }
  function dayNumber(date) {
    var p = ukParts(date);
    var utc = Date.UTC(p.year, p.month - 1, p.day);
    return Math.round((utc - LAUNCH_UTC) / 86400000) + 1;
  }
  function secondsToUkMidnight(date) {
    var p = ukParts(date);
    return 86400 - (p.hour * 3600 + p.minute * 60 + p.second);
  }

  // ---------- Seeded random (same results for everyone) ----------
  function rng(seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6d2b79f5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function shuffle(list, rand) {
    for (var i = list.length - 1; i > 0; i--) {
      var j = Math.floor(rand() * (i + 1));
      var t = list[i]; list[i] = list[j]; list[j] = t;
    }
    return list;
  }

  // Each "cycle" shuffles the whole list once and deals it out five a day,
  // so no airport repeats until every airport has had its turn.
  function puzzleFor(n) {
    var daysPerCycle = Math.floor(AIRPORTS.length / PER_DAY);
    var cycle = Math.floor((n - 1) / daysPerCycle);
    var pos = (n - 1) % daysPerCycle;
    var order = shuffle(AIRPORTS.map(function (_, i) { return i; }), rng(1000 + cycle));
    return order.slice(pos * PER_DAY, pos * PER_DAY + PER_DAY).map(function (idx, q) {
      var right = AIRPORTS[idx];
      var rand = rng(n * 97 + q * 13 + 7);
      var sameRegion = AIRPORTS.filter(function (a) { return a[3] === right[3] && a[0] !== right[0]; });
      var wrong = shuffle(sameRegion, rand).slice(0, 3);
      return {
        code: right[0], name: right[1], country: right[2],
        options: shuffle([right].concat(wrong), rand).map(function (a) { return a[1]; })
      };
    });
  }

  // Shared with the home page board (assets/home.js).
  window.AG1Daily = { dayNumber: dayNumber, puzzleFor: puzzleFor, storeKey: STORE_KEY, secondsToUkMidnight: secondsToUkMidnight };

  var root = document.getElementById("daily");
  if (!root) return;

  // ---------- Saved progress ----------
  function load() {
    try {
      var s = JSON.parse(localStorage.getItem(STORE_KEY));
      if (s && typeof s === "object") return s;
    } catch (e) {}
    return { streak: 0, best: 0, lastDay: 0, days: {} };
  }
  function save(s) {
    // Keep the last 60 days of results so storage stays tiny.
    var keys = Object.keys(s.days).map(Number).sort(function (a, b) { return b - a; });
    keys.slice(60).forEach(function (k) { delete s.days[k]; });
    try { localStorage.setItem(STORE_KEY, JSON.stringify(s)); } catch (e) {}
  }

  // ---------- Elements ----------
  function $(id) { return document.getElementById(id); }
  var el = {
    num: $("daily-num"), date: $("daily-date"), streak: $("daily-streak"),
    pips: $("daily-pips"), flaps: $("daily-flaps"), step: $("daily-step"),
    options: $("daily-options"), feedback: $("daily-feedback"), next: $("daily-next"),
    play: $("daily-play"), result: $("daily-result"), score: $("daily-score"),
    passNum: $("daily-pass-num"), passStreak: $("daily-pass-streak"), grid: $("daily-grid"),
    share: $("daily-share"), shareStatus: $("daily-share-status"), countdown: $("daily-countdown")
  };

  var today = dayNumber(new Date());
  var puzzle = puzzleFor(today);
  var codes = puzzle.map(function (q) { return q.code; }).join(",");
  var state = load();
  var mine = state.days[today];
  if (!mine || mine.codes !== codes) mine = state.days[today] = { codes: codes, picks: [] };
  var current = Math.min(mine.picks.length, PER_DAY - 1);

  el.num.textContent = "#" + today;
  el.passNum.textContent = "#" + today;
  el.date.textContent = new Intl.DateTimeFormat("en-GB", {
    timeZone: "Europe/London", weekday: "short", day: "numeric", month: "short"
  }).format(new Date());

  function liveStreak() {
    // A streak only counts if you played yesterday or today.
    return state.lastDay >= today - 1 ? state.streak : 0;
  }
  function isRight(q, pick) { return pick === q.name; }
  function score() {
    return puzzle.filter(function (q, i) { return isRight(q, mine.picks[i]); }).length;
  }

  function renderPips() {
    el.pips.innerHTML = "";
    puzzle.forEach(function (q, i) {
      var pip = document.createElement("span");
      pip.className = "daily-pip";
      var pick = mine.picks[i];
      if (pick !== undefined) pip.classList.add(isRight(q, pick) ? "is-right" : "is-wrong");
      else if (i === current) pip.classList.add("is-current");
      el.pips.appendChild(pip);
    });
  }

  function renderQuestion() {
    var q = puzzle[current];
    var pick = mine.picks[current];
    var answered = pick !== undefined;
    el.step.textContent = "Flight " + (current + 1) + " of " + PER_DAY;
    el.streak.textContent = liveStreak();
    el.flaps.innerHTML = "";
    el.flaps.setAttribute("aria-label", "Airport code " + q.code.split("").join(" "));
    q.code.split("").forEach(function (ch) {
      var f = document.createElement("span");
      f.className = "flap";
      f.setAttribute("aria-hidden", "true");
      f.textContent = ch;
      el.flaps.appendChild(f);
    });
    el.options.innerHTML = "";
    q.options.forEach(function (name, k) {
      var b = document.createElement("button");
      b.type = "button";
      b.className = "quiz-option";
      b.innerHTML = "<span>" + "ABCD"[k] + "</span>";
      b.appendChild(document.createTextNode(name));
      if (answered) {
        b.disabled = true;
        if (name === q.name) b.classList.add("is-right");
        else if (name === pick) b.classList.add("is-wrong");
      }
      b.addEventListener("click", function () { answer(name); });
      el.options.appendChild(b);
    });
    el.feedback.hidden = !answered;
    el.next.hidden = !answered;
    if (answered) {
      el.feedback.textContent = (isRight(q, pick) ? "Correct! " : "Not quite. ") +
        q.code + " is " + q.name + ", " + q.country + ".";
      el.next.textContent = current === PER_DAY - 1 ? "See my boarding pass" : "Next flight";
    }
    renderPips();
  }

  function answer(name) {
    if (mine.picks[current] !== undefined) return;
    mine.picks[current] = name;
    if (mine.picks.length === PER_DAY) finish();
    save(state);
    renderQuestion();
    el.next.focus();
  }

  function finish() {
    if (mine.done) return;
    mine.done = true;
    mine.score = score();
    if (state.lastDay === today - 1) state.streak += 1;
    else if (state.lastDay !== today) state.streak = 1;
    state.lastDay = today;
    state.best = Math.max(state.best || 0, state.streak);
  }

  function showResult() {
    el.play.hidden = true;
    el.result.hidden = false;
    el.score.textContent = score() + "/" + PER_DAY;
    var s = liveStreak();
    el.passStreak.textContent = s + (s === 1 ? " day" : " days");
    el.streak.textContent = s;
    el.grid.innerHTML = "";
    puzzle.forEach(function (q, i) {
      var ok = isRight(q, mine.picks[i]);
      var cell = document.createElement("li");
      cell.className = ok ? "is-right" : "is-wrong";
      cell.innerHTML = '<b aria-hidden="true">' + (ok ? "✓" : "✗") + "</b>";
      var code = document.createElement("span");
      code.textContent = q.code;
      cell.appendChild(code);
      cell.setAttribute("aria-label", q.code + " " + (ok ? "right" : "wrong") + ", " + q.name);
      el.grid.appendChild(cell);
    });
    tick();
    el.result.focus();
  }

  el.next.addEventListener("click", function () {
    if (current < PER_DAY - 1) { current += 1; renderQuestion(); el.options.querySelector("button").focus(); }
    else showResult();
  });

  el.share.addEventListener("click", function () {
    var squares = puzzle.map(function (q, i) { return isRight(q, mine.picks[i]) ? "🟩" : "🟥"; }).join("");
    var text = "Daily Departure #" + today + " " + score() + "/" + PER_DAY + "\n" + squares +
      "\nStreak: " + liveStreak() + "\n" + SITE_URL;
    function copied() { el.shareStatus.textContent = "Copied! Paste it anywhere."; }
    if (navigator.share) {
      navigator.share({ text: text }).catch(function () {});
    } else if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(copied, function () { el.shareStatus.textContent = text; });
    } else {
      el.shareStatus.textContent = text;
    }
  });

  function tick() {
    var left = secondsToUkMidnight(new Date());
    var h = Math.floor(left / 3600), m = Math.floor((left % 3600) / 60);
    el.countdown.textContent = h + "h " + (m < 10 ? "0" : "") + m + "m";
  }
  setInterval(function () {
    if (dayNumber(new Date()) !== today) { location.reload(); return; }
    if (!el.result.hidden) tick();
  }, 30000);

  root.classList.add("is-ready");
  if (mine.done) showResult();
  else renderQuestion();

  // Exposed for testing in the browser console only.
  window.__daily = { dayNumber: dayNumber, puzzleFor: puzzleFor };
})();
