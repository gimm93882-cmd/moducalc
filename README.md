# 모두계산기

급여·대출·세금·부동산 계산기 모음 → https://moducalc.kr

## 구조

```
src/engine.js      계산기 공용 엔진 (폼 렌더링 · 포맷 · 저장)
src/calcs.py       계산기 정의 (필드 + compute + 가이드 + FAQ)
src/calculator.html 복리 계산기 전용 마크업
src/content.py     허브 가이드 · 정책 문서
src/site.css       공용 스타일
build.py           위를 합쳐 정적 페이지 생성
```

루트의 `index.html`, `<slug>/index.html`, `sitemap.xml` 등은 **생성 결과물이므로
직접 고치지 않습니다.**

## 계산기 추가

`src/calcs.py` 에 `add(...)` 를 하나 더 쓰고 다시 빌드하면 됩니다.
허브 카드, 내비게이션, 사이트맵, 구조화 데이터는 자동으로 붙습니다.

```python
add(
    slug="example", name=u"예시 계산기", group=u"사업·세금",
    title=u"...", desc=u"...", kw=u"...",
    spec=u"""Calc.mount({ id:"example", fields:[...], compute:function(v,F){...} });""",
    guide=u"...", faq=[(u"질문", u"답")],
)
```

## 빌드

```bash
python3 build.py
```

주소를 바꿔 빌드하려면 인자로 넘깁니다.

```bash
python3 build.py https://moducalc.kr
```

## 고지

계산 결과는 입력값에 대한 산술 결과이며 세무·법률·노무·투자 자문이 아닙니다.
세율과 요율은 해마다 바뀌므로 관계 기관 자료를 확인하세요.
