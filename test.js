/* 계산기 런타임 검사.
 *
 *     node test.js
 *
 * 생성된 각 페이지에서 Calc.mount 호출을 가로채 compute 를 기본값으로 실행한다.
 * 문법 검사만으로는 잡히지 않는 것들을 잡기 위한 것이다. 실제로
 * `var decided` 의 공백이 사라져 `vardecided` 가 된 적이 있는데,
 * 이건 문법상 유효한 전역 대입이라 파싱은 통과하고 실행에서만 터졌다.
 */

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const ROOT = __dirname;
const F = {
  won: x => String(Math.round(x || 0)),
  kor: x => String(Math.round(x || 0)),
  num: x => String(x),
  pct: x => String(x),
  signed: x => String(x),
};

function specOf(html) {
  const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  // 엔진 정의부에도 "Calc.mount" 가 주석 예시로 들어 있다.
  // 엔진은 항상 먼저 오므로 조건에 맞는 것 중 마지막을 고른다.
  const hits = scripts.filter(s => s.includes("Calc.mount({") && !s.includes("function Calc(spec)"));
  return hits.length ? hits[hits.length - 1] : null;
}

function defaults(spec) {
  const v = {};
  for (const f of spec.fields || []) {
    if (f.type === "seg") v[f.k] = f.options[0].value;
    else if (f.type === "select") v[f.k] = f.value != null ? f.value : f.options[0].value;
    else v[f.k] = f.value;
    if (typeof v[f.k] === "string" && v[f.k] !== "" && !isNaN(v[f.k])) v[f.k] = +v[f.k];
  }
  return v;
}

let ok = 0, bad = 0;
const noop = () => {};

for (const dir of fs.readdirSync(ROOT).sort()) {
  const file = path.join(ROOT, dir, "index.html");
  if (!fs.existsSync(file)) continue;

  const src = specOf(fs.readFileSync(file, "utf8"));
  if (!src) continue;

  let captured = null;
  const el = { value: "", textContent: "", title: "", addEventListener: noop,
               querySelector: () => null, querySelectorAll: () => [] };
  const ctx = {
    window: {},
    Calc: { mount: s => { captured = s; return { run: noop }; } },
    document: { getElementById: () => el, querySelector: () => null,
                querySelectorAll: () => [], createElement: () => el },
    localStorage: { getItem: () => null, setItem: noop },
    fetch: () => ({ then: () => ({ then: () => ({ catch: noop }) }) }),
    setTimeout: noop,
    console,
  };

  try {
    vm.runInNewContext(src, ctx, { timeout: 3000 });
  } catch (e) {
    bad++; console.log(`  ✗ ${dir} [mount] ${e.message}`); continue;
  }
  if (!captured) { bad++; console.log(`  ✗ ${dir} [mount] spec 캡처 실패`); continue; }

  try {
    const out = captured.compute(defaults(captured), F);
    if (!out || !out.hero) throw new Error("hero 없음");
    const val = String(out.hero.v);
    if (val.includes("undefined") || val.includes("NaN")) throw new Error("결과가 " + val);
    for (const s of out.stats || []) {
      const sv = String(s.v);
      if (sv.includes("undefined") || sv.includes("NaN")) throw new Error(`${s.k} = ${sv}`);
    }
    ok++;
  } catch (e) {
    bad++; console.log(`  ✗ ${dir} [compute] ${e.message}`);
  }
}

console.log(`\n  정상 ${ok}개 · 오류 ${bad}개`);
process.exit(bad ? 1 : 0);
