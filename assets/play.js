// Quick Play (/play): unlimited 10-question airport code rounds, by region.
// Uses the same airport list as Daily Departure (assets/daily-airports.js).
// Best scores are saved in this browser only (localStorage).
(function () {
  var root = document.getElementById("play");
  var AIRPORTS = window.DAILY_AIRPORTS;
  if (!root || !AIRPORTS) return;

  var ROUND = 10;
  var STORE_KEY = "ag1-play-v1";
  var REGIONS = {
    eu: "Europe",
    am: "Americas",
    ap: "Asia & Pacific",
    me: "Middle East & Africa",
    all: "World mix"
  };

  function $(id) { return document.getElementById(id); }
  var el = {
    pick: $("play-pick"), round: $("play-round"), end: $("play-end"),
    region: $("play-region"), step: $("play-step"), score: $("play-score"),
    pips: $("play-pips"), flaps: $("play-flaps"), options: $("play-options"),
    feedback: $("play-feedback"), next: $("play-next"),
    final: $("play-final"), verdict: $("play-verdict"), best: $("play-best"),
    missedWrap: $("play-missed-wrap"), missed: $("play-missed"),
    again: $("play-again"), change: $("play-change")
  };

  function shuffle(list) {
    for (var i = list.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = list[i]; list[i] = list[j]; list[j] = t;
    }
    return list;
  }

  function loadBest() {
    try { return JSON.parse(localStorage.getItem(STORE_KEY)) || {}; } catch (e) { return {}; }
  }
  function saveBest(b) {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(b)); } catch (e) {}
  }
  var best = loadBest();

  // Show best scores on the region buttons.
  function renderPicker() {
    Object.keys(REGIONS).forEach(function (r) {
      var span = root.querySelector('[data-best="' + r + '"]');
      if (span) span.textContent = best[r] !== undefined ? "Best " + best[r] + "/" + ROUND : "Not played yet";
    });
  }

  var region, questions, current, picks;

  function buildRound(r) {
    var pool = AIRPORTS.filter(function (a) { return r === "all" || a[3] === r; });
    return shuffle(pool.slice()).slice(0, ROUND).map(function (right) {
      // Wrong answers come from the same region so they're believable.
      var same = AIRPORTS.filter(function (a) { return a[3] === right[3] && a[0] !== right[0]; });
      var wrong = shuffle(same).slice(0, 3);
      return {
        code: right[0], name: right[1], country: right[2],
        options: shuffle([right].concat(wrong)).map(function (a) { return a[1]; })
      };
    });
  }

  function show(which) {
    el.pick.hidden = which !== "pick";
    el.round.hidden = which !== "round";
    el.end.hidden = which !== "end";
  }

  function start(r) {
    region = r;
    questions = buildRound(r);
    current = 0;
    picks = [];
    el.region.textContent = REGIONS[r];
    show("round");
    renderQuestion();
    var first = el.options.querySelector("button");
    if (first) first.focus();
  }

  function score() {
    return questions.filter(function (q, i) { return picks[i] === q.name; }).length;
  }

  function renderQuestion() {
    var q = questions[current];
    var pick = picks[current];
    var answered = pick !== undefined;
    el.step.textContent = "Question " + (current + 1) + " of " + ROUND;
    el.score.textContent = score();

    el.pips.innerHTML = "";
    questions.forEach(function (qq, i) {
      var pip = document.createElement("span");
      pip.className = "daily-pip";
      if (picks[i] !== undefined) pip.classList.add(picks[i] === qq.name ? "is-right" : "is-wrong");
      else if (i === current) pip.classList.add("is-current");
      el.pips.appendChild(pip);
    });

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
      el.feedback.textContent = (pick === q.name ? "Correct! " : "Not quite. ") +
        q.code + " is " + q.name + ", " + q.country + ".";
      el.next.textContent = current === ROUND - 1 ? "See my score" : "Next question";
    }
  }

  function answer(name) {
    if (picks[current] !== undefined) return;
    picks[current] = name;
    renderQuestion();
    el.next.focus();
  }

  function verdict(s) {
    if (s === ROUND) return "Perfect round. You could work the departures board.";
    if (s >= 8) return "Frequent flyer. Just a couple to brush up on.";
    if (s >= 5) return "Not bad at all. Another round?";
    return "Everyone starts somewhere. The codes below are worth a look.";
  }

  function finish() {
    var s = score();
    var isBest = best[region] === undefined || s > best[region];
    if (isBest) { best[region] = s; saveBest(best); }
    el.final.textContent = s + "/" + ROUND;
    el.verdict.textContent = verdict(s);
    el.best.textContent = isBest ? "New best for " + REGIONS[region] + "!" :
      "Your best for " + REGIONS[region] + ": " + best[region] + "/" + ROUND;

    el.missed.innerHTML = "";
    var missed = questions.filter(function (q, i) { return picks[i] !== q.name; });
    missed.forEach(function (q) {
      var li = document.createElement("li");
      var code = document.createElement("a");
      code.href = "/airports/" + q.code.toLowerCase();
      code.textContent = q.code;
      li.appendChild(code);
      li.appendChild(document.createTextNode(q.name + ", " + q.country));
      el.missed.appendChild(li);
    });
    el.missedWrap.hidden = missed.length === 0;
    show("end");
    el.again.focus();
  }

  el.next.addEventListener("click", function () {
    if (current < ROUND - 1) {
      current += 1;
      renderQuestion();
      el.options.querySelector("button").focus();
    } else {
      finish();
    }
  });
  el.again.addEventListener("click", function () { start(region); });
  el.change.addEventListener("click", function () { renderPicker(); show("pick"); });
  Array.prototype.forEach.call(root.querySelectorAll("[data-region]"), function (b) {
    b.addEventListener("click", function () { start(b.getAttribute("data-region")); });
  });

  renderPicker();
  show("pick");
  root.classList.add("is-ready");
})();
