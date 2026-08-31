/* 계산기 공용 엔진.
 *
 * 계산기마다 폼과 렌더링을 새로 짜지 않는다. 각 계산기는 필드 정의와
 * compute(v) 하나만 제공하고, 화면 구성·포맷·저장은 전부 여기서 처리한다.
 *
 *   Calc.mount({
 *     id: "vat",
 *     fields: [{k:"amount", label:"공급가액", suffix:"원", value:1000000}],
 *     compute: function(v){ return { hero:{...}, stats:[...], rows:[...] }; }
 *   });
 */
(function (global) {
  "use strict";

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }

  var F = {
    won: function (n) {
      if (n == null || !isFinite(n)) return "—";
      return Math.round(n).toLocaleString("ko-KR") + "원";
    },
    /* 1,234,567,890 -> "12억 3,456만원". 큰 금액은 자릿수를 세지 않고 읽히게 한다. */
    kor: function (n) {
      if (n == null || !isFinite(n)) return "—";
      var neg = n < 0;
      n = Math.floor(Math.abs(n));
      if (n < 10000) return (neg ? "-" : "") + n.toLocaleString("ko-KR") + "원";
      var eok = Math.floor(n / 100000000), man = Math.floor((n % 100000000) / 10000);
      var out = [];
      if (eok) out.push(eok.toLocaleString("ko-KR") + "억");
      if (man) out.push(man.toLocaleString("ko-KR") + "만");
      return (neg ? "-" : "") + out.join(" ") + "원";
    },
    num: function (n, d) {
      if (n == null || !isFinite(n)) return "—";
      return n.toLocaleString("ko-KR", { maximumFractionDigits: d == null ? 0 : d });
    },
    pct: function (n, d) {
      if (n == null || !isFinite(n)) return "—";
      return n.toFixed(d == null ? 2 : d) + "%";
    },
    signed: function (n, d) {
      if (n == null || !isFinite(n)) return "—";
      return (n >= 0 ? "+" : "") + n.toFixed(d == null ? 2 : d) + "%";
    }
  };

  function Calc(spec) {
    this.spec = spec;
    this.key = "moducalc:" + spec.id;
    this.root = document.getElementById("calc");
    this.inputs = {};
  }

  Calc.prototype.build = function () {
    var self = this, s = this.spec;

    var grid = el("div", "grid");
    var side = el("div", "side");
    var panel = el("div", "panel");
    panel.appendChild(el("div", "panel-head", "<h2>" + (s.formTitle || "입력") + "</h2>"));
    var body = el("div", "panel-body");

    (s.fields || []).forEach(function (f) {
      body.appendChild(self.field(f));
    });
    panel.appendChild(body);
    side.appendChild(panel);
    if (s.sideNote) side.appendChild(el("div", "note sidenote", s.sideNote));
    grid.appendChild(side);

    var stack = el("div", "stack");
    var res = el("div", "panel");
    res.appendChild(el("div", "panel-head",
      "<h2>" + (s.resultTitle || "결과") + "</h2><span class='hint' id='resHint'></span>"));
    res.appendChild(el("div", "hero", ""));
    res.appendChild(el("div", "stats", ""));
    var extra = el("div", "panel-body");
    extra.id = "extra";
    res.appendChild(extra);
    stack.appendChild(res);

    var tbl = el("div", "panel");
    tbl.id = "tablePanel";
    tbl.style.display = "none";
    tbl.appendChild(el("div", "panel-head",
      "<h2>" + (s.tableTitle || "상세") + "</h2><span class='hint' id='tblHint'></span>"));
    var wrap = el("div", "tablewrap");
    wrap.appendChild(el("table", "", "<thead></thead><tbody></tbody>"));
    tbl.appendChild(wrap);
    stack.appendChild(tbl);

    grid.appendChild(stack);
    this.root.appendChild(grid);

    this.hero = res.querySelector(".hero");
    this.stats = res.querySelector(".stats");
    this.extra = extra;
    this.tablePanel = tbl;
    this.thead = tbl.querySelector("thead");
    this.tbody = tbl.querySelector("tbody");
    this.hint = res.querySelector("#resHint");
    this.tblHint = tbl.querySelector("#tblHint");
  };

  Calc.prototype.field = function (f) {
    var self = this;
    var wrap = el("div", "field");
    var lab = el("label", "", f.label + (f.sub ? " <span class='sub'>" + f.sub + "</span>" : ""));
    lab.setAttribute("for", "f_" + f.k);
    wrap.appendChild(lab);

    if (f.type === "seg") {
      var seg = el("div", "seg");
      f.options.forEach(function (o, i) {
        var b = el("button", "", o.label);
        b.type = "button";
        b.dataset.v = o.value;
        b.setAttribute("aria-pressed", String(i === 0));
        b.addEventListener("click", function () {
          seg.querySelectorAll("button").forEach(function (x) {
            x.setAttribute("aria-pressed", "false");
          });
          b.setAttribute("aria-pressed", "true");
          self.run();
        });
        seg.appendChild(b);
      });
      wrap.appendChild(seg);
      this.inputs[f.k] = { type: "seg", node: seg };
    } else if (f.type === "select") {
      var sel = el("select");
      sel.id = "f_" + f.k;
      f.options.forEach(function (o) {
        var op = document.createElement("option");
        op.value = o.value; op.textContent = o.label;
        sel.appendChild(op);
      });
      if (f.value != null) sel.value = f.value;
      sel.addEventListener("change", function () { self.run(); });
      wrap.appendChild(sel);
      this.inputs[f.k] = { type: "select", node: sel };
    } else {
      var ctl = el("div", "control");
      var inp = document.createElement("input");
      inp.type = f.type === "date" ? "date" : "number";
      inp.id = "f_" + f.k;
      if (f.step != null) inp.step = f.step;
      if (f.min != null) inp.min = f.min;
      if (f.value != null) inp.value = f.value;
      if (f.suffix) inp.className = "has-suffix";
      inp.addEventListener("input", function () { self.run(); });
      ctl.appendChild(inp);
      if (f.suffix) ctl.appendChild(el("span", "suffix", f.suffix));
      wrap.appendChild(ctl);
      if (f.note) wrap.appendChild(el("div", "readout", f.note));
      this.inputs[f.k] = { type: "num", node: inp };
    }
    return wrap;
  };

  Calc.prototype.values = function () {
    var v = {};
    for (var k in this.inputs) {
      var it = this.inputs[k];
      if (it.type === "seg") {
        var on = it.node.querySelector('button[aria-pressed="true"]');
        v[k] = on ? on.dataset.v : null;
        if (v[k] !== null && v[k] !== "" && !isNaN(v[k])) v[k] = +v[k];
      } else if (it.type === "select") {
        v[k] = isNaN(it.node.value) || it.node.value === "" ? it.node.value : +it.node.value;
      } else if (it.node.type === "date") {
        v[k] = it.node.value;
      } else {
        v[k] = it.node.value === "" ? null : +it.node.value;
      }
    }
    return v;
  };

  Calc.prototype.run = function () {
    var out;
    try {
      out = this.spec.compute(this.values(), F);
    } catch (e) {
      out = { hero: { k: "오류", v: "입력값을 확인해 주세요" } };
    }
    if (!out) return;

    var h = out.hero || {};
    this.hero.innerHTML =
      "<div class='k'>" + (h.k || "") + "</div>" +
      "<div class='v display " + (h.cls || "") + "'>" + (h.v || "—") + "</div>" +
      (h.sub ? "<div class='exact'>" + h.sub + "</div>" : "");

    this.stats.innerHTML = (out.stats || []).map(function (s) {
      return "<div class='stat'><div class='k'>" + s.k + "</div>" +
        "<div class='v num " + (s.cls || "") + "'>" + s.v + "</div>" +
        (s.sub ? "<div class='sub'>" + s.sub + "</div>" : "") + "</div>";
    }).join("");
    this.stats.style.display = (out.stats && out.stats.length) ? "" : "none";

    this.extra.innerHTML = out.extra || "";
    this.extra.style.display = out.extra ? "" : "none";
    this.hint.textContent = out.hint || "";

    if (out.rows && out.rows.length) {
      this.tablePanel.style.display = "";
      this.thead.innerHTML = "<tr>" + (out.cols || []).map(function (c) {
        return "<th>" + c + "</th>";
      }).join("") + "</tr>";
      this.tbody.innerHTML = out.rows.map(function (r) {
        return "<tr>" + r.map(function (c, i) {
          return "<td" + (i ? " class='n'" : "") + ">" + c + "</td>";
        }).join("") + "</tr>";
      }).join("");
      this.tblHint.textContent = out.tableHint || "";
    } else {
      this.tablePanel.style.display = "none";
    }

    this.save();
  };

  Calc.prototype.save = function () {
    try {
      var v = {};
      for (var k in this.inputs) {
        var it = this.inputs[k];
        v[k] = it.type === "seg"
          ? (it.node.querySelector('button[aria-pressed="true"]') || {}).dataset.v
          : it.node.value;
      }
      localStorage.setItem(this.key, JSON.stringify(v));
    } catch (e) {}
  };

  Calc.prototype.load = function () {
    try {
      var v = JSON.parse(localStorage.getItem(this.key) || "null");
      if (!v) return;
      for (var k in v) {
        var it = this.inputs[k];
        if (!it || v[k] == null) continue;
        if (it.type === "seg") {
          it.node.querySelectorAll("button").forEach(function (b) {
            b.setAttribute("aria-pressed", String(b.dataset.v === v[k]));
          });
        } else {
          it.node.value = v[k];
        }
      }
    } catch (e) {}
  };

  global.Calc = {
    fmt: F,
    mount: function (spec) {
      var c = new Calc(spec);
      c.build();
      c.load();
      c.run();
      return c;
    }
  };
})(window);
