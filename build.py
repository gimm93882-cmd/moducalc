# -*- coding: utf-8 -*-
"""정적 사이트 빌드.

    python3 build.py [사이트주소]

애드센스 심사를 염두에 둔 구성이다. 심사에서 반려되는 흔한 이유가
(1) 도구만 있고 읽을 내용이 없음 (2) 개인정보처리방침 없음 (3) 운영자 정보 없음
이라서, 계산기 아래 가이드와 FAQ 를 두고 정책·소개 페이지를 분리했다.
"""

import io
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
import content  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = (sys.argv[1].rstrip("/") if len(sys.argv) > 1
        else "https://gimm93882-cmd.github.io/compound-calculator")
CONTACT = "gimm93882@gmail.com"
SITE = u"복리 계산기"
UPDATED = "2026-08-31"

FAVICON = ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
           "<text y='.9em' font-size='90'>📈</text></svg>")

# href 는 상대 경로로 둔다. github.io/<repo>/ 하위 경로와 커스텀 도메인 루트
# 양쪽에서 모두 동작해야 하기 때문이다. 정규 경로(canonical)는 별도로 절대 주소를 쓴다.
NAV = [("./", "/", u"계산기"), ("about.html", "/about.html", u"소개"),
       ("privacy.html", "/privacy.html", u"개인정보처리방침"),
       ("terms.html", "/terms.html", u"이용약관")]

CHROME = u"""
<style>
/* 사이트 공통 껍데기. 계산기 자체 스타일은 src/calculator.html 안에 있다. */
.sitenav{border-bottom:1px solid var(--line);background:var(--surface)}
.sitenav .in{max-width:1160px;margin:0 auto;padding:0 20px;display:flex;
  align-items:center;gap:6px;flex-wrap:wrap;min-height:56px}
.sitenav a{color:var(--ink-2);text-decoration:none;font-size:13.5px;font-weight:500;
  padding:9px 11px;border-radius:7px;white-space:nowrap}
.sitenav a:hover{background:var(--surface-2);color:var(--ink)}
.sitenav a[aria-current="page"]{color:var(--accent-ink);font-weight:700;background:var(--accent-soft)}
.sitenav .brand{font-family:"Black Han Sans","Noto Sans KR",sans-serif;font-size:17px;
  color:var(--ink);margin-right:8px;padding-left:0}
.sitenav .brand em{font-style:normal;color:var(--accent)}

.prose{max-width:1160px;margin:0 auto;padding:8px 20px 0}
.prose article{background:var(--surface);border:1px solid var(--line);border-radius:14px;
  padding:30px 28px;margin-top:22px;box-shadow:var(--shadow)}
@media (max-width:600px){.prose article{padding:22px 17px}.prose{padding:8px 14px 0}}
.prose h2{font-family:"Black Han Sans","Noto Sans KR",sans-serif;font-weight:400;
  font-size:clamp(22px,4.6vw,30px);margin:0 0 18px;letter-spacing:-.01em}
.prose h3{font-size:clamp(16px,3.4vw,19px);font-weight:700;margin:30px 0 10px;
  letter-spacing:-.01em;color:var(--ink)}
.prose h3:first-of-type{margin-top:22px}
.prose p{margin:0 0 14px;color:var(--ink-2);line-height:1.85;max-width:68ch}
.prose strong{color:var(--ink);font-weight:700}
.prose li{color:var(--ink-2);line-height:1.85;margin-bottom:7px}
.prose .tablewrap{margin:16px 0 20px;border:1px solid var(--line);border-radius:10px}
.prose table{min-width:420px}
.prose .n{font-family:"JetBrains Mono",monospace;font-variant-numeric:tabular-nums}

.faq details{border:1px solid var(--line);border-radius:10px;margin-bottom:9px;
  background:var(--surface-3);overflow:hidden}
.faq summary{cursor:pointer;padding:15px 17px;font-weight:700;font-size:14.5px;
  list-style:none;color:var(--ink);display:flex;gap:10px;align-items:flex-start}
.faq summary::-webkit-details-marker{display:none}
.faq summary::before{content:"Q";color:var(--accent);font-family:"JetBrains Mono",monospace;
  font-weight:700;flex-shrink:0}
.faq details[open] summary{border-bottom:1px solid var(--line);background:var(--surface)}
.faq .a{padding:15px 17px 17px;color:var(--ink-2);line-height:1.85;font-size:14px}

.sitefoot{border-top:1px solid var(--line);margin-top:40px;background:var(--surface)}
.sitefoot .in{max-width:1160px;margin:0 auto;padding:26px 20px 40px;
  display:flex;flex-wrap:wrap;gap:18px;justify-content:space-between}
.sitefoot a{color:var(--ink-2);text-decoration:none;font-size:13px}
.sitefoot a:hover{color:var(--accent-ink);text-decoration:underline}
.sitefoot .links{display:flex;gap:16px;flex-wrap:wrap}
.sitefoot .small{font-size:12px;color:var(--muted);max-width:60ch;line-height:1.7}
</style>
"""

