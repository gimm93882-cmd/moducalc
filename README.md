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

## 검사

```bash
node test.js
```

각 페이지에서 `Calc.mount` 를 가로채 `compute` 를 기본값으로 실행합니다.
결과에 `NaN` 이나 `undefined` 가 섞이면 실패로 처리합니다.

문법 검사만으로는 부족합니다. 실제로 `var decided` 의 공백이 사라져 `vardecided` 가 된 적이 있는데,
이건 문법상 유효한 전역 대입이라 파싱은 통과하고 실행에서만 터졌습니다.

## 검색엔진 소유 확인

`src/verify.txt` 에 한 줄에 하나씩 `name=content` 로 적으면 모든 페이지 `<head>` 에
메타 태그가 들어갑니다.

```
google-site-verification=abc123...
naver-site-verification=def456...
```

구글 서치콘솔을 **도메인 속성**으로 등록하면 DNS TXT 로 확인하므로 이 파일이 필요 없습니다.
**URL 접두어**로 등록해 HTML 태그 방식을 고를 때만 씁니다.

## 애드센스

게시자 ID 를 `src/adsense.txt` 에 한 줄로 넣고 다시 빌드하면 **모든 페이지**에
확인용 메타 태그와 광고 스크립트가 들어가고 `ads.txt` 가 생성됩니다.

```bash
echo "ca-pub-여기에번호" > src/adsense.txt
python3 build.py
```

파일이 없으면 광고 관련 코드가 전혀 들어가지 않습니다.
`ads.txt` 가 없으면 승인 후 "승인되지 않은 판매자" 경고가 뜨므로 함께 생성합니다.

## 고지

계산 결과는 입력값에 대한 산술 결과이며 세무·법률·노무·투자 자문이 아닙니다.
세율과 요율은 해마다 바뀌므로 관계 기관 자료를 확인하세요.
