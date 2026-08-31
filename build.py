# -*- coding: utf-8 -*-
u"""모두계산기 정적 사이트 빌드.

    python3 build.py [사이트주소]

주소 구조
    /              허브 (계산기 목록)
    /<slug>/       계산기별 페이지
    /about.html /privacy.html /terms.html

계산기를 추가하려면 src/calcs.py 에 add(...) 를 하나 더 쓰면 된다.
페이지 생성·내비게이션·사이트맵은 여기서 자동으로 처리한다.

내부 링크는 상대 경로로 만든다. 계산기 페이지는 한 단계 아래에 있으므로
루트로 올라가는 접두사(up)를 페이지마다 다르게 넣는다.
"""

import io
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
import calcs  # noqa: E402
import content  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = (sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "https://moducalc.kr")
SITE = u"모두계산기"
CONTACT = "gimm93882@gmail.com"
UPDATED = "2026-08-31"
GROUPS = [u"급여·노무", u"대출·예금", u"사업·세금", u"부동산·생활", u"투자"]

# 구글 애드센스 게시자 ID. "ca-pub-" 로 시작하는 16자리 숫자다.
#
# 비워두면 광고 관련 코드가 전혀 들어가지 않는다. 값을 넣으면
#   - 모든 페이지 <head> 에 애드센스 스크립트와 사이트 확인용 메타 태그가 붙고
#   - ads.txt 가 생성된다 (없으면 승인 후 "승인되지 않은 판매자" 경고가 뜬다)
#
# 파일 src/adsense.txt 가 있으면 그 내용을 우선한다. 저장소에 커밋해도 되는 값이다.
ADSENSE = ""
_ad_file = os.path.join(ROOT, "src", "adsense.txt")
if os.path.exists(_ad_file):
    ADSENSE = io.open(_ad_file, encoding="utf-8").read().strip()