SHELL = u"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{base}{path}">
<meta name="theme-color" content="#FF6B00">
<link rel="icon" href="{favicon}">
<meta property="og:type" content="website">
<meta property="og:locale" content="ko_KR">
<meta property="og:site_name" content="{site}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{base}{path}">
<meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=JetBrains+Mono:wght@400;500;700&family=Noto+Sans+KR:wght@400;500;700;900&display=swap">
<style>*,*::before,*::after{{box-sizing:border-box}}html{{-webkit-text-size-adjust:100%}}body{{margin:0}}</style>
{chrome}{jsonld}
</head>
<body>
<nav class="sitenav"><div class="in">
<a class="brand" href="./">복리 <em>계산기</em></a>
{nav}
</div></nav>
{body}
<footer class="sitefoot"><div class="in">
<div class="small">
  <strong>{site}</strong><br>
  계산 결과는 입력한 가정에 대한 산술 결과일 뿐이며 특정 투자의 수익을 예상하거나 보장하지 않습니다.
  투자 판단과 그 결과에 대한 책임은 이용자 본인에게 있습니다.<br>
  문의 <a href="mailto:{contact}">{contact}</a>
</div>
<div class="links">{footlinks}</div>
</div></footer>
</body>
</html>
"""


def shell(path, title, desc, body, jsonld=""):
    nav = "\n".join(
        '<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if c == path else "", t)
        for h, c, t in NAV)
    foot = "\n".join('<a href="%s">%s</a>' % (h, t) for h, c, t in NAV)
    if jsonld:
        jsonld = '\n<script type="application/ld+json">%s</script>' % jsonld
    return SHELL.format(title=title, desc=desc, base=BASE, path=path, site=SITE,
                        favicon=FAVICON, chrome=CHROME, jsonld=jsonld, nav=nav,
                        body=body, contact=CONTACT, footlinks=foot)


def faq_html():
    items = "\n".join(
        u'<details><summary>%s</summary><div class="a">%s</div></details>' % (q, a)
        for q, a in content.FAQ)
    return u'<article class="faq"><h2 id="faq">자주 묻는 질문</h2>%s</article>' % items


def faq_jsonld():
    import json
    return json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text": a}}
                       for q, a in content.FAQ],
    }, ensure_ascii=False)


def app_jsonld():
    import json
    return json.dumps({
        "@context": "https://schema.org", "@type": "WebApplication",
        "name": SITE, "url": BASE + "/",
        "applicationCategory": "FinanceApplication",
        "operatingSystem": "All", "inLanguage": "ko",
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"},
        "description": u"원금과 회차당 수익률로 복리를 계산하고, 레버리지·수수료 환산과 "
                       u"목표 금액 역산, 승률을 반영한 기대값을 함께 보여주는 계산기.",
    }, ensure_ascii=False)


def page_index():
    calc = io.open(os.path.join(ROOT, "src", "calculator.html"), encoding="utf-8").read()
    body = (calc
            + u'\n<div class="prose">\n<article>' + content.GUIDE + u'</article>\n'
            + faq_html() + u'\n</div>')
    return shell("/", u"복리 계산기 | 일복리·월복리·레버리지 수익률 계산",
                 u"원금과 회차당 수익률로 복리를 계산합니다. 레버리지와 수수료를 수익률로 "
                 u"환산하고, 목표 금액까지 걸리는 회차를 역산하며, 승률을 넣으면 실제 기대값으로 "
                 u"다시 계산합니다. 무료, 설치 없음.",
                 body, "[%s,\n%s]" % (app_jsonld(), faq_jsonld()))


def doc(path, title, desc, heading, html):
    body = u'<div class="prose"><article><h2>%s</h2>%s</article></div>' % (heading, html)
    return shell(path, title, desc, body)


PRIVACY = u"""
<p class="small" style="color:var(--muted);font-size:13px">시행일 %s</p>

