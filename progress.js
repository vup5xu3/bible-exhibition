// ══════════════════════════════════════════
// PortraitProgress — 閱讀紀錄（純瀏覽器 localStorage，無伺服器）
// 供 index.html 與所有 portrait_*.html 共用。
// 資料格式：{ [人物id]: 標記已讀的 ISO 時間字串 }
// ══════════════════════════════════════════
(function (global) {
  var KEY = "portrait_read_v1";

  function load() {
    try {
      var raw = localStorage.getItem(KEY);
      if (!raw) return {};
      var obj = JSON.parse(raw);
      return (obj && typeof obj === "object") ? obj : {};
    } catch (e) { return {}; }
  }

  function save(obj) {
    try { localStorage.setItem(KEY, JSON.stringify(obj)); } catch (e) {}
  }

  function isRead(id) { return !!load()[id]; }

  function setRead(id, val) {
    var obj = load();
    if (val) obj[id] = new Date().toISOString();
    else delete obj[id];
    save(obj);
    return obj;
  }

  function toggle(id) {
    var obj = load();
    if (obj[id]) delete obj[id];
    else obj[id] = new Date().toISOString();
    save(obj);
    return !!obj[id];
  }

  function count() { return Object.keys(load()).length; }

  function exportJSON() {
    var data = { version: 1, exportedAt: new Date().toISOString(), read: load() };
    var blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    var d = new Date();
    var pad = function (n) { return String(n).padStart(2, "0"); };
    a.href = url;
    a.download = "portrait-progress-" + d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()) + ".json";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  // 匯入：與現有紀錄「合併」（不會覆蓋／刪除既有紀錄），方便跨裝置同步
  function importFile(file, cb) {
    var reader = new FileReader();
    reader.onload = function () {
      try {
        var parsed = JSON.parse(reader.result);
        var incoming = (parsed && typeof parsed === "object" && parsed.read && typeof parsed.read === "object")
          ? parsed.read : parsed;
        if (!incoming || typeof incoming !== "object" || Array.isArray(incoming)) {
          throw new Error("檔案格式不正確");
        }
        var current = load();
        var added = 0;
        Object.keys(incoming).forEach(function (id) {
          if (!current[id]) added++;
          var t = typeof incoming[id] === "string" ? incoming[id] : new Date().toISOString();
          if (!current[id] || t < current[id]) current[id] = t;
        });
        save(current);
        cb(null, { added: added, total: Object.keys(current).length });
      } catch (e) {
        cb(e);
      }
    };
    reader.onerror = function () { cb(reader.error || new Error("讀取檔案失敗")); };
    reader.readAsText(file, "utf-8");
  }

  function resetAll() { save({}); }

  global.PortraitProgress = {
    load: load, save: save, isRead: isRead, setRead: setRead, toggle: toggle,
    count: count, exportJSON: exportJSON, importFile: importFile, resetAll: resetAll, KEY: KEY
  };

  // ── 人物頁：右下角「標記已讀」浮動按鈕（自動依網址判斷 id，無需另外埋參數）──
  function initReadToggleButton() {
    var m = location.pathname.match(/portrait_([a-zA-Z0-9_]+)\.html?$/i);
    if (!m) return;
    var id = m[1];

    var style = document.createElement("style");
    style.textContent =
      ".read-toggle-btn{position:fixed;right:20px;bottom:20px;z-index:200;background:var(--ink,#1A1610);" +
      "color:var(--gold-light,#D4AF5A);border:1px solid var(--gold,#B8962E);border-radius:30px;" +
      "padding:10px 20px;font-family:'Noto Sans TC',sans-serif;font-size:13px;letter-spacing:.05em;" +
      "cursor:pointer;box-shadow:0 4px 18px rgba(0,0,0,.28);transition:background .2s,color .2s,transform .15s;}" +
      ".read-toggle-btn:hover{transform:translateY(-2px);background:var(--gold,#B8962E);color:var(--ink,#1A1610);}" +
      ".read-toggle-btn.is-read{background:var(--teal-deep,#1A4A3E);color:#fff;border-color:var(--teal-deep,#1A4A3E);}" +
      "@media (max-width:640px){.read-toggle-btn{right:14px;bottom:14px;padding:9px 15px;font-size:12px;}}";
    document.head.appendChild(style);

    var btn = document.createElement("button");
    btn.className = "read-toggle-btn";
    btn.id = "read-toggle-btn";
    btn.type = "button";

    function render() {
      var read = isRead(id);
      btn.textContent = read ? "✓ 已讀" : "☆ 標記已讀";
      btn.classList.toggle("is-read", read);
      btn.setAttribute("aria-pressed", read ? "true" : "false");
    }
    btn.addEventListener("click", function () { toggle(id); render(); });
    render();

    document.body.appendChild(btn);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initReadToggleButton);
  } else {
    initReadToggleButton();
  }
})(window);