# 검색엔진 사이트 소유 확인 태그.
#
# src/verify.txt 에 한 줄에 하나씩 "name=content" 형식으로 적으면
# 모든 페이지 <head> 에 <meta name="..." content="..."> 로 들어간다.
# 주석(#)과 빈 줄은 무시한다.
#
#   google-site-verification=abc123...
#   naver-site-verification=def456...
#
# 구글 서치콘솔에서 "도메인 속성"으로 등록하면 DNS TXT 로 확인하므로 이 파일이 필요 없다.
# "URL 접두어"로 등록해 HTML 태그 방식을 고를 때만 쓴다.
VERIFY = []
_v_file = os.path.join(ROOT, "src", "verify.txt")
if os.path.exists(_v_file):
    for line in io.open(_v_file, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, _, val = line.partition("=")
        VERIFY.append((name.strip(), val.strip()))

FAVICON = ("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
           "<text y='.9em' font-size='90'>🧮</text></svg>")

CSS = io.open(os.path.join(ROOT, "src", "site.css"), encoding="utf-8").read()
ENGINE = io.open(os.path.join(ROOT, "src", "engine.js"), encoding="utf-8").read()
HUBJS = io.open(os.path.join(ROOT, "src", "hub.js"), encoding="utf-8").read()

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
<style>{css}</style>{verify}{jsonld}{adsense}
</head>
<body>
<nav class="sitenav"><div class="in">
<a class="brand" href="{up}">모두<em>계산기</em></a>
<div class="navlinks">{nav}</div>
</div></nav>
{body}
<footer class="sitefoot"><div class="in">
<div class="small">
  <strong>{site}</strong> · 급여, 대출, 세금, 부동산 계산을 한곳에서.<br>
  계산 결과는 입력한 값에 대한 산술 결과이며 법률·세무·투자 자문이 아닙니다.
  세율과 요율은 해마다 바뀌므로 중요한 판단에는 관계 기관 자료를 확인하세요.<br>
  문의 <a href="mailto:{contact}">{contact}</a>
</div>
<div class="links">{footlinks}</div>
</div></footer>
</body>
</html>
"""


def nav_html(up, path):
    items = [(up, "/", u"전체 계산기"),
             (up + "about.html", "/about.html", u"소개"),
             (up + "privacy.html", "/privacy.html", u"개인정보처리방침"),
             (up + "terms.html", "/terms.html", u"이용약관")]
    nav = "\n".join('<a href="%s"%s>%s</a>'
                    % (h, ' aria-current="page"' if c == path else "", t)
                    for h, c, t in items)
    foot = "\n".join('<a href="%s">%s</a>' % (h, t) for h, c, t in items)
    return nav, foot


def verify_head():
    """검색엔진 소유 확인 메타 태그."""
    return "".join('\n<meta name="%s" content="%s">' % (n, v) for n, v in VERIFY)


def adsense_head():
    """애드센스 스크립트와 사이트 확인용 메타 태그. ID 가 없으면 아무것도 넣지 않는다."""
    if not ADSENSE:
        return ""
    return ('\n<meta name="google-adsense-account" content="%s">'
            '\n<script async src="https://pagead2.googlesyndication.com/pagead/js/'
            'adsbygoogle.js?client=%s" crossorigin="anonymous"></script>'
            % (ADSENSE, ADSENSE))


def shell(path, title, desc, body, up="", jsonld=None):
    nav, foot = nav_html(up, path)
    ld = ('\n<script type="application/ld+json">%s</script>'
          % json.dumps(jsonld, ensure_ascii=False)) if jsonld else ""
    return SHELL.format(title=title, desc=desc, base=BASE, path=path, site=SITE,
                        favicon=FAVICON, css=CSS, jsonld=ld, adsense=adsense_head(),
                        verify=verify_head(), nav=nav, up=up or "./", body=body,
                        contact=CONTACT, footlinks=foot)


def faq_block(faq):
    if not faq:
        return ""
    items = "\n".join(
        u'<details><summary>%s</summary><div class="a">%s</div></details>' % (q, a)
        for q, a in faq)
    return u'<article class="faq"><h2 id="faq">자주 묻는 질문</h2>%s</article>' % items


def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}}
                           for q, a in faq]}


def app_ld(name, url, desc):
    return {"@context": "https://schema.org", "@type": "WebApplication",
            "name": name, "url": url, "applicationCategory": "FinanceApplication",
            "operatingSystem": "All", "inLanguage": "ko", "description": desc,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "KRW"}}


def related_html(c, items):
    """같은 분류의 다른 계산기. 내부 링크가 늘면 색인과 체류시간 모두에 도움이 된다."""
    rows = [x for x in items if x["group"] == c["group"] and x["slug"] != c["slug"]][:6]
    if not rows:
        return ""
    return (u'<section class="related"><h2>%s 계산기 더 보기</h2><div class="cards">%s</div>'
            u'<p class="allink"><a href="../">전체 계산기 보기 \u2192</a></p></section>'
            % (c["group"], "".join(
                u'<a class="card" href="../%s/"><span class="cname">%s</span>'
                u'<span class="ckw">%s</span></a>' % (x["slug"], x["name"], x["kw"])
                for x in rows)))


def calc_page(c, items):
    url = "%s/%s/" % (BASE, c["slug"])
    body = (
        u'<div class="wrap">'
        u'<header><p class="eyebrow"><a href="../">전체 계산기</a> · %s</p>'
        u'<h1>%s</h1><p>%s</p></header>'
        u'<div id="calc"></div>'
        u'</div>'
        u'<div class="prose"><article>%s</article>%s</div>'
        u'<div class="wrap">%s</div>'
        u'<script>%s</script><script>%s</script>'
        % (c["group"], c["name"], c["desc"], c["guide"], faq_block(c.get("faq")),
           related_html(c, items), ENGINE, c["spec"])
    )
    ld = [app_ld(c["name"], url, c["desc"])]
    if c.get("faq"):
        ld.append(faq_ld(c["faq"]))
    return shell("/%s/" % c["slug"], c["title"], c["desc"], body, up="../", jsonld=ld)


def card_html(c):
    return (u'<a class="card" href="%s/" data-slug="%s" data-name="%s" '
            u'data-kw="%s" data-group="%s">'
            u'<button class="star" type="button" data-slug="%s" '
            u'aria-pressed="false" aria-label="즐겨찾기">\u2606</button>'
            u'<span class="cname">%s</span><span class="ckw">%s</span></a>'
            % (c["slug"], c["slug"], c["name"], c["kw"], c["group"],
               c["slug"], c["name"], c["kw"]))


def hub_page(items):
    tabs = [u'<button class="tab" type="button" data-cat="all" aria-selected="true">'
            u'전체 <span class="n">%d</span></button>' % len(items)]
    for g in GROUPS:
        n = len([c for c in items if c["group"] == g])
        if n:
            tabs.append(u'<button class="tab" type="button" data-cat="%s" aria-selected="false">'
                        u'%s <span class="n">%d</span></button>' % (g, g, n))

    sections = []
    for g in GROUPS:
        rows = [c for c in items if c["group"] == g]
        if not rows:
            continue
        sections.append(u'<section class="group" data-group="%s"><h2>%s</h2>'
                        u'<div class="cards">%s</div></section>'
                        % (g, g, "".join(card_html(c) for c in rows)))

    body = (
        u'<div class="landing">'
        u'  <div class="landing-in">'
        u'    <p class="eyebrow">무료 · 가입 없음 · 설치 없음</p>'
        u'    <h1>필요한 계산,<br><em>여기서 끝냅니다</em></h1>'
        u'    <p class="lede">급여와 세금, 대출과 부동산까지 자주 쓰는 계산 %d가지. '
        u'모든 계산은 브라우저 안에서 이루어지며 입력한 값은 서버로 전송되지 않습니다.</p>'
        u'    <div class="search">'
        u'      <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/>'
        u'<line x1="16.5" y1="16.5" x2="21" y2="21"/></svg>'
        u'      <input id="q" type="text" autocomplete="off" '
        u'placeholder="계산기 검색  (초성도 됩니다 · ㅂㄱㅅ)" aria-label="계산기 검색">'
        u'      <button id="qclear" type="button" hidden aria-label="지우기">\u00d7</button>'
        u'    </div>'
        u'  </div>'
        u'</div>'
        u'<div class="wrap">'
        u'  <div class="tabs" role="tablist">%s</div>'
        u'  <section class="group" id="favgroup" hidden>'
        u'    <h2>즐겨찾기</h2><div class="cards" id="favcards"></div>'
        u'  </section>'
        u'  %s'
        u'  <p class="empty" id="empty" hidden>찾는 계산기가 없습니다. 다른 말로 검색해 보세요.</p>'
        u'</div>'
        u'<div class="prose"><article>%s</article>%s</div>'
        u'<script>%s</script>'
        % (len(items), "".join(tabs), "".join(sections),
           content.HUB_GUIDE, faq_block(content.HUB_FAQ), HUBJS)
    )

    ld = {"@context": "https://schema.org", "@type": "ItemList",
          "name": u"모두계산기 계산기 목록",
          "itemListElement": [{"@type": "ListItem", "position": i + 1,
                               "name": c["name"], "url": "%s/%s/" % (BASE, c["slug"])}
                              for i, c in enumerate(items)]}
    return shell("/", u"모두계산기 | 급여·대출·세금·부동산 계산기 %d종" % len(items),
                 u"연봉 실수령액, 퇴직금, 대출 이자, 부가세, 취득세, 양도소득세까지 "
                 u"자주 쓰는 계산기 %d가지를 한곳에. 무료이고 가입이 필요 없습니다." % len(items),
                 body, up="", jsonld=[ld, faq_ld(content.HUB_FAQ)])


def doc_page(path, title, desc, heading, html):
    body = u'<div class="prose"><article><h2>%s</h2>%s</article></div>' % (heading, html)
    return shell(path, title, desc, body, up="")


def write(rel, html):
    p = os.path.join(ROOT, rel)
    d = os.path.dirname(p)
    if d and not os.path.isdir(d):
        os.makedirs(d)
    io.open(p, "w", encoding="utf-8").write(html)
    return os.path.getsize(p)


def main():
    # 복리 계산기는 전용 로직(레버리지·목표역산·승률)이 있어 별도 페이지로 유지한다.
    bokri = {"slug": "bokri", "name": u"복리 계산기", "group": u"투자",
             "kw": u"레버리지·수수료 환산, 목표 금액 역산, 승률 보정",
             "title": u"복리 계산기 | 일복리·월복리·레버리지 수익률 계산",
             "desc": u"원금과 회차당 수익률로 복리를 계산합니다. 레버리지와 수수료를 "
                     u"수익률로 환산하고, 목표 금액까지 걸리는 회차를 역산하며, "
                     u"승률을 넣으면 실제 기대값으로 다시 계산합니다."}
    items = calcs.CALCS + [bokri]

    total = 0
    total += write("index.html", hub_page(items))

    for c in calcs.CALCS:
        total += write("%s/index.html" % c["slug"], calc_page(c, items))

    # 복리: 기존 전용 마크업 + 가이드
    widget = io.open(os.path.join(ROOT, "src", "calculator.html"), encoding="utf-8").read()
    body = (u'<div class="wrap"><header>'
            u'<p class="eyebrow"><a href="../">전체 계산기</a> · 투자</p>'
            u'<h1>복리 계산기</h1><p>%s</p></header></div>%s'
            u'<div class="prose"><article>%s</article>%s</div>'
            u'<div class="wrap">%s</div>'
            % (bokri["desc"], widget, content.GUIDE, faq_block(content.FAQ),
               related_html(bokri, items)))
    total += write("bokri/index.html",
                   shell("/bokri/", bokri["title"], bokri["desc"], body, up="../",
                         jsonld=[app_ld(bokri["name"], BASE + "/bokri/", bokri["desc"]),
                                 faq_ld(content.FAQ)]))

    total += write("privacy.html", doc_page(
        "/privacy.html", u"개인정보처리방침 | 모두계산기",
        u"모두계산기의 개인정보 처리 방침. 개인정보를 수집하지 않으며 계산은 브라우저에서만 이루어집니다.",
        u"개인정보처리방침", content.PRIVACY % (UPDATED, SITE, CONTACT, CONTACT)))
    total += write("terms.html", doc_page(
        "/terms.html", u"이용약관 | 모두계산기",
        u"모두계산기 이용약관과 면책 고지.",
        u"이용약관", content.TERMS % (UPDATED, SITE, CONTACT, CONTACT)))
    total += write("about.html", doc_page(
        "/about.html", u"소개 | 모두계산기",
        u"모두계산기를 만든 이유와 계산 방식, 문의처 안내.",
        u"소개", content.ABOUT % (len(items), CONTACT, CONTACT)))

    urls = ["/"] + ["/%s/" % c["slug"] for c in items] + \
           ["/about.html", "/privacy.html", "/terms.html"]
    sm = ('<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join('  <url><loc>%s%s</loc><lastmod>%s</lastmod>'
                    '<changefreq>monthly</changefreq><priority>%s</priority></url>\n'
                    % (BASE, u, UPDATED, "1.0" if u == "/" else "0.8" if u.endswith("/") else "0.3")
                    for u in urls)
          + "</urlset>\n")
    write("sitemap.xml", sm)
    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % BASE)

    # RSS. 계산기 사이트라 원래 필요 없지만 네이버 서치어드바이저가 제출 항목으로 두고 있다.
    # 각 계산기를 항목으로 넣어 수집 경로를 하나 더 열어준다.
    import email.utils
    now = email.utils.formatdate(usegmt=True)

    def esc(t):
        return (t.replace("&", "&amp;").replace("<", "&lt;")
                 .replace(">", "&gt;").replace('"', "&quot;"))

    entries = "".join(
        u"  <item>\n"
        u"    <title>%s</title>\n"
        u"    <link>%s/%s/</link>\n"
        u"    <guid isPermaLink=\"true\">%s/%s/</guid>\n"
        u"    <description>%s</description>\n"
        u"    <pubDate>%s</pubDate>\n"
        u"  </item>\n"
        % (esc(c["name"]), BASE, c["slug"], BASE, c["slug"], esc(c["desc"]), now)
        for c in items)

    rss = (u'<?xml version="1.0" encoding="UTF-8"?>\n'
           u'<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
           u'<channel>\n'
           u'  <title>%s</title>\n'
           u'  <link>%s/</link>\n'
           u'  <description>급여·대출·세금·부동산 계산기 모음</description>\n'
           u'  <language>ko</language>\n'
           u'  <lastBuildDate>%s</lastBuildDate>\n'
           u'  <atom:link href="%s/rss.xml" rel="self" type="application/rss+xml"/>\n'
           u'%s'
           u'</channel>\n</rss>\n'
           % (SITE, BASE, now, BASE, entries))
    write("rss.xml", rss)

    # ads.txt — 광고 재고를 팔 권한이 있는 판매자를 명시한다.
    # 없으면 승인 후 애드센스에 "승인되지 않은 판매자" 경고가 뜨고 수익이 줄 수 있다.
    if ADSENSE:
        pub = ADSENSE.replace("ca-", "")
        write("ads.txt", "google.com, %s, DIRECT, f08c47fec0942fa0\n" % pub)
    if BASE.startswith("https://moducalc.kr"):
        write("CNAME", "moducalc.kr\n")

    print(u"페이지 %d개 · %.0f KB" % (len(urls), total / 1024.0))
    print(u"애드센스 %s" % (ADSENSE if ADSENSE else u"미설정 (src/adsense.txt 없음)"))
    print(u"소유확인 %s" % (", ".join(n for n, v in VERIFY) if VERIFY
                            else u"미설정 (src/verify.txt 없음)"))
    print(u"기준 주소 %s" % BASE)
    for c in items:
        print(u"  /%-12s %s" % (c["slug"] + "/", c["name"]))


if __name__ == "__main__":
    main()