<p><strong>복리 계산기</strong>(이하 “사이트”)는 이용자의 개인정보를 소중히 다루며,
아래와 같이 처리 방침을 안내합니다.</p>

<h3>1. 수집하는 정보</h3>
<p>사이트는 회원가입 절차가 없으며, <strong>이름·연락처·계좌정보 등 개인을 식별할 수 있는
정보를 직접 수집하지 않습니다.</strong> 계산기에 입력한 금액과 수익률은 서버로 전송되지 않고
이용자의 브라우저 안에서만 처리됩니다.</p>

<h3>2. 브라우저 저장소 이용</h3>
<p>다시 방문했을 때 입력값을 그대로 보여드리기 위해, 입력한 숫자를 브라우저의
로컬 저장소(localStorage)에 보관합니다. 이 값은 이용자의 기기에만 저장되며 사이트 운영자를
포함한 누구에게도 전송되지 않습니다. 브라우저의 인터넷 사용 기록·사이트 데이터를 삭제하면
함께 지워집니다.</p>

<h3>3. 광고 및 제3자 쿠키</h3>
<p>사이트는 Google AdSense 등 제3자 광고를 게재할 수 있습니다. Google을 포함한 제3자
광고 사업자는 쿠키를 사용하여 이용자의 이 사이트 및 다른 사이트 방문 기록을 바탕으로
광고를 게재할 수 있습니다.</p>
<ul>
<li>Google의 광고 쿠키 사용에 관한 안내:
<a href="https://policies.google.com/technologies/ads" rel="noopener" target="_blank">policies.google.com/technologies/ads</a></li>
<li>맞춤 광고 사용 중지:
<a href="https://adssettings.google.com" rel="noopener" target="_blank">adssettings.google.com</a></li>
<li>제3자 광고 일괄 거부:
<a href="https://optout.aboutads.info" rel="noopener" target="_blank">optout.aboutads.info</a></li>
</ul>
<p>이용자는 브라우저 설정에서 쿠키 저장을 거부할 수 있습니다. 다만 이 경우 일부 기능이
정상적으로 동작하지 않을 수 있습니다.</p>

<h3>4. 접속 기록</h3>
<p>사이트는 GitHub Pages를 통해 제공되며, 호스팅 사업자가 서비스 운영과 보안을 위해
접속 기록을 처리할 수 있습니다. 자세한 내용은 해당 사업자의 정책을 따릅니다.</p>

<h3>5. 개인정보의 제3자 제공</h3>
<p>사이트는 이용자의 개인정보를 수집하지 않으므로 제3자에게 제공하는 정보도 없습니다.</p>

