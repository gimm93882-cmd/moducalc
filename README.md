# 복리 계산기

원금과 회차당 수익률로 복리를 계산합니다. → https://gimm93882-cmd.github.io/compound-calculator/

- **레버리지 환산** — 가격 변동률 × 배수 − 수수료 = 회차당 순수익률. 청산선도 함께 표시합니다.
- **목표 금액 역산** — 목표까지 몇 회차인지, 정한 기간에 맞추려면 회차당 몇 %가 필요한지 계산합니다.
- **승률 보정** — 승률과 손실 폭을 넣으면 기하평균 기준 기대값으로 다시 계산합니다.

계산은 전부 브라우저 안에서 이루어지며 입력값은 서버로 전송되지 않습니다.

## 구조

```
src/calculator.html   계산기 본체 (마크업 · 스타일 · 스크립트)
src/content.py        가이드 본문과 FAQ
build.py              위 둘을 합쳐 정적 페이지를 생성
```

루트의 `index.html`, `about.html`, `privacy.html`, `terms.html`, `sitemap.xml`,
`robots.txt` 는 **생성 결과물이므로 직접 고치지 않습니다.**

## 수정

```bash
python3 build.py
```

도메인을 연결한 뒤에는 정규 주소(canonical·sitemap)가 바뀌므로 주소를 넘겨서 빌드합니다.

```bash
python3 build.py https://bokricalc.com
```

## 고지

계산 결과는 입력한 가정에 대한 산술 결과일 뿐이며 특정 투자의 수익을 예상하거나 보장하지 않습니다.
