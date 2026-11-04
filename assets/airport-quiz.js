// Airport pages: the three-question "Quick check" quiz, and the search box on /airports/.
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
    });
  }
})();
