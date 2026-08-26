// ══════════════════════════════════════════
// PortraitQuiz — 人物小測驗（純瀏覽器 localStorage，無伺服器）
// 題目資料來自 data.js 的 window.BIBLE_QUIZZES[人物id]；
// 只有該人物的 JSON 內有 "quiz" 欄位、render.py 才會產生 #quiz-section 容器，
// 這支程式只在容器存在時才啟動，其餘頁面完全不受影響。
// 進度紀錄格式：{ [人物id]: { best: 分數, total: 題數, byCategory: {...}, updatedAt } }
// ══════════════════════════════════════════
(function (global) {
  var KEY = "portrait_quiz_v1";
  var QUESTION_SECONDS = 45;
  var CATEGORY_HINTS = {
    "文脈": "建議回頭讀一次「人物素描」與「生命軌跡」，把事件發生的時間與場景重新串一遍。",
    "關鍵字": "建議重讀「神學意義」中的原文小卡，留意關鍵字背後的意思與份量。",
    "結構": "建議重讀「生命軌跡」的時間軸，留意事件先後與轉折點怎麼串成一條線。",
    "神學主題": "建議重讀「神學意義」整段，特別是「洞見」與「預表」的部分。",
    "常見誤解": "建議重讀「性格剖析」與「神學意義」，這裡通常藏著最容易被誤讀的地方。",
    "應用": "建議重讀「鏡照今日」，把提出的問題實際套用在自己的處境裡想一遍。"
  };

  function loadAll() {
    try {
      var raw = localStorage.getItem(KEY);
      var obj = raw ? JSON.parse(raw) : {};
      return (obj && typeof obj === "object") ? obj : {};
    } catch (e) { return {}; }
  }
  function saveResult(personId, result) {
    var all = loadAll();
    var prev = all[personId];
    if (!prev || result.score > prev.best) {
      all[personId] = {
        best: result.score, total: result.total,
        byCategory: result.byCategory, updatedAt: new Date().toISOString()
      };
      try { localStorage.setItem(KEY, JSON.stringify(all)); } catch (e) {}
    }
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (m) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[m];
    });
  }

  function initQuiz() {
    var section = document.getElementById("quiz-section");
    if (!section) return;
    var personId = section.getAttribute("data-person-id");
    var questions = (global.BIBLE_QUIZZES && global.BIBLE_QUIZZES[personId]) || [];
    if (!questions.length) { section.style.display = "none"; return; }

    var startBtn = document.getElementById("quiz-start-btn");
    var descEl = document.getElementById("quiz-desc");
    var playEl = document.getElementById("quiz-play");
    var resultEl = document.getElementById("quiz-result");

    var state = { idx: 0, answers: [], timer: null, remaining: QUESTION_SECONDS };

    startBtn.addEventListener("click", function () {
      startBtn.style.display = "none";
      descEl.style.display = "none";
      state.idx = 0; state.answers = [];
      renderQuestion();
    });

    function clearTimer() {
      if (state.timer) { clearInterval(state.timer); state.timer = null; }
    }

    function renderQuestion() {
      clearTimer();
      resultEl.innerHTML = "";
      var q = questions[state.idx];
      var dots = questions.map(function (_, i) {
        var cls = i < state.idx ? "done" : (i === state.idx ? "current" : "");
        return '<div class="quiz-progress-dot ' + cls + '"></div>';
      }).join("");

      playEl.innerHTML =
        '<div class="quiz-progress-bar">' + dots + '</div>' +
        '<div class="quiz-meta-row">' +
        '<span class="quiz-q-num">第 ' + (state.idx + 1) + ' / ' + questions.length + ' 題</span>' +
        '<span class="quiz-timer" id="quiz-timer">' + QUESTION_SECONDS + ' 秒</span>' +
        '</div>' +
        '<span class="quiz-category-badge">' + esc(q.category || "") + '</span>' +
        '<div class="quiz-question">' + esc(q.question) + '</div>' +
        '<div class="quiz-options" id="quiz-options">' +
        q.options.map(function (opt, i) {
          return '<button class="quiz-option" type="button" data-i="' + i + '">' + esc(opt) + '</button>';
        }).join("") +
        '</div>' +
        '<div class="quiz-explain" id="quiz-explain"></div>' +
        '<div class="quiz-actions"><button class="quiz-btn" id="quiz-next-btn" style="display:none" type="button">' +
        (state.idx === questions.length - 1 ? "看結果" : "下一題") + '</button></div>';

      var startTime = Date.now();
      state.remaining = QUESTION_SECONDS;
      var timerEl = document.getElementById("quiz-timer");
      state.timer = setInterval(function () {
        state.remaining--;
        if (timerEl) {
          timerEl.textContent = state.remaining + " 秒";
          timerEl.classList.toggle("low", state.remaining <= 10);
        }
        if (state.remaining <= 0) {
          clearTimer();
          lockAnswer(null, Date.now() - startTime);
        }
      }, 1000);

      document.querySelectorAll(".quiz-option").forEach(function (btn) {
        btn.addEventListener("click", function () {
          clearTimer();
          lockAnswer(parseInt(btn.getAttribute("data-i"), 10), Date.now() - startTime);
        });
      });

      function lockAnswer(chosenIdx, timeMs) {
        var correctIdx = q.answer;
        var isCorrect = chosenIdx === correctIdx;
        document.querySelectorAll(".quiz-option").forEach(function (btn) {
          var i = parseInt(btn.getAttribute("data-i"), 10);
          btn.classList.add("locked");
          btn.disabled = true;
          if (i === correctIdx) btn.classList.add("correct");
          else if (i === chosenIdx) btn.classList.add("wrong");
          if (i === chosenIdx) btn.classList.add("selected");
        });
        var explainEl = document.getElementById("quiz-explain");
        explainEl.textContent = (isCorrect ? "✓ 答對了。" : "✗ 這題答錯了。") + (q.explain ? "　" + q.explain : "");
        explainEl.classList.add("visible");
        document.getElementById("quiz-next-btn").style.display = "inline-block";

        state.answers.push({ category: q.category || "未分類", correct: isCorrect, timeMs: timeMs });

        document.getElementById("quiz-next-btn").addEventListener("click", function () {
          state.idx++;
          if (state.idx < questions.length) renderQuestion();
          else renderResult();
        }, { once: true });
      }
    }

    function renderResult() {
      clearTimer();
      playEl.innerHTML = "";
      var total = state.answers.length;
      var score = state.answers.filter(function (a) { return a.correct; }).length;
      var byCategory = {};
      state.answers.forEach(function (a) {
        var c = byCategory[a.category] || { correct: 0, total: 0 };
        c.total++; if (a.correct) c.correct++;
        byCategory[a.category] = c;
      });

      var catCards = Object.keys(byCategory).map(function (cat) {
        var c = byCategory[cat];
        var mastered = c.correct === c.total;
        return '<div class="quiz-cat-card ' + (mastered ? "mastered" : "weak") + '">' +
          '<div class="quiz-cat-name">' + esc(cat) + '</div>' +
          '<div class="quiz-cat-status ' + (mastered ? "mastered-text" : "weak-text") + '">' +
          (mastered ? "✓ 已掌握" : "△ 待加強 (" + c.correct + "/" + c.total + ")") + '</div></div>';
      }).join("");

      var weakCats = Object.keys(byCategory).filter(function (cat) {
        return byCategory[cat].correct < byCategory[cat].total;
      });
      var nextStepHTML = weakCats.length
        ? '<div class="quiz-next-step"><span class="quiz-next-step-label">下一步建議</span>' +
          weakCats.map(function (cat) {
            return "「" + esc(cat) + "」：" + esc(CATEGORY_HINTS[cat] || "建議重讀本頁對應段落。");
          }).join("<br><br>") + '</div>'
        : '<div class="quiz-next-step"><span class="quiz-next-step-label">下一步建議</span>全部分類都已掌握，這一位可以放心繼續往下一位讀了。</div>';

      resultEl.innerHTML =
        '<div class="quiz-result-score">' +
        '<span class="quiz-result-num">' + score + ' / ' + total + '</span>' +
        '<div class="quiz-result-label">答對題數</div></div>' +
        '<div class="quiz-cat-grid">' + catCards + '</div>' +
        nextStepHTML +
        '<div class="quiz-actions"><button class="quiz-btn secondary" id="quiz-restart-btn" type="button">重新測驗</button></div>';

      saveResult(personId, { score: score, total: total, byCategory: byCategory });

      document.getElementById("quiz-restart-btn").addEventListener("click", function () {
        resultEl.innerHTML = "";
        startBtn.style.display = "inline-block";
        descEl.style.display = "block";
      });
    }
  }

  global.PortraitQuiz = { loadAll: loadAll };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initQuiz);
  } else {
    initQuiz();
  }
})(window);