<h3>6. 이용자의 권리</h3>
<p>수집되는 개인정보가 없으므로 열람·정정·삭제를 요청할 대상 정보가 존재하지 않습니다.
브라우저에 저장된 입력값은 이용자가 직접 언제든 삭제할 수 있습니다.</p>

<h3>7. 아동의 개인정보</h3>
<p>사이트는 만 14세 미만 아동을 대상으로 하지 않으며, 아동의 개인정보를 의도적으로
수집하지 않습니다.</p>

<h3>8. 방침의 변경</h3>
<p>이 방침이 변경될 경우 이 페이지를 통해 공지합니다.</p>

<h3>9. 문의</h3>
<p>개인정보 처리와 관련한 문의는 <a href="mailto:%s">%s</a> 로 연락 주시기 바랍니다.</p>
"""

TERMS = u"""
<p class="small" style="color:var(--muted);font-size:13px">시행일 %s</p>

<h3>1. 목적</h3>
<p>이 약관은 <strong>복리 계산기</strong>(이하 “사이트”)가 제공하는 계산 도구의 이용 조건을
정합니다. 사이트를 이용함으로써 이 약관에 동의한 것으로 봅니다.</p>

<h3>2. 서비스의 성격</h3>
<p>사이트는 이용자가 <strong>직접 입력한 가정</strong>에 따라 복리 결과를 계산해 보여주는
도구입니다. 특정 금융상품이나 거래를 추천하지 않으며, 시장 데이터를 제공하지 않습니다.</p>

<h3>3. 투자 자문이 아님</h3>
<p>사이트가 제공하는 어떤 숫자나 설명도 <strong>투자 자문·권유·중개에 해당하지 않습니다.</strong>
사이트 운영자는 자본시장과 금융투자업에 관한 법률에 따른 투자자문업자가 아니며,
개별 이용자에게 적합한 투자 판단을 제시하지 않습니다.</p>

<h3>4. 결과의 한계</h3>
<p>계산 결과는 입력한 수치가 <strong>변동 없이 그대로 반복된다고 가정</strong>한 산술 결과입니다.
실제 거래에는 다음이 개입하며 사이트는 이를 반영하지 않습니다.</p>
<ul>
<li>체결 가격 차이(슬리피지)와 호가 공백</li>
<li>파생상품의 펀딩비·이자·롤오버 비용</li>
<li>증거금 부족에 따른 강제 청산</li>
<li>거래소·상품별로 다른 수수료 체계와 세금</li>
<li>시장 상황에 따른 수익률 변동</li>
</ul>
<p>표시되는 청산선은 유지증거금률을 일정하게 가정한 근사치이며, 실제 청산 기준은
거래소·포지션 규모·마진 방식에 따라 다릅니다.</p>

<h3>5. 면책</h3>
<p>이용자는 사이트의 계산 결과를 참고 자료로만 활용해야 하며, 이를 근거로 한 투자 판단과
그로 인한 손익은 전적으로 이용자 본인에게 귀속됩니다. 사이트 운영자는 계산 결과의 정확성·
완전성을 보증하지 않으며, 이용으로 발생한 손해에 대해 관련 법령이 허용하는 범위에서
책임을 지지 않습니다.</p>

<h3>6. 서비스의 변경과 중단</h3>
<p>사이트는 사전 통지 없이 기능을 변경하거나 제공을 중단할 수 있습니다.</p>

<h3>7. 저작권</h3>
<p>사이트의 문서와 코드에 대한 권리는 운영자에게 있습니다. 계산 결과를 개인적으로
활용하는 것은 자유이나, 사이트 전체 또는 상당 부분을 복제해 동일한 서비스를 제공하는 것은
허용되지 않습니다.</p>

<h3>8. 문의</h3>
<p><a href="mailto:%s">%s</a></p>
"""

ABOUT = u"""
<p><strong>복리 계산기</strong>는 원금과 회차당 수익률로 자산이 어떻게 불어나는지
계산하는 무료 도구입니다. 설치나 가입 없이 브라우저에서 바로 쓸 수 있습니다.</p>

