// Sample question on the home page. The first question (LHR) is in the HTML,
// so the page still shows a question if this script doesn't run.
(function () {
  var quiz = document.getElementById("quiz");
  if (!quiz) return;

  var QUESTIONS = [
    ["JFK", "New York JFK", ["Newark Liberty", "Boston Logan", "Washington Dulles"]],
    ["HND", "Tokyo Haneda", ["Tokyo Narita", "Osaka Kansai", "Seoul Incheon"]],
    ["CDG", "Paris Charles de Gaulle", ["Paris Orly", "Brussels", "Lyon"]],
    ["ORD", "Chicago O’Hare", ["Chicago Midway", "Detroit", "Denver"]],
    ["YYZ", "Toronto Pearson", ["Vancouver", "Montréal Trudeau", "Calgary"]],
    ["FCO", "Rome Fiumicino", ["Rome Ciampino", "Milan Malpensa", "Naples"]],
    ["MUC", "Munich", ["Frankfurt", "Berlin Brandenburg", "Zurich"]],
    ["SIN", "Singapore Changi", ["Kuala Lumpur", "Bangkok Suvarnabhumi", "Jakarta"]],
    ["GRU", "São Paulo Guarulhos", ["Rio de Janeiro Galeão", "Buenos Aires Ezeiza", "Lima"]],
    ["LAX", "Los Angeles", ["San Francisco", "Las Vegas", "San Diego"]],
    ["AMS", "Amsterdam Schiphol", ["Rotterdam", "Brussels", "Copenhagen"]],
    ["DXB", "Dubai", ["Abu Dhabi", "Doha", "Muscat"]]
  ];

  var codeEl = document.getElementById("quiz-code");
  var optionsEl = document.getElementById("quiz-options");
  var resultEl = document.getElementById("quiz-result");
  var feedbackEl = document.getElementById("quiz-feedback");
  var hintEl = document.getElementById("quiz-hint");
  var numEl = document.getElementById("quiz-num");
  var scoreEl = document.getElementById("quiz-score");
  var nextBtn = document.getElementById("quiz-next");

  var order = shuffle(QUESTIONS.slice());
  var index = -1;
  var asked = 1;
  var score = 0;
  var answered = false;

  function shuffle(list) {
    for (var i = list.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = list[i]; list[i] = list[j]; list[j] = t;
    }
    return list;
  }

  function bindOptions() {
    var buttons = optionsEl.querySelectorAll(".quiz-option");
    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () { answer(btn, buttons); });
    });
  }

  function answer(btn, buttons) {
    if (answered) return;
    answered = true;
    var right = btn.hasAttribute("data-right");
    var rightName = "";
    buttons.forEach(function (b) {
      b.disabled = true;
      if (b.hasAttribute("data-right")) {
        b.classList.add("is-right");
        rightName = b.lastChild.textContent;
      }
    });
    if (right) {
      score++;
      scoreEl.textContent = score;
      feedbackEl.textContent = "Correct! There are 999 more in the app.";
    } else {
      btn.classList.add("is-wrong");
      feedbackEl.textContent = "So close. It’s " + rightName + ".";
    }
    hintEl.hidden = true;
    resultEl.hidden = false;
    nextBtn.focus();
  }

  function render(q) {
    codeEl.innerHTML = "";
    q[0].split("").forEach(function (ch) {
      var flap = document.createElement("span");
      flap.className = "flap";
      flap.textContent = ch;
      codeEl.appendChild(flap);
    });
    var names = shuffle([q[1]].concat(q[2]));
    optionsEl.innerHTML = "";
    names.forEach(function (name, i) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "quiz-option";
      if (name === q[1]) btn.setAttribute("data-right", "");
      var letter = document.createElement("span");
      letter.textContent = "ABCD"[i];
      btn.appendChild(letter);
      btn.appendChild(document.createTextNode(name));
      optionsEl.appendChild(btn);
    });
    bindOptions();
  }

  nextBtn.addEventListener("click", function () {
    index = (index + 1) % order.length;
    asked++;
    numEl.textContent = asked;
    answered = false;
    resultEl.hidden = true;
    hintEl.hidden = false;
    render(order[index]);
    optionsEl.querySelector(".quiz-option").focus();
  });

  bindOptions();
})();
