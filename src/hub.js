/* 허브 화면: 검색 · 카테고리 · 즐겨찾기.
 *
 * 계산기가 32개가 되면서 카드를 눈으로 훑는 게 한계에 왔다.
 * 검색은 이름·설명·분류를 모두 보고, 한글은 초성으로도 찾는다(ㅂㄱㅅ → 부가세).
 */
(function () {
  "use strict";

  var CHO = ["ㄱ","ㄲ","ㄴ","ㄷ","ㄸ","ㄹ","ㅁ","ㅂ","ㅃ","ㅅ","ㅆ",
             "ㅇ","ㅈ","ㅉ","ㅊ","ㅋ","ㅌ","ㅍ","ㅎ"];

  /* "부가세" -> "ㅂㄱㅅ". 한글이 아닌 글자는 그대로 둔다. */
  function initials(s) {
    var out = "";
    for (var i = 0; i < s.length; i++) {
      var c = s.charCodeAt(i) - 0xAC00;
      out += (c >= 0 && c <= 11171) ? CHO[Math.floor(c / 588)] : s[i];
    }
    return out;
  }

  /* 초성 검색은 질의가 **자음만으로** 이루어졌을 때만 쓴다.
     그러지 않으면 "세금"(ㅅㄱ)이 모든 항목의 "계산기"(ㄱㅅㄱ)에 걸려 전부 매치된다. */
  function isChoOnly(s) {
    if (!s) return false;
    for (var i = 0; i < s.length; i++) {
      var c = s.charCodeAt(i);
      if (c === 32) continue;
      if (c < 0x3131 || c > 0x314E) return false;   /* ㄱ~ㅎ 밖이면 아님 */
    }
    return true;
  }

  var FAV = "moducalc:fav";
  function favs() {
    try { return JSON.parse(localStorage.getItem(FAV) || "[]"); } catch (e) { return []; }
  }
  function setFavs(v) {
    try { localStorage.setItem(FAV, JSON.stringify(v)); } catch (e) {}
  }

  var q = document.getElementById("q");
  var clear = document.getElementById("qclear");
  var tabs = document.querySelectorAll(".tab");
  var cards = [].slice.call(document.querySelectorAll(".card"));
  var groups = [].slice.call(document.querySelectorAll(".group"));
  var empty = document.getElementById("empty");
  var favSection = document.getElementById("favgroup");
  var favWrap = document.getElementById("favcards");

  /* 검색 대상 문자열을 미리 만들어 둔다. */
  cards.forEach(function (c) {
    var hay = (c.dataset.name + " " + c.dataset.kw + " " + c.dataset.group).toLowerCase();
    c._hay = hay;
    c._cho = initials(hay);
  });

  var state = { q: "", cat: "all" };

  function renderFavs() {
    if (!favWrap) return;
    var list = favs();
    favWrap.innerHTML = "";
    var found = 0;
    list.forEach(function (slug) {
      var src = cards.filter(function (c) { return c.dataset.slug === slug; })[0];
      if (!src) return;
      var clone = src.cloneNode(true);
      clone.classList.add("is-fav");
      favWrap.appendChild(clone);
      found++;
    });
    favSection.hidden = found === 0;
  }

  function apply() {
    var term = state.q.trim().toLowerCase();
    var choMode = isChoOnly(term);
    var shown = 0;

    cards.forEach(function (c) {
      var okCat = state.cat === "all" || c.dataset.group === state.cat;
      var okQ = !term ||
                (choMode ? c._cho.indexOf(term) >= 0 : c._hay.indexOf(term) >= 0);
      var on = okCat && okQ;
      c.hidden = !on;
      if (on) shown++;
    });

    /* 카드가 하나도 안 남은 분류는 제목까지 감춘다. */
    groups.forEach(function (g) {
      var any = [].slice.call(g.querySelectorAll(".card")).some(function (c) { return !c.hidden; });
      g.hidden = !any;
    });

    if (empty) empty.hidden = shown > 0;
    if (favSection) favSection.hidden = favSection.hidden || !!term || state.cat !== "all";
    if (clear) clear.hidden = !term;
  }

  if (q) {
    q.addEventListener("input", function () { state.q = q.value; apply(); });
    q.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { q.value = ""; state.q = ""; apply(); }
      if (e.key === "Enter") {
        var first = cards.filter(function (c) { return !c.hidden; })[0];
        if (first) location.href = first.getAttribute("href");
      }
    });
  }
  if (clear) {
    clear.addEventListener("click", function () {
      q.value = ""; state.q = ""; q.focus(); apply();
    });
  }

  tabs.forEach(function (t) {
    t.addEventListener("click", function () {
      tabs.forEach(function (x) { x.setAttribute("aria-selected", "false"); });
      t.setAttribute("aria-selected", "true");
      state.cat = t.dataset.cat;
      apply();
    });
  });

  /* 즐겨찾기 별. 카드 안의 버튼이므로 링크 이동을 막는다. */
  document.addEventListener("click", function (e) {
    var b = e.target.closest ? e.target.closest(".star") : null;
    if (!b) return;
    e.preventDefault();
    e.stopPropagation();
    var slug = b.dataset.slug;
    var list = favs();
    var i = list.indexOf(slug);
    if (i >= 0) list.splice(i, 1); else list.push(slug);
    setFavs(list);
    document.querySelectorAll('.star[data-slug="' + slug + '"]').forEach(function (x) {
      x.setAttribute("aria-pressed", String(i < 0));
      x.textContent = i < 0 ? "★" : "☆";
    });
    renderFavs();
    apply();
  });

  /* 첫 표시 */
  var saved = favs();
  document.querySelectorAll(".star").forEach(function (b) {
    var on = saved.indexOf(b.dataset.slug) >= 0;
    b.setAttribute("aria-pressed", String(on));
    b.textContent = on ? "★" : "☆";
  });
  renderFavs();
  apply();

  /* "/" 로 검색창 포커스 */
  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && document.activeElement !== q &&
        !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) {
      e.preventDefault();
      if (q) q.focus();
    }
  });
})();