<h3>왜 만들었나</h3>
<p>복리 계산기는 이미 많지만, 대부분 <strong>매 회차 반드시 이긴다</strong>고 가정합니다.
그 가정은 예·적금에는 맞지만 매매에는 맞지 않습니다. 지는 회차가 섞이는 순간
산술평균이 아니라 기하평균이 결과를 결정하는데, 이 차이를 보여주는 계산기가 드물었습니다.</p>
<p>그래서 세 가지를 더했습니다.</p>
<ul>
<li><strong>레버리지 환산</strong> — 가격 변동률을 증거금 대비 수익률로 바꾸고, 수수료를 배수만큼 반영하며, 청산선을 함께 보여줍니다.</li>
<li><strong>목표 금액 역산</strong> — 목표까지 몇 회차인지, 정한 기간에 맞추려면 회차당 몇 %%가 필요한지 계산합니다.</li>
<li><strong>승률 보정</strong> — 승률과 손실 폭을 넣으면 기하평균 기준의 실제 기대값을 계산합니다.</li>
</ul>

<h3>개인정보</h3>
<p>계산은 전부 브라우저 안에서 이루어집니다. 입력한 금액은 서버로 전송되지 않습니다.
자세한 내용은 <a href="privacy.html">개인정보처리방침</a>을 참고해 주세요.</p>

<h3>중요한 고지</h3>
<p>이 사이트는 <strong>투자 자문을 제공하지 않습니다.</strong> 계산 결과는 입력한 가정에 대한
산술 결과일 뿐이며 특정 투자의 수익을 예상하거나 보장하지 않습니다. 자세한 내용은
<a href="terms.html">이용약관</a>에 정리해 두었습니다.</p>

<h3>문의</h3>
<p>오류 제보나 기능 제안은 <a href="mailto:%s">%s</a> 로 보내주시면 확인하겠습니다.</p>
"""


def main():
    pages = {
        "index.html": page_index(),
        "privacy.html": doc("/privacy.html", u"개인정보처리방침 | 복리 계산기",
                            u"복리 계산기의 개인정보 처리 방침. 수집하는 개인정보가 없으며 "
                            u"계산은 브라우저 안에서만 이루어집니다.",
                            u"개인정보처리방침", PRIVACY % (UPDATED, CONTACT, CONTACT)),
        "terms.html": doc("/terms.html", u"이용약관 | 복리 계산기",
                          u"복리 계산기 이용약관과 투자 관련 면책 고지.",
                          u"이용약관", TERMS % (UPDATED, CONTACT, CONTACT)),
        "about.html": doc("/about.html", u"소개 | 복리 계산기",
                          u"복리 계산기를 만든 이유와 다른 계산기와의 차이, 문의처 안내.",
                          u"소개", ABOUT % (CONTACT, CONTACT)),
    }

    for name, html in pages.items():
        io.open(os.path.join(ROOT, name), "w", encoding="utf-8").write(html)

    urls = ["/", "/about.html", "/privacy.html", "/terms.html"]
    sitemap = ('<?xml version="1.0" encoding="UTF-8"?>\n'
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
               + "".join('  <url><loc>%s%s</loc><lastmod>%s</lastmod>'
                         '<changefreq>monthly</changefreq>'
                         '<priority>%s</priority></url>\n'
                         % (BASE, u, UPDATED, "1.0" if u == "/" else "0.5") for u in urls)
               + "</urlset>\n")
    io.open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(sitemap)

    io.open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
        "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BASE)

    for name in sorted(pages):
        p = os.path.join(ROOT, name)
        print("  %-14s %6d bytes" % (name, os.path.getsize(p)))
    print("  sitemap.xml, robots.txt")
    print("\n기준 주소: %s" % BASE)


if __name__ == "__main__":
    main()
