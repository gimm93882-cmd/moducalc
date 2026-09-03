# -*- coding: utf-8 -*-
u"""계산기 정의.

각 항목은 dict 이며 build.py 가 페이지로 만든다.

  slug     주소 (/slug/)
  name     계산기 이름
  title    <title>
  desc     메타 설명
  kw       허브 카드에 붙는 한 줄 설명
  group    허브에서 묶이는 분류
  spec     Calc.mount 에 넘길 자바스크립트 (문자열)
  guide    본문 HTML
  faq      [(질문, 답)]

요율은 해마다 바뀐다. 상수로 박지 말고 입력 필드로 빼서 이용자가 고칠 수 있게 한다.
"""

CALCS = []


def add(**kw):
    CALCS.append(kw)


# ───────────────────────── 부가가치세 ─────────────────────────
add(
    slug="bugagse", name=u"부가세 계산기", group=u"사업·세금",
    title=u"부가세 계산기 | 공급가액·부가가치세 자동 계산",
    desc=u"공급가액에서 부가세를 더하거나, 합계금액에서 부가세를 역산합니다. 세율도 바꿀 수 있습니다.",
    kw=u"공급가액에서 더하거나 합계액에서 역산",
    spec=u"""
Calc.mount({
  id:"bugagse",
  formTitle:"금액 입력",
  fields:[
    {k:"mode", label:"기준", type:"seg", options:[
      {value:"supply", label:"공급가액"}, {value:"total", label:"합계금액"}]},
    {k:"amount", label:"금액", suffix:"원", value:1000000, step:1000, min:0},
    {k:"rate", label:"세율", sub:"일반 10%", suffix:"%", value:10, step:0.5, min:0}
  ],
  compute:function(v,F){
    var r=(v.rate||0)/100, a=v.amount||0, supply, vat, total;
    if(v.mode==="total"){ total=a; supply=a/(1+r); vat=total-supply; }
    else { supply=a; vat=a*r; total=a+vat; }
    return {
      hero:{k: v.mode==="total" ? "부가세 (합계에 포함된 금액)" : "부가세",
            v:F.kor(vat), sub:F.won(vat)},
      stats:[
        {k:"공급가액", v:F.won(supply)},
        {k:"부가세", v:F.won(vat), cls:"up"},
        {k:"합계금액", v:F.won(total)}
      ],
      hint:"세율 "+F.num(v.rate,1)+"%",
      extra:"<div class='note'>"+
        (v.mode==="total"
          ? "합계 <b>"+F.won(total)+"</b> 에는 부가세 <b>"+F.won(vat)+"</b> 가 포함돼 있습니다. 공급가액은 <b>"+F.won(supply)+"</b> 입니다."
          : "공급가액 <b>"+F.won(supply)+"</b> 에 부가세 <b>"+F.won(vat)+"</b> 를 더하면 <b>"+F.won(total)+"</b> 를 청구하게 됩니다.")
        +"</div>"
    };
  }
});""",
    guide=u"""
<h3>공급가액과 합계금액은 다릅니다</h3>
<p>거래에서 혼동이 가장 많이 생기는 지점입니다. <strong>공급가액</strong>은 부가세를 빼고
물건이나 용역 자체의 값이고, <strong>합계금액</strong>은 여기에 부가세를 더해 실제로 주고받는 돈입니다.
세금계산서에는 둘이 따로 적힙니다.</p>

<h3>합계금액에서 부가세를 뽑을 때 흔한 실수</h3>
<p>110만원을 받았을 때 부가세를 <em>110만 × 10% = 11만원</em>으로 계산하면 틀립니다.
110만원은 이미 부가세가 포함된 금액이므로 <strong>1.1로 나눠야</strong> 합니다.
공급가액 100만원, 부가세 10만원이 맞습니다. 이 계산기의 ‘합계금액’ 기준이 그 역산을 해줍니다.</p>

<h3>간이과세자와 일반과세자</h3>
<p>연 매출 기준을 넘는 일반과세자는 10% 세율로 세금계산서를 발행하고 매입세액을 공제받습니다.
간이과세자는 업종별 부가가치율이 적용돼 실제 부담률이 낮은 대신 매입세액 공제와
세금계산서 발행에 제약이 있습니다. 본인이 어느 쪽인지에 따라 계산이 달라지므로
홈택스나 세무 담당자에게 확인하세요.</p>

<h3>영세율과 면세</h3>
<p>수출 등에 적용되는 <strong>영세율</strong>은 세율이 0%이고, 매입세액은 환급받을 수 있습니다.
<strong>면세</strong>는 애초에 부가세 과세 대상이 아니라 매입세액 공제도 되지 않습니다.
세율 칸에 0을 넣으면 영세율 상황의 금액을 확인할 수 있습니다.</p>
""",
    faq=[
        (u"110만원을 받았는데 부가세가 얼마인가요?",
         u"‘합계금액’ 기준으로 110만원을 넣으시면 공급가액 100만원, 부가세 10만원이 나옵니다. "
         u"110만원에 10%를 곱하는 것이 아니라 1.1로 나눠야 합니다."),
        (u"세율을 바꿀 수 있나요?",
         u"바꿀 수 있습니다. 일반 세율은 10%이고, 영세율 거래는 0을 넣으시면 됩니다."),
        (u"간이과세자도 이 계산기를 쓸 수 있나요?",
         u"부가세를 포함·제외한 금액 자체를 확인하는 용도로는 쓸 수 있습니다. 다만 간이과세자의 "
         u"실제 납부세액은 업종별 부가가치율이 적용돼 다르게 산출되므로 홈택스에서 확인하세요."),
    ],
)

# ───────────────────────── 마진율 ─────────────────────────
add(
    slug="margin", name=u"마진율 계산기", group=u"사업·세금",
    title=u"마진율 계산기 | 원가·판매가로 마진율과 목표 판매가 계산",
    desc=u"원가와 판매가로 마진율·마진액·원가율을 계산하고, 목표 마진율에 맞는 판매가를 역산합니다.",
    kw=u"원가·판매가로 마진율, 목표 마진율로 판매가 역산",
    spec=u"""
Calc.mount({
  id:"margin",
  formTitle:"원가와 판매가",
  fields:[
    {k:"mode", label:"계산 방향", type:"seg", options:[
      {value:"rate", label:"마진율 구하기"}, {value:"price", label:"판매가 구하기"}]},
    {k:"cost", label:"원가", sub:"매입가", suffix:"원", value:6000, step:100, min:0},
    {k:"price", label:"판매가", sub:"마진율 구하기에서 사용", suffix:"원", value:10000, step:100, min:0},
    {k:"target", label:"목표 마진율", sub:"판매가 구하기에서 사용", suffix:"%", value:40, step:1},
    {k:"qty", label:"판매 수량", suffix:"개", value:100, step:1, min:0}
  ],
  compute:function(v,F){
    var cost=v.cost||0, price, marginRate;
    if(v.mode==="price"){
      var t=Math.min(v.target||0, 99.9)/100;
      price = t>=1 ? 0 : cost/(1-t);
      marginRate = t*100;
    } else {
      price=v.price||0;
      marginRate = price>0 ? (price-cost)/price*100 : 0;
    }
    var unit=price-cost, qty=v.qty||0;
    var costRate = price>0 ? cost/price*100 : 0;
    var markup = cost>0 ? (price-cost)/cost*100 : 0;
    return {
      hero:{k: v.mode==="price" ? "필요 판매가" : "마진율",
            v: v.mode==="price" ? F.won(price) : F.pct(marginRate,1),
            cls: unit>=0?"up":"down",
            sub: v.mode==="price" ? "마진율 "+F.pct(marginRate,1) : "개당 "+F.won(unit)},
      stats:[
        {k:"개당 마진", v:F.won(unit), cls:unit>=0?"up":"down"},
        {k:"총 마진", v:F.won(unit*qty), sub:F.num(qty)+"개 기준", cls:unit>=0?"up":"down"},
        {k:"원가율", v:F.pct(costRate,1)}
      ],
      hint:"원가 "+F.won(cost),
      extra:"<div class='note'>마진율 <b>"+F.pct(marginRate,1)+"</b> 는 <b>판매가</b> 대비 비율입니다. "+
        "원가 대비로 계산하는 <b>마크업</b>은 <b>"+F.pct(markup,1)+"</b> 입니다. 둘을 섞어 쓰면 손해를 봅니다.</div>"
    };
  }
});""",
    guide=u"""
<h3>마진율과 마크업을 섞어 쓰면 손해를 봅니다</h3>
<p>같은 거래인데 기준이 다릅니다.</p>
<ul>
<li><strong>마진율</strong> = (판매가 − 원가) ÷ <strong>판매가</strong></li>
<li><strong>마크업</strong> = (판매가 − 원가) ÷ <strong>원가</strong></li>
</ul>
<p>원가 6,000원에 10,000원으로 팔면 마진율은 40%지만 마크업은 66.7%입니다.
“마진 40% 붙였다”고 하면서 원가에 40%를 더해 8,400원에 팔면, 실제 마진율은 28.6%밖에 안 됩니다.
거래처와 이야기할 때 어느 기준인지 먼저 맞춰야 합니다.</p>

<h3>목표 마진율에서 판매가를 역산하는 법</h3>
<p>원가를 <em>(1 − 목표마진율)</em>로 나눕니다. 원가 6,000원에 마진율 40%를 남기려면
6,000 ÷ 0.6 = 10,000원입니다. 원가에 40%를 더하는 것이 아닙니다.
‘판매가 구하기’ 모드가 이 계산을 해줍니다.</p>

<h3>원가에 빠뜨리기 쉬운 것들</h3>
<p>매입가만 원가로 잡으면 실제 남는 돈이 계산과 어긋납니다. 카드 수수료, 배송비, 포장비,
플랫폼 판매수수료, 반품·폐기 손실을 원가에 포함해서 넣어야 실제 마진이 보입니다.
카드 결제 비중이 높다면 <a href="../card/">카드 수수료 계산기</a>로 실수령액을 먼저 확인하세요.</p>

<h3>부가세는 마진 계산에서 빼고 봅니다</h3>
<p>일반과세자라면 매출 부가세는 잠시 보관했다 납부하는 돈이지 매출이 아닙니다.
마진은 <strong>공급가액 기준</strong>으로 계산해야 정확합니다.
<a href="../bugagse/">부가세 계산기</a>에서 공급가액을 먼저 뽑아 넣으세요.</p>
""",
    faq=[
        (u"마진율과 마크업 중 어느 것이 맞나요?",
         u"둘 다 쓰이지만 기준이 다릅니다. 유통·소매에서는 보통 판매가 기준인 마진율을 씁니다. "
         u"이 계산기는 두 값을 함께 보여주니 거래처와 기준을 맞출 때 활용하세요."),
        (u"원가에 무엇까지 넣어야 하나요?",
         u"매입가에 더해 카드 수수료, 배송비, 포장비, 플랫폼 수수료, 반품·폐기 손실까지 넣어야 "
         u"실제 남는 금액이 나옵니다."),
        (u"마진율 100%는 왜 안 되나요?",
         u"마진율은 판매가 대비 비율이라 100%가 되려면 원가가 0이어야 합니다. "
         u"원가 대비 두 배로 파는 것은 마진율 50%, 마크업 100%입니다."),
    ],
)

# ───────────────────────── 카드 수수료 ─────────────────────────
add(
    slug="card", name=u"카드 수수료 계산기", group=u"사업·세금",
    title=u"카드 수수료 계산기 | 결제금액에서 실수령액 계산",
    desc=u"카드 결제금액에서 수수료를 빼고 실제로 입금되는 금액을 계산합니다. 월 매출 기준 부담액도 확인할 수 있습니다.",
    kw=u"결제금액에서 수수료 빼고 실입금액 확인",
    spec=u"""
Calc.mount({
  id:"card",
  formTitle:"결제 정보",
  fields:[
    {k:"amount", label:"결제금액", sub:"1건", suffix:"원", value:50000, step:1000, min:0},
    {k:"rate", label:"수수료율", sub:"우대가맹점은 낮습니다", suffix:"%", value:1.5, step:0.05, min:0},
    {k:"vatOnFee", label:"수수료 부가세", type:"seg", options:[
      {value:"0", label:"미포함"}, {value:"1", label:"10% 추가"}]},
    {k:"monthly", label:"월 카드 매출", suffix:"원", value:20000000, step:100000, min:0}
  ],
  compute:function(v,F){
    var a=v.amount||0, r=(v.rate||0)/100;
    var mul = v.vatOnFee==1 ? 1.1 : 1;
    var fee=a*r*mul, net=a-fee;
    var m=v.monthly||0, mFee=m*r*mul;
    return {
      hero:{k:"실수령액 (1건)", v:F.kor(net), sub:F.won(net), cls:"up"},
      stats:[
        {k:"수수료", v:F.won(fee), cls:"down", sub:v.vatOnFee==1?"부가세 포함":"부가세 별도"},
        {k:"월 수수료", v:F.won(mFee), cls:"down", sub:"월 매출 "+F.kor(m)},
        {k:"연 수수료", v:F.won(mFee*12), cls:"down"}
      ],
      hint:"수수료율 "+F.num(v.rate,2)+"%",
      extra:"<div class='note'>월 카드매출 <b>"+F.kor(m)+"</b> 기준 수수료가 <b>"+F.won(mFee)+"</b> 입니다. "+
        "연간으로는 <b>"+F.kor(mFee*12)+"</b> 이므로, 우대수수료율 적용 여부를 반드시 확인하세요. "+
        "영세·중소가맹점은 매출 구간에 따라 낮은 우대요율이 적용됩니다.</div>"
    };
  }
});""",
    guide=u"""
<h3>실제로 입금되는 금액은 결제금액이 아닙니다</h3>
<p>손님이 5만원을 카드로 결제해도 가맹점 통장에 5만원이 들어오지 않습니다.
카드사 가맹점 수수료를 뺀 금액이 입금됩니다. 수수료율이 1.5%라면 750원이 빠져
49,250원이 들어옵니다.</p>

<h3>우대수수료율을 받고 있는지 확인하세요</h3>
<p>영세·중소가맹점은 연매출 구간에 따라 낮은 우대수수료율이 적용됩니다.
매출 규모가 바뀌었는데 요율이 그대로라면 손해를 보고 있을 수 있습니다.
여신금융협회나 거래 카드사에서 본인 가맹점의 적용 요율을 조회할 수 있고,
소급 환급을 받을 수 있는 경우도 있습니다.</p>

<h3>연 단위로 보면 금액이 달라 보입니다</h3>
<p>건당 750원은 작아 보이지만 월 카드매출 2,000만원에 1.5%면 월 30만원, 연 360만원입니다.
요율이 0.5%p만 낮아져도 연 120만원이 남습니다. 이 계산기의 월·연 수수료 항목이
그 규모를 보여줍니다.</p>

<h3>마진 계산에 수수료를 넣어야 합니다</h3>
<p>카드 결제 비중이 높은 업종에서 수수료를 원가에 넣지 않으면 실제 마진이
계산보다 낮게 나옵니다. <a href="../margin/">마진율 계산기</a>의 원가 항목에
수수료까지 반영하세요.</p>
""",
    faq=[
        (u"수수료 부가세는 무엇인가요?",
         u"가맹점 수수료에도 부가가치세가 붙는 구조입니다. 카드사 정산 방식에 따라 표시가 다르므로 "
         u"실제 정산내역서와 대조해 보시고, 포함/미포함을 골라 계산하세요."),
        (u"우대수수료율은 어떻게 확인하나요?",
         u"여신금융협회 가맹점 수수료 조회 서비스나 거래 중인 카드사 고객센터에서 확인할 수 있습니다. "
         u"매출 구간이 바뀌면 요율도 조정되므로 주기적으로 확인하는 편이 좋습니다."),
        (u"입금은 언제 되나요?",
         u"카드사와 결제대행사에 따라 다르며 보통 영업일 기준 2~5일이 걸립니다. "
         u"이 계산기는 금액만 계산하며 입금 일정은 다루지 않습니다."),
    ],
)

# ───────────────────────── 평수 ─────────────────────────
add(
    slug="pyeong", name=u"평수 계산기", group=u"부동산·생활",
    title=u"평수 계산기 | 평 ↔ 제곱미터(㎡) 변환",
    desc=u"평과 제곱미터를 서로 변환합니다. 공급면적과 전용면적 차이, 전용률도 함께 확인할 수 있습니다.",
    kw=u"평 ↔ ㎡ 변환, 전용률 확인",
    spec=u"""
Calc.mount({
  id:"pyeong",
  formTitle:"면적 입력",
  fields:[
    {k:"mode", label:"변환 방향", type:"seg", options:[
      {value:"p2m", label:"평 → ㎡"}, {value:"m2p", label:"㎡ → 평"}]},
    {k:"value", label:"면적", suffix:"", value:25, step:0.01, min:0},
    {k:"exclusive", label:"전용면적", sub:"전용률 계산용, 없으면 0", suffix:"㎡", value:0, step:0.01, min:0}
  ],
  compute:function(v,F){
    var P=3.3057851239669422, x=v.value||0, m2, py;
    if(v.mode==="m2p"){ m2=x; py=x/P; } else { py=x; m2=x*P; }
    var ex=v.exclusive||0;
    var rate = m2>0 && ex>0 ? ex/m2*100 : null;
    var stats=[
      {k:"제곱미터", v:F.num(m2,2)+" ㎡"},
      {k:"평", v:F.num(py,2)+" 평"},
      {k:"전용률", v: rate==null ? "—" : F.pct(rate,1), sub: rate==null?"전용면적 입력 시":"공급면적 대비"}
    ];
    return {
      hero:{k: v.mode==="m2p" ? "평" : "제곱미터",
            v: v.mode==="m2p" ? F.num(py,2)+" 평" : F.num(m2,2)+" ㎡",
            sub: v.mode==="m2p" ? F.num(m2,2)+" ㎡" : F.num(py,2)+" 평"},
      stats:stats,
      hint:"1평 = 3.3058㎡",
      extra:"<div class='note'>부동산 광고의 <b>84㎡</b> 는 흔히 <b>34평형</b>으로 불리지만, "+
        "84㎡ 는 <b>전용면적</b>이고 34평은 <b>공급면적</b> 기준이라 서로 다른 숫자입니다. "+
        "84㎡ 자체를 평으로 바꾸면 "+F.num(84/3.3057851239669422,1)+"평입니다.</div>"
    };
  }
});""",
    guide=u"""
<h3>1평은 정확히 몇 제곱미터인가</h3>
<p>1평 = 400/121 ㎡ = 약 3.3058㎡입니다. 반대로 1㎡는 약 0.3025평입니다.
간단히 <strong>㎡에 0.3025를 곱하면 평</strong>, <strong>평에 3.3058을 곱하면 ㎡</strong>입니다.</p>

<h3>84㎡가 왜 34평이라고 불리나</h3>
<p>혼동이 가장 많은 부분입니다. 84㎡를 그대로 평으로 바꾸면 25.4평입니다.
그런데 광고에서는 34평형이라고 합니다. 기준이 다르기 때문입니다.</p>
<ul>
<li><strong>전용면적</strong> — 현관문 안쪽, 실제로 우리 집만 쓰는 공간. 84㎡가 이것입니다.</li>
<li><strong>공급면적</strong> — 전용면적 + 계단·복도 등 주거공용면적. 34평은 이쪽 기준입니다.</li>
<li><strong>계약면적</strong> — 공급면적 + 지하주차장 등 기타공용면적.</li>
</ul>
<p>같은 84㎡라도 공용면적이 얼마나 붙느냐에 따라 체감 넓이가 달라집니다.</p>

<h3>전용률을 보면 실속을 알 수 있습니다</h3>
<p>전용률 = 전용면적 ÷ 공급면적입니다. 아파트는 보통 70~80%대이고,
오피스텔은 50%대까지 내려가기도 합니다. 전용률이 낮으면 같은 평형이라도
실제 사용하는 공간이 좁습니다. 계약서의 전용면적을 이 계산기에 넣으면
전용률이 바로 나옵니다.</p>

<h3>자주 쓰는 평형 환산</h3>
<div class="tablewrap"><table>
<thead><tr><th>전용면적</th><th>평 환산</th><th>흔히 부르는 이름</th></tr></thead>
<tbody>
<tr><td>39㎡</td><td class="n">11.8평</td><td>17평형</td></tr>
<tr><td>49㎡</td><td class="n">14.8평</td><td>21평형</td></tr>
<tr><td>59㎡</td><td class="n">17.8평</td><td>24~25평형</td></tr>
<tr><td>74㎡</td><td class="n">22.4평</td><td>30평형</td></tr>
<tr><td>84㎡</td><td class="n">25.4평</td><td>33~34평형</td></tr>
<tr><td>101㎡</td><td class="n">30.6평</td><td>40평형</td></tr>
</tbody></table></div>
<p>평형 이름은 단지마다 공용면적이 달라 차이가 납니다.</p>
""",
    faq=[
        (u"1평은 몇 제곱미터인가요?",
         u"약 3.3058㎡입니다. 정확히는 400/121 ㎡입니다."),
        (u"84㎡는 왜 34평이라고 하나요?",
         u"84㎡는 전용면적이고 34평은 공급면적 기준이기 때문입니다. 84㎡ 자체를 평으로 바꾸면 25.4평입니다."),
        (u"전용률은 어느 정도가 보통인가요?",
         u"아파트는 대체로 70~80%대, 오피스텔은 그보다 낮은 경우가 많습니다. "
         u"같은 평형이어도 전용률이 높을수록 실제 사용 공간이 넓습니다."),
    ],
)

# ───────────────────────── 날짜 ─────────────────────────
add(
    slug="date", name=u"날짜 계산기", group=u"부동산·생활",
    title=u"날짜 계산기 | 디데이·날짜 간 일수·N일 후 계산",
    desc=u"두 날짜 사이의 일수를 세거나, 기준일에서 N일 뒤·앞의 날짜를 계산합니다.",
    kw=u"디데이, 날짜 사이 일수, N일 후",
    spec=u"""
Calc.mount({
  id:"date",
  formTitle:"날짜 입력",
  fields:[
    {k:"mode", label:"계산 방식", type:"seg", options:[
      {value:"between", label:"두 날짜 사이"}, {value:"offset", label:"N일 후/전"}]},
    {k:"from", label:"기준일", type:"date", value:""},
    {k:"to", label:"대상일", sub:"두 날짜 사이에서 사용", type:"date", value:""},
    {k:"days", label:"더할 일수", sub:"음수면 이전 날짜", suffix:"일", value:100, step:1}
  ],
  compute:function(v,F){
    var D=24*3600*1000;
    var wd=["일","월","화","수","목","금","토"];
    function fmt(d){ return d.getFullYear()+"년 "+(d.getMonth()+1)+"월 "+d.getDate()+"일 ("+wd[d.getDay()]+")"; }
    var a = v.from ? new Date(v.from+"T00:00:00") : new Date(new Date().toDateString());
    if(isNaN(a)) a=new Date(new Date().toDateString());

    if(v.mode==="offset"){
      var n=v.days||0;
      var b=new Date(a.getTime()+n*D);
      return {
        hero:{k:(n>=0?"+":"")+F.num(n)+"일 뒤", v:fmt(b)},
        stats:[
          {k:"기준일", v:fmt(a)},
          {k:"경과", v:F.num(Math.abs(n))+"일", sub:F.num(Math.abs(n)/7,1)+"주"},
          {k:"개월 환산", v:F.num(Math.abs(n)/30.44,1)+"개월"}
        ],
        hint:"당일 포함하지 않음"
      };
    }
    var b2 = v.to ? new Date(v.to+"T00:00:00") : new Date(new Date().toDateString());
    if(isNaN(b2)) b2=new Date(new Date().toDateString());
    var diff=Math.round((b2-a)/D);
    var abs=Math.abs(diff);
    var y=Math.floor(abs/365), rem=abs%365, mm=Math.floor(rem/30.44);
    return {
      hero:{k: diff>=0 ? "남은 일수" : "지난 일수",
            v:F.num(abs)+"일", cls: diff>=0?"up":"down",
            sub:(diff>=0?"D-":"D+")+F.num(abs)},
      stats:[
        {k:"기준일", v:fmt(a)},
        {k:"대상일", v:fmt(b2)},
        {k:"환산", v:(y?y+"년 ":"")+mm+"개월", sub:F.num(abs/7,1)+"주"}
      ],
      hint:"당일 포함하지 않음",
      extra:"<div class='note'>당일을 포함해서 세려면 <b>"+F.num(abs+1)+"일</b> 입니다. "+
        "계약이나 법정 기간은 초일 산입 여부가 사안마다 달라, 실제 기한은 관련 규정을 확인하세요.</div>"
    };
  }
});""",
    guide=u"""
<h3>당일을 세느냐 마느냐</h3>
<p>날짜 계산에서 다툼이 생기는 지점입니다. 이 계산기는 기본적으로 <strong>당일을 빼고</strong>
셉니다. 1월 1일에서 1월 2일까지는 1일입니다. 당일을 포함하는 방식(초일 산입)으로 세면 2일이 됩니다.</p>
<p>민법에서는 기간을 일·주·월·년으로 정한 때 초일을 넣지 않는 것이 원칙이지만,
오전 0시부터 시작하는 경우나 개별 법령이 따로 정한 경우에는 초일을 넣습니다.
계약서상 기한이나 법정 기간은 해당 규정을 확인하셔야 합니다.</p>

<h3>디데이 표기</h3>
<p>아직 오지 않은 날은 D-숫자, 지나간 날은 D+숫자로 씁니다.
시험일이 30일 남았으면 D-30, 개업한 지 100일이 지났으면 D+100입니다.</p>

<h3>어디에 쓰나</h3>
<ul>
<li>계약 만료일까지 남은 기간 확인</li>
<li>수습 기간·계약직 종료일 계산</li>
<li>세금 신고 기한까지 남은 일수</li>
<li>기념일·기일 디데이</li>
<li>배송·정산 예정일에서 N일 뒤 날짜 뽑기</li>
</ul>
""",
    faq=[
        (u"당일이 포함되나요?",
         u"기본 계산은 당일을 빼고 셉니다. 결과 아래에 당일을 포함한 일수도 함께 표시하니 "
         u"필요한 쪽을 쓰시면 됩니다."),
        (u"공휴일과 주말을 뺀 영업일도 셀 수 있나요?",
         u"현재는 달력상 일수만 계산합니다. 영업일 계산은 공휴일 지정이 해마다 달라져 "
         u"별도 확인이 필요합니다."),
        (u"날짜를 비워두면 어떻게 되나요?",
         u"오늘 날짜가 기준으로 들어갑니다."),
    ],
)

# ───────────────────────── 주휴수당 ─────────────────────────
add(
    slug="juhyu", name=u"주휴수당 계산기", group=u"급여·노무",
    title=u"주휴수당 계산기 | 주휴수당 지급 조건과 금액 계산",
    desc=u"시급과 주 근로시간으로 주휴수당을 계산합니다. 주 15시간 기준과 월 환산 급여도 함께 확인합니다.",
    kw=u"시급·주 근로시간으로 주휴수당과 월급 환산",
    spec=u"""
Calc.mount({
  id:"juhyu",
  formTitle:"근로 조건",
  fields:[
    {k:"wage", label:"시급", sub:"최저임금은 해마다 바뀝니다", suffix:"원", value:10320, step:10, min:0},
    {k:"hours", label:"주 소정근로시간", sub:"실제 일하기로 정한 시간", suffix:"시간", value:15, step:0.5, min:0},
    {k:"weeks", label:"월 환산 주수", sub:"보통 4.345주", suffix:"주", value:4.345, step:0.001, min:0}
  ],
  compute:function(v,F){
    var w=v.wage||0, h=v.hours||0, wk=v.weeks||4.345;
    var eligible = h>=15;
    /* 주휴시간 = (주 소정근로시간 / 40) * 8, 주 40시간 초과분은 인정하지 않는다 */
    var paidHours = eligible ? Math.min(h,40)/40*8 : 0;
    var juhyu = paidHours*w;
    var basic = h*w;
    var weekTotal = basic+juhyu;
    return {
      hero:{k:"주휴수당 (주 1회)", v:F.kor(juhyu), sub:F.won(juhyu), cls: eligible?"up":"down"},
      stats:[
        {k:"주급 (기본)", v:F.won(basic)},
        {k:"주급 (주휴 포함)", v:F.won(weekTotal), cls:"up"},
        {k:"월 환산", v:F.won(weekTotal*wk), sub:F.num(wk,3)+"주 기준"}
      ],
      hint: eligible ? "주 "+F.num(h,1)+"시간 · 주휴시간 "+F.num(paidHours,2)+"시간"
                     : "주 15시간 미만은 지급 대상 아님",
      extra: eligible
        ? "<div class='note'>주 소정근로시간이 <b>15시간 이상</b>이고 그 주의 소정근로일을 "+
          "<b>개근</b>했다면 주휴수당이 발생합니다. 주휴시간은 (주 소정근로시간 ÷ 40) × 8 로 계산하며 "+
          "주 40시간을 넘는 부분은 인정되지 않습니다.</div>"
        : "<div class='note'>주 소정근로시간이 <b>15시간 미만</b>이면 주휴수당 지급 대상이 아닙니다. "+
          "여러 주의 근로시간이 들쭉날쭉하다면 4주를 평균해 판단합니다.</div>"
    };
  }
});""",
    guide=u"""
<h3>주휴수당은 언제 발생하나</h3>
<p>두 조건을 모두 만족해야 합니다.</p>
<ul>
<li>주 소정근로시간이 <strong>15시간 이상</strong>일 것</li>
<li>그 주의 <strong>소정근로일을 개근</strong>할 것</li>
</ul>
<p>소정근로시간은 실제로 일하기로 정한 시간입니다. 근로시간이 주마다 다르면
4주를 평균해서 판단합니다. 15시간에서 아슬아슬하게 걸치는 경우가 실무에서 분쟁이 잦습니다.</p>

<h3>계산식</h3>
<p><strong>주휴시간 = (주 소정근로시간 ÷ 40) × 8</strong>, <strong>주휴수당 = 주휴시간 × 시급</strong>입니다.
주 40시간을 넘게 일해도 주휴시간은 8시간이 상한입니다.</p>
<div class="tablewrap"><table>
<thead><tr><th>주 근로시간</th><th>주휴시간</th><th>시급 10,320원 기준</th></tr></thead>
<tbody>
<tr><td>15시간</td><td class="n">3.0시간</td><td class="n">30,960원</td></tr>
<tr><td>20시간</td><td class="n">4.0시간</td><td class="n">41,280원</td></tr>
<tr><td>30시간</td><td class="n">6.0시간</td><td class="n">61,920원</td></tr>
<tr><td>40시간</td><td class="n">8.0시간</td><td class="n">82,560원</td></tr>
</tbody></table></div>

<h3>월급에 이미 포함돼 있는 경우</h3>
<p>월급제 근로자의 급여에는 주휴수당이 포함돼 있는 것이 일반적입니다.
주 40시간 근로자의 월 소정근로시간을 209시간으로 잡는 것이 그래서입니다.
(40시간 + 주휴 8시간) × 4.345주 ≒ 209시간이기 때문입니다.
따라서 월급제라면 주휴수당을 따로 더 받는 것이 아니라 이미 들어 있는지를 확인해야 합니다.</p>

<h3>시급이 최저임금 아래로 내려가지 않는지</h3>
<p>최저임금은 해마다 고시로 바뀝니다. 이 계산기의 시급 칸은 직접 입력하도록 열어두었으니,
고용노동부가 고시한 당해 연도 최저임금을 확인해 넣으세요.
주휴수당까지 포함해 시간당 실질 임금을 계산하면 최저임금 위반 여부를 판단할 때 참고가 됩니다.</p>
""",
    faq=[
        (u"주 14시간이면 주휴수당을 못 받나요?",
         u"주 소정근로시간이 15시간 미만이면 지급 대상이 아닙니다. 다만 주마다 시간이 다르면 "
         u"4주 평균으로 판단하므로, 평균이 15시간을 넘는지 확인해 보세요."),
        (u"지각이나 조퇴를 하면 못 받나요?",
         u"개근은 소정근로일에 출근했는지를 보는 것이라, 지각·조퇴가 있어도 결근이 아니면 "
         u"개근으로 봅니다. 다만 사업장 규정과 사안에 따라 다를 수 있습니다."),
        (u"월급제인데 주휴수당을 따로 받아야 하나요?",
         u"월급에는 통상 주휴수당이 포함돼 있습니다. 주 40시간 근로자의 월 소정근로시간을 209시간으로 "
         u"잡는 것이 그 때문입니다. 급여명세서와 근로계약서를 확인해 보세요."),
        (u"최저임금이 기본값과 다릅니다.",
         u"최저임금은 해마다 바뀌어 기본값이 맞지 않을 수 있습니다. 시급 칸에 고용노동부 고시 금액을 "
         u"직접 넣어 계산하세요."),
    ],
)

# ───────────────────────── 대출 상환 ─────────────────────────
add(
    slug="loan", name=u"대출 이자 계산기", group=u"대출·예금",
    title=u"대출 이자 계산기 | 원리금균등·원금균등·만기일시 상환 비교",
    desc=u"주택담보대출·신용대출의 월 상환액과 총이자를 계산합니다. 원리금균등·원금균등·만기일시 세 방식을 비교하고 상환 스케줄을 확인할 수 있습니다.",
    kw=u"주담대·신용대출 월 상환액과 총이자, 상환 스케줄",
    spec=u"""
Calc.mount({
  id:"loan",
  formTitle:"대출 조건",
  fields:[
    {k:"principal", label:"대출금액", suffix:"원", value:300000000, step:1000000, min:0},
    {k:"rate", label:"연이자율", suffix:"%", value:4.5, step:0.01, min:0},
    {k:"months", label:"대출기간", suffix:"개월", value:360, step:1, min:1,
     note:"360개월 = 30년"},
    {k:"method", label:"상환방식", type:"select", value:"equal", options:[
      {value:"equal", label:"원리금균등"},
      {value:"principal", label:"원금균등"},
      {value:"bullet", label:"만기일시"}]},
    {k:"grace", label:"거치기간", sub:"이자만 내는 기간", suffix:"개월", value:0, step:1, min:0}
  ],
  compute:function(v,F){
    var P=v.principal||0, i=(v.rate||0)/100/12, n=Math.max(1,Math.round(v.months||1));
    var g=Math.min(Math.max(0,Math.round(v.grace||0)), n-1);
    var pay=n-g, bal=P, rows=[], totalInt=0, first=0;

    for(var m=1;m<=n;m++){
      var interest=bal*i, princ=0;
      if(m<=g){ princ=0; }
      else if(v.method==="bullet"){ princ = (m===n)?bal:0; }
      else if(v.method==="principal"){ princ = P/pay; }
      else {
        var A = i>0 ? P*i*Math.pow(1+i,pay)/(Math.pow(1+i,pay)-1) : P/pay;
        princ = A-interest;
        if(m===n) princ=bal;
      }
      if(princ>bal) princ=bal;
      var total=princ+interest;
      bal-=princ; totalInt+=interest;
      if(m===g+1) first=total;
      if(rows.length<600)
        rows.push([m+"회", F.won(princ), F.won(interest), F.won(total), F.won(Math.max(bal,0))]);
    }

    var label={equal:"원리금균등",principal:"원금균등",bullet:"만기일시"}[v.method];
    return {
      hero:{k: v.method==="principal" ? "첫 달 상환액" : "월 상환액",
            v:F.kor(first), sub:F.won(first)},
      stats:[
        {k:"총 이자", v:F.won(totalInt), cls:"down"},
        {k:"총 상환액", v:F.won(P+totalInt)},
        {k:"이자 비중", v:F.pct(P>0?totalInt/P*100:0,1), sub:"원금 대비"}
      ],
      hint:label+" · "+F.num(n)+"개월"+(g?" · 거치 "+F.num(g)+"개월":""),
      extra:"<div class='note'>"+
        (v.method==="principal"
          ? "원금균등은 첫 달이 가장 많고 매달 줄어듭니다. 마지막 달 상환액은 <b>"+F.won(P/pay*(1+0)+0)+"</b> 수준까지 내려갑니다."
          : v.method==="bullet"
            ? "만기일시는 매달 이자만 내다가 만기에 원금 <b>"+F.won(P)+"</b> 를 한 번에 갚습니다. 월 부담은 가장 작지만 총이자는 가장 큽니다."
            : "원리금균등은 매달 같은 금액을 냅니다. 초반에는 이자 비중이 크고 후반으로 갈수록 원금 비중이 커집니다.")
        +"</div>",
      cols:["회차","원금","이자","상환액","잔액"],
      rows:rows,
      tableHint: n>600 ? "앞 600회차만 표시" : F.num(n)+"회차"
    };
  }
});""",
    guide=u"""
<h3>상환방식에 따라 총이자가 크게 달라집니다</h3>
<p>3억원을 연 4.5%로 30년 빌린다고 할 때 방식별 차이입니다.</p>
<div class="tablewrap"><table>
<thead><tr><th>방식</th><th>첫 달</th><th>총이자</th><th>특징</th></tr></thead>
<tbody>
<tr><td>원리금균등</td><td class="n">약 152만원</td><td class="n">약 2억 4,722만원</td><td>매달 같은 금액</td></tr>
<tr><td>원금균등</td><td class="n">약 195만원</td><td class="n">약 2억 306만원</td><td>초반 부담 크고 점점 감소</td></tr>
<tr><td>만기일시</td><td class="n">약 112만원</td><td class="n">약 4억 500만원</td><td>월 부담 최소, 총이자 최대</td></tr>
</tbody></table></div>
<p>월 부담이 작을수록 총이자는 커집니다. 원금을 늦게 갚을수록 이자가 붙는 기간이 길어지기 때문입니다.</p>

<h3>원리금균등 — 가장 흔한 방식</h3>
<p>매달 내는 금액이 똑같아 자금 계획을 세우기 쉽습니다. 다만 <strong>초반에는 낸 돈의 대부분이 이자</strong>입니다.
위 조건에서 첫 달 152만원 중 이자가 112.5만원, 원금은 40만원이 채 안 됩니다.
5년을 갚아도 원금은 10% 남짓 줄어듭니다. 중도상환을 생각한다면 이 점을 알고 계셔야 합니다.</p>

<h3>거치기간의 함정</h3>
<p>거치기간에는 이자만 냅니다. 당장 부담은 줄지만 원금이 그대로 남아 있어
거치가 끝난 뒤 월 상환액이 올라가고 총이자도 늘어납니다.
거치기간 칸에 숫자를 넣어 총이자가 얼마나 늘어나는지 비교해 보세요.</p>

<h3>중도상환수수료</h3>
<p>대출을 일찍 갚으면 수수료가 붙는 경우가 있습니다. 보통 3년이 지나면 면제되고,
남은 기간에 비례해 줄어드는 구조(슬라이딩)가 일반적입니다.
이 계산기는 중도상환수수료를 반영하지 않으니 약정서를 확인하세요.</p>

<h3>변동금리라면</h3>
<p>이 계산기는 금리가 끝까지 그대로라고 가정합니다. 변동금리 대출은 기준금리 변동에 따라
상환액이 바뀝니다. 금리를 1%p 올려서 다시 계산해 보면 감당 가능한 수준인지 가늠할 수 있습니다.</p>
""",
    faq=[
        (u"원리금균등과 원금균등 중 어느 것이 유리한가요?",
         u"총이자만 보면 원금균등이 적습니다. 다만 초반 상환 부담이 크므로 현금 흐름을 함께 봐야 합니다. "
         u"두 방식을 각각 계산해 첫 달 금액과 총이자를 비교해 보세요."),
        (u"중도상환수수료도 계산되나요?",
         u"반영하지 않습니다. 상품마다 요율과 면제 조건이 달라 약정서를 확인하셔야 합니다."),
        (u"변동금리는 어떻게 확인하나요?",
         u"현재 금리로 한 번, 1~2%p 높인 금리로 한 번 계산해 상환액이 얼마나 늘어나는지 "
         u"비교해 보시는 방법을 권합니다."),
        (u"거치기간을 두면 왜 총이자가 늘어나나요?",
         u"거치기간에는 원금이 줄지 않아 그만큼 이자가 붙는 기간이 길어지기 때문입니다."),
    ],
)

# ───────────────────────── 예적금 ─────────────────────────
add(
    slug="deposit", name=u"예적금 계산기", group=u"대출·예금",
    title=u"예금 적금 계산기 | 만기 수령액과 세후 이자 계산",
    desc=u"정기예금과 정기적금의 만기 수령액을 계산합니다. 단리·복리, 이자소득세 15.4%를 반영합니다.",
    kw=u"정기예금·정기적금 만기 수령액과 세후 이자",
    spec=u"""
Calc.mount({
  id:"deposit",
  formTitle:"상품 조건",
  fields:[
    {k:"kind", label:"상품", type:"seg", options:[
      {value:"jeokgeum", label:"적금"}, {value:"yegeum", label:"예금"}]},
    {k:"amount", label:"금액", sub:"적금은 매월 납입액", suffix:"원", value:500000, step:10000, min:0},
    {k:"rate", label:"연이자율", suffix:"%", value:3.5, step:0.01, min:0},
    {k:"months", label:"기간", suffix:"개월", value:12, step:1, min:1},
    {k:"compound", label:"이자 방식", type:"seg", options:[
      {value:"simple", label:"단리"}, {value:"month", label:"월복리"}]},
    {k:"tax", label:"이자소득세", type:"seg", options:[
      {value:"15.4", label:"일반 15.4%"}, {value:"0", label:"비과세"}, {value:"9.5", label:"세금우대 9.5%"}]}
  ],
  compute:function(v,F){
    var a=v.amount||0, r=(v.rate||0)/100, n=Math.max(1,Math.round(v.months||1));
    var t=(+v.tax||0)/100, i=r/12, principal, gross;

    if(v.kind==="yegeum"){
      principal=a;
      gross = v.compound==="month" ? a*(Math.pow(1+i,n)-1) : a*r*(n/12);
    } else {
      principal=a*n;
      if(v.compound==="month"){
        /* 매월 말 납입, 남은 개월수만큼 월복리 */
        var s=0; for(var m=1;m<=n;m++) s+=a*Math.pow(1+i,n-m+1);
        gross=s-principal;
      } else {
        /* 첫 회차는 n개월, 마지막은 1개월치 이자 */
        gross = a*i*n*(n+1)/2;
      }
    }
    var tax=gross*t, net=gross-tax, total=principal+net;
    var eff = principal>0 ? net/principal*100 : 0;

    return {
      hero:{k:"만기 수령액", v:F.kor(total), sub:F.won(total), cls:"up"},
      stats:[
        {k:"납입 원금", v:F.won(principal), sub: v.kind==="jeokgeum" ? F.num(n)+"회 납입" : "일시 예치"},
        {k:"세후 이자", v:F.won(net), cls:"up", sub:"세금 "+F.won(tax)},
        {k:"원금 대비", v:F.pct(eff,2), sub:F.num(n)+"개월 총"}
      ],
      hint:(v.kind==="jeokgeum"?"적금":"예금")+" · 연 "+F.num(v.rate,2)+"% · "+
           (v.compound==="month"?"월복리":"단리"),
      extra: v.kind==="jeokgeum"
        ? "<div class='note'>적금 이자는 <b>납입한 시점부터</b> 붙습니다. 마지막 달에 넣은 돈은 한 달치 이자만 받습니다. "+
          "그래서 연 "+F.num(v.rate,2)+"% 적금의 원금 대비 실제 수익률은 <b>"+F.pct(eff,2)+"</b> 로, 표시금리의 절반 남짓입니다. "+
          "예금과 헷갈리기 쉬운 지점입니다.</div>"
        : "<div class='note'>예금은 목돈을 한 번에 맡겨 전 기간 이자가 붙습니다. "+
          "같은 금리라면 적금보다 원금 대비 수익률이 높게 나옵니다.</div>"
    };
  }
});""",
    guide=u"""
<h3>“연 3.5% 적금인데 왜 이자가 이것밖에 안 되나”</h3>
<p>가장 많이 하는 오해입니다. 매월 50만원씩 12개월 넣으면 원금은 600만원인데,
연 3.5%라고 600만원의 3.5%인 21만원을 기대하게 됩니다. 실제로는 세전 11만원 남짓입니다.</p>
<p>적금 이자는 <strong>돈을 넣은 시점부터</strong> 붙기 때문입니다.
첫 달에 넣은 50만원은 12개월치 이자를 받지만, 마지막 달에 넣은 50만원은 한 달치만 받습니다.
평균하면 절반 정도 기간만 이자가 붙는 셈이라, 원금 대비 실질 수익률은 표시금리의 절반 남짓입니다.</p>

<h3>예금과 적금은 같은 금리라도 결과가 다릅니다</h3>
<p>목돈 600만원을 연 3.5% 예금에 1년 넣으면 세전 21만원입니다.
같은 금리로 매월 50만원씩 적금하면 세전 11만원 정도입니다.
금리 숫자만 비교하면 안 되는 이유입니다.</p>

<h3>이자소득세 15.4%</h3>
<p>이자에는 소득세 14%와 지방소득세 1.4%를 더해 15.4%가 원천징수됩니다.
세전 이자 11만원이면 실제 손에 쥐는 것은 약 9만 3천원입니다.
계산기의 세금 항목에서 비과세·세금우대와 비교해 볼 수 있습니다.</p>

<h3>단리와 월복리</h3>
<p>대부분의 시중 예적금은 단리입니다. 월복리 상품은 이자가 다시 원금에 더해져
기간이 길수록 유리하지만, 1년 이하 상품에서는 차이가 크지 않습니다.
기간을 늘려가며 비교해 보시면 차이가 언제부터 벌어지는지 볼 수 있습니다.</p>

<h3>매매·투자 수익률과 헷갈리지 마세요</h3>
<p>예적금은 원금이 보장되고 이자가 확정됩니다. 반복 매매로 수익을 복리로 굴리는 것은
전혀 다른 성격이며 손실 가능성이 있습니다. 그 계산은
<a href="../bokri/">복리 계산기</a>에서 승률까지 반영해 확인하실 수 있습니다.</p>
""",
    faq=[
        (u"적금 이자가 생각보다 적습니다.",
         u"적금은 납입 시점부터 이자가 붙어, 마지막 달 납입금은 한 달치 이자만 받습니다. "
         u"원금 대비 실질 수익률이 표시금리의 절반 남짓인 것이 정상입니다."),
        (u"이자소득세는 왜 15.4%인가요?",
         u"소득세 14%에 지방소득세 1.4%(소득세의 10%)를 더한 값입니다."),
        (u"세금우대 9.5%는 누가 받나요?",
         u"조건은 제도와 시점에 따라 달라집니다. 가입하려는 금융기관에서 본인이 대상인지 확인하세요."),
        (u"중도해지하면 어떻게 되나요?",
         u"약정금리가 아니라 훨씬 낮은 중도해지이율이 적용됩니다. 이 계산기는 만기 유지를 전제로 합니다."),
    ],
)

# ───────────────────────── 4대보험 ─────────────────────────
add(
    slug="insurance", name=u"4대보험 계산기", group=u"급여·노무",
    title=u"4대보험 계산기 | 근로자·사업주 부담금 계산",
    desc=u"월 급여로 국민연금·건강보험·장기요양·고용보험의 근로자 부담금과 사업주 부담금을 계산합니다.",
    kw=u"국민연금·건강보험·고용보험 근로자/사업주 부담",
    spec=u"""
Calc.mount({
  id:"insurance",
  formTitle:"급여와 요율",
  sideNote:"요율은 해마다 바뀝니다. 국민건강보험공단·국민연금공단 고시를 확인해 값을 고쳐 쓰세요.",
  fields:[
    {k:"pay", label:"월 보수액", sub:"비과세 제외", suffix:"원", value:3000000, step:10000, min:0},
    {k:"pension", label:"국민연금", sub:"근로자 부담률", suffix:"%", value:4.5, step:0.01, min:0},
    {k:"health", label:"건강보험", sub:"근로자 부담률", suffix:"%", value:3.545, step:0.001, min:0},
    {k:"care", label:"장기요양", sub:"건강보험료 대비", suffix:"%", value:12.95, step:0.01, min:0},
    {k:"employ", label:"고용보험", sub:"근로자 부담률", suffix:"%", value:0.9, step:0.01, min:0},
    {k:"pensionMax", label:"국민연금 상한 기준소득", suffix:"원", value:6170000, step:10000, min:0}
  ],
  compute:function(v,F){
    var p=v.pay||0;
    var base=Math.min(p, v.pensionMax||p);
    var pension=Math.floor(base*(v.pension||0)/100/10)*10;
    var health=Math.floor(p*(v.health||0)/100/10)*10;
    var care=Math.floor(health*(v.care||0)/100/10)*10;
    var employ=Math.floor(p*(v.employ||0)/100/10)*10;
    var sum=pension+health+care+employ;
    var net=p-sum;
    /* 사업주는 연금·건강·장기요양이 같고 고용보험은 실업급여분 외에 고용안정 등이 더 붙는다 */
    var empSum=pension+health+care+employ;
    return {
      hero:{k:"근로자 공제 합계", v:F.kor(sum), sub:F.won(sum), cls:"down"},
      stats:[
        {k:"공제 후 급여", v:F.won(net), cls:"up", sub:"소득세 제외 전"},
        {k:"공제율", v:F.pct(p>0?sum/p*100:0,2)},
        {k:"사업주 부담(개략)", v:F.won(empSum), sub:"고용보험 추가분 별도"}
      ],
      hint:"월 보수 "+F.won(p),
      cols:["항목","근로자 부담","비고"],
      rows:[
        ["국민연금", F.won(pension), p>(v.pensionMax||0) ? "상한 적용" : F.num(v.pension,2)+"%"],
        ["건강보험", F.won(health), F.num(v.health,3)+"%"],
        ["장기요양", F.won(care), "건강보험료의 "+F.num(v.care,2)+"%"],
        ["고용보험", F.won(employ), F.num(v.employ,2)+"%"],
        ["합계", F.won(sum), F.pct(p>0?sum/p*100:0,2)]
      ],
      tableHint:"원 단위 절사",
      extra:"<div class='note'>국민연금은 기준소득월액에 <b>상한과 하한</b>이 있어 급여가 높아도 "+
        "일정 금액 이상은 더 내지 않습니다. 산재보험은 전액 사업주 부담이며 업종별 요율이 달라 "+
        "여기에 포함하지 않았습니다.</div>"
    };
  }
});""",
    guide=u"""
<h3>4대보험은 무엇으로 이루어져 있나</h3>
<ul>
<li><strong>국민연금</strong> — 근로자와 사업주가 절반씩 부담합니다. 기준소득월액에 상·하한이 있습니다.</li>
<li><strong>건강보험</strong> — 역시 절반씩 부담합니다.</li>
<li><strong>장기요양보험</strong> — 건강보험료에 일정 비율을 곱해 산정합니다. 급여에 직접 곱하는 것이 아닙니다.</li>
<li><strong>고용보험</strong> — 실업급여분은 근로자와 사업주가 나눠 내고, 고용안정·직업능력개발 사업분은 사업주만 부담합니다.</li>
<li><strong>산재보험</strong> — 전액 사업주 부담이며 업종별 요율이 크게 다릅니다.</li>
</ul>

<h3>장기요양보험료 계산을 자주 틀립니다</h3>
<p>장기요양보험료는 <strong>건강보험료에</strong> 요율을 곱합니다. 월급에 곱하는 것이 아닙니다.
건강보험료가 10만원이고 장기요양 요율이 12.95%라면 12,950원입니다.
월급 300만원에 12.95%를 곱해 38만원이 나온다면 계산이 잘못된 것입니다.</p>

<h3>국민연금 상한</h3>
<p>국민연금은 기준소득월액에 상한이 있어, 급여가 상한을 넘어도 보험료가 더 늘지 않습니다.
상한액은 해마다 조정되므로 계산기의 상한 칸을 당해 연도 고시액으로 맞춰 쓰세요.
급여가 높을수록 실효 공제율이 낮아지는 이유입니다.</p>

<h3>요율은 해마다 바뀝니다</h3>
<p>이 계산기의 요율은 모두 <strong>입력값</strong>으로 열어두었습니다.
국민건강보험공단·국민연금공단이 고시한 당해 연도 요율을 확인해 넣으시면
정확한 금액이 나옵니다. 기본값은 참고용입니다.</p>

<h3>실수령액을 보려면</h3>
<p>4대보험 외에 소득세와 지방소득세가 더 공제됩니다.
연봉 기준 실수령액은 <a href="../salary/">연봉 실수령액 계산기</a>에서 확인하세요.</p>
""",
    faq=[
        (u"요율 기본값이 실제와 다릅니다.",
         u"요율은 해마다 조정됩니다. 모든 요율을 입력값으로 열어두었으니 공단 고시 수치를 넣어 계산하세요."),
        (u"장기요양보험료가 이상하게 나옵니다.",
         u"장기요양보험료는 월급이 아니라 건강보험료에 요율을 곱합니다. 이 계산기는 그 방식으로 계산합니다."),
        (u"산재보험은 왜 없나요?",
         u"산재보험은 전액 사업주 부담이고 업종별 요율 차이가 커서 일률적으로 계산하기 어렵습니다. "
         u"근로복지공단에서 해당 업종 요율을 확인하세요."),
        (u"사업주 부담이 개략이라고 되어 있는 이유는?",
         u"고용보험은 실업급여분 외에 고용안정·직업능력개발 사업분이 사업장 규모에 따라 추가되기 때문입니다."),
    ],
)

# ───────────────────────── 연봉 실수령액 ─────────────────────────
add(
    slug="salary", name=u"연봉 실수령액 계산기", group=u"급여·노무",
    title=u"연봉 실수령액 계산기 | 4대보험·소득세 공제 후 월급",
    desc=u"연봉에서 4대보험과 소득세를 뺀 월 실수령액을 계산합니다. 부양가족과 비과세액을 반영합니다.",
    kw=u"연봉에서 4대보험·소득세 빼고 월 실수령액",
    spec=u"""
Calc.mount({
  id:"salary",
  formTitle:"급여 정보",
  sideNote:"소득세는 연말정산 기준 추정치입니다. 매월 원천징수되는 금액은 간이세액표에 따라 달라, 연말정산에서 정산됩니다.",
  fields:[
    {k:"annual", label:"연봉", sub:"세전", suffix:"원", value:40000000, step:1000000, min:0},
    {k:"nontax", label:"월 비과세액", sub:"식대 등", suffix:"원", value:200000, step:10000, min:0},
    {k:"family", label:"부양가족 수", sub:"본인 포함", suffix:"명", value:1, step:1, min:1},
    {k:"child", label:"20세 이하 자녀", suffix:"명", value:0, step:1, min:0}
  ],
  compute:function(v,F){
    var annual=v.annual||0, monthly=annual/12;
    var nontax=Math.min(v.nontax||0, monthly);
    var taxableM=monthly-nontax;                 /* 보험료 부과 기준 */
    var totalPay=annual-nontax*12;               /* 총급여 (과세대상) */

    /* 4대보험 (근로자 부담, 기본 요율) */
    var pensionBase=Math.min(taxableM,6170000);
    var pension=Math.floor(pensionBase*0.045/10)*10;
    var health=Math.floor(taxableM*0.03545/10)*10;
    var care=Math.floor(health*0.1295/10)*10;
    var employ=Math.floor(taxableM*0.009/10)*10;
    var ins=pension+health+care+employ;

    /* 근로소득공제 */
    var g=totalPay, wd;
    if(g<=5000000) wd=g*0.7;
    else if(g<=15000000) wd=3500000+(g-5000000)*0.4;
    else if(g<=45000000) wd=7500000+(g-15000000)*0.15;
    else if(g<=100000000) wd=12000000+(g-45000000)*0.05;
    else wd=14750000+(g-100000000)*0.02;
    wd=Math.min(wd,20000000);

    /* 인적공제 + 보험료공제 */
    var personal=1500000*Math.max(1,v.family||1);
    var childCredit=(v.child||0)>0 ? ((v.child==1)?150000:(v.child==2)?350000:350000+(v.child-2)*300000) : 0;
    var deduction=personal+ins*12;
    var taxBase=Math.max(0, g-wd-deduction);

    /* 종합소득세율 (누진공제) */
    function calcTax(b){
      var t=[[14000000,.06,0],[50000000,.15,1260000],[88000000,.24,5760000],
             [150000000,.35,15440000],[300000000,.38,19940000],[500000000,.40,25940000],
             [1000000000,.42,35940000],[Infinity,.45,65940000]];
      for(var i=0;i<t.length;i++) if(b<=t[i][0]) return b*t[i][1]-t[i][2];
      return 0;
    }
    var gross=Math.max(0,calcTax(taxBase));

    /* 근로소득세액공제 */
    var credit = gross<=1300000 ? gross*0.55 : 715000+(gross-1300000)*0.30;
    var cap = g<=33000000 ? 740000
            : g<=70000000 ? Math.max(660000, 740000-(g-33000000)*0.008)
            : Math.max(500000, 660000-(g-70000000)*0.005);
    credit=Math.min(credit,cap);
    var income=Math.max(0, gross-credit-childCredit);
    var local=income*0.1;
    var taxYear=income+local;

    var deductM=ins+taxYear/12;
    var netM=monthly-deductM;

    return {
      hero:{k:"월 실수령액", v:F.kor(netM), sub:F.won(netM), cls:"up"},
      stats:[
        {k:"세전 월급", v:F.won(monthly)},
        {k:"월 공제액", v:F.won(deductM), cls:"down", sub:F.pct(monthly>0?deductM/monthly*100:0,1)},
        {k:"연 실수령", v:F.won(netM*12)}
      ],
      hint:"연봉 "+F.kor(annual)+" · 부양 "+F.num(v.family)+"명",
      cols:["항목","월","연"],
      rows:[
        ["국민연금", F.won(pension), F.won(pension*12)],
        ["건강보험", F.won(health), F.won(health*12)],
        ["장기요양", F.won(care), F.won(care*12)],
        ["고용보험", F.won(employ), F.won(employ*12)],
        ["소득세", F.won(income/12), F.won(income)],
        ["지방소득세", F.won(local/12), F.won(local)],
        ["공제 합계", F.won(deductM), F.won(deductM*12)],
        ["실수령", F.won(netM), F.won(netM*12)]
      ],
      extra:"<div class='note'>비과세 <b>"+F.won(nontax)+"</b> 는 보험료와 소득세 계산에서 빠집니다. "+
        "소득세는 <b>연말정산 기준 추정치</b>이며, 실제 매월 원천징수액은 간이세액표를 따릅니다. "+
        "의료비·기부금·연금저축 등 추가 공제는 반영하지 않았습니다.</div>"
    };
  }
});""",
    guide=u"""
<h3>연봉과 실수령액은 왜 이렇게 차이가 나나</h3>
<p>세전 연봉에서 <strong>4대보험</strong>과 <strong>소득세·지방소득세</strong>가 빠집니다.
연봉 4,000만원이면 월 세전 333만원이지만 실수령은 290만원 안팎입니다.
공제율은 대체로 10~15% 수준이고 연봉이 높을수록 커집니다.</p>

<h3>비과세액은 왜 중요한가</h3>
<p>식대처럼 비과세로 처리되는 항목은 <strong>보험료와 소득세 계산에서 아예 빠집니다.</strong>
같은 연봉이라도 비과세 항목이 많으면 실수령액이 늘어납니다.
계약할 때 총액만 보지 말고 비과세 구성도 확인할 이유입니다.</p>

<h3>부양가족이 늘면 세금이 줄어듭니다</h3>
<p>기본공제는 1인당 150만원입니다. 여기에 자녀세액공제가 더해집니다.
부양가족 수를 바꿔가며 계산해 보시면 차이를 확인할 수 있습니다.
다만 부양가족으로 올리려면 소득·나이 요건을 충족해야 합니다.</p>

<h3>매월 떼는 세금과 연말정산은 다릅니다</h3>
<p>회사가 매월 떼는 소득세는 <strong>간이세액표</strong>에 따른 개략적인 선납입니다.
연말정산에서 실제 세액을 계산해 더 냈으면 돌려받고 덜 냈으면 더 냅니다.
이 계산기는 <strong>연말정산 기준</strong>으로 연간 세액을 추정한 뒤 12로 나눠 보여줍니다.
그래서 급여명세서의 소득세와 정확히 일치하지 않을 수 있습니다.</p>

<h3>반영하지 않은 것</h3>
<p>의료비·교육비·기부금·신용카드 사용액·연금저축·주택자금 등 개인별 공제는 넣지 않았습니다.
이런 공제가 많으면 실제 세금은 이 계산보다 줄어듭니다.
정확한 금액은 국세청 홈택스 연말정산 미리보기에서 확인하세요.</p>
""",
    faq=[
        (u"급여명세서의 소득세와 다릅니다.",
         u"매월 원천징수되는 소득세는 간이세액표 기준의 선납이고, 이 계산기는 연말정산 기준으로 "
         u"연간 세액을 추정합니다. 연말정산을 거치면 차액이 정산됩니다."),
        (u"비과세액은 얼마로 넣어야 하나요?",
         u"식대는 급여명세서에 별도 표시되는 경우가 많습니다. 회사 규정과 명세서를 확인해 넣으세요."),
        (u"부양가족은 누구까지 넣나요?",
         u"본인을 포함해 소득·나이 요건을 충족하는 가족입니다. 요건은 국세청 기준을 확인하세요."),
        (u"4대보험 요율을 바꿀 수 있나요?",
         u"이 계산기는 기본 요율로 고정돼 있습니다. 요율을 직접 조정하려면 "
         u"4대보험 계산기를 이용하세요."),
    ],
)

# ───────────────────────── 퇴직금 ─────────────────────────
add(
    slug="severance", name=u"퇴직금 계산기", group=u"급여·노무",
    title=u"퇴직금 계산기 | 평균임금 기준 퇴직금 계산",
    desc=u"입사일과 퇴사일, 최근 3개월 급여로 퇴직금을 계산합니다. 상여금과 연차수당을 반영합니다.",
    kw=u"재직기간과 평균임금으로 퇴직금 산정",
    spec=u"""
Calc.mount({
  id:"severance",
  formTitle:"재직 정보",
  fields:[
    {k:"join", label:"입사일", type:"date", value:"2021-03-02"},
    {k:"leave", label:"퇴사일", sub:"마지막 근무일 다음날", type:"date", value:"2026-03-02"},
    {k:"pay3", label:"최근 3개월 급여 합계", sub:"세전", suffix:"원", value:9000000, step:100000, min:0},
    {k:"bonus", label:"연간 상여금", suffix:"원", value:0, step:100000, min:0},
    {k:"annual", label:"연차수당", sub:"전년도 지급분", suffix:"원", value:0, step:100000, min:0}
  ],
  compute:function(v,F){
    var D=24*3600*1000;
    var a=new Date((v.join||"2021-01-01")+"T00:00:00");
    var b=new Date((v.leave||"2026-01-01")+"T00:00:00");
    if(isNaN(a)||isNaN(b)) return {hero:{k:"오류",v:"날짜를 확인해 주세요"}};
    var days=Math.round((b-a)/D);
    if(days<=0) return {hero:{k:"오류",v:"퇴사일이 입사일보다 빨라야 합니다"}};

    /* 평균임금 = (3개월 임금 + 상여 3/12 + 연차수당 3/12) / 3개월 일수 */
    var span=Math.round((b-new Date(b.getFullYear(),b.getMonth()-3,b.getDate()))/D);
    var base=(v.pay3||0)+(v.bonus||0)*3/12+(v.annual||0)*3/12;
    var avgDaily=span>0?base/span:0;
    var eligible=days>=365;
    var pay=eligible ? avgDaily*30*(days/365) : 0;
    var years=Math.floor(days/365), rest=days%365;

    return {
      hero:{k:"예상 퇴직금", v:F.kor(pay), sub:F.won(pay), cls: eligible?"up":"down"},
      stats:[
        {k:"재직기간", v:years+"년 "+Math.floor(rest/30)+"개월", sub:F.num(days)+"일"},
        {k:"1일 평균임금", v:F.won(avgDaily)},
        {k:"30일분", v:F.won(avgDaily*30), sub:"1년 근속 기준"}
      ],
      hint: eligible ? F.num(days)+"일 근속" : "1년 미만은 지급 대상 아님",
      extra: eligible
        ? "<div class='note'>퇴직금 = <b>1일 평균임금 × 30일 × (재직일수 ÷ 365)</b> 입니다. "+
          "평균임금이 통상임금보다 낮으면 <b>통상임금</b>으로 계산합니다. "+
          "실제 지급액은 회사 규정과 퇴직연금 제도(DB·DC)에 따라 달라질 수 있습니다.</div>"
        : "<div class='note'>계속근로기간이 <b>1년 미만</b>이면 법정 퇴직금 지급 대상이 아닙니다. "+
          "주 15시간 미만 근로자도 제외됩니다.</div>"
    };
  }
});""",
    guide=u"""
<h3>퇴직금 계산식</h3>
<p><strong>퇴직금 = 1일 평균임금 × 30일 × (재직일수 ÷ 365)</strong></p>
<p>대략 <em>1년에 한 달치 월급</em>이라고 생각하면 맞습니다. 3년 일했으면 석 달치 정도입니다.</p>

<h3>평균임금이란</h3>
<p>퇴직 직전 <strong>3개월간 받은 임금 총액</strong>을 그 기간의 <strong>총 일수</strong>로 나눈 값입니다.
여기에 연간 상여금의 3/12, 전년도 연차수당의 3/12를 더해 넣습니다.
기본급만이 아니라 정기적으로 지급된 수당이 포함됩니다.</p>
<p>주의할 점은 나누는 값이 <strong>근무일수가 아니라 달력상 총일수</strong>라는 것입니다.
3개월이 92일이면 92로 나눕니다.</p>

<h3>평균임금과 통상임금 중 큰 쪽</h3>
<p>평균임금이 통상임금보다 적으면 <strong>통상임금</strong>으로 계산합니다.
퇴직 직전 3개월에 무급휴직이나 결근이 있어 급여가 적었다면 이 규정이 적용될 수 있습니다.
이 계산기는 평균임금 기준으로만 계산하니, 그런 경우 통상임금과 비교해 보셔야 합니다.</p>

<h3>1년 미만이면 못 받습니다</h3>
<p>계속근로기간이 1년 미만이면 법정 퇴직금 지급 대상이 아닙니다.
주 소정근로시간이 15시간 미만인 경우도 제외됩니다.
1년을 며칠 앞두고 퇴사하면 퇴직금이 0이 되므로 날짜를 확인해 보세요.</p>

<h3>퇴직연금(DB·DC)이면 다를 수 있습니다</h3>
<p>확정급여형(DB)은 위 계산과 유사하지만, 확정기여형(DC)은 회사가 매년 납입한 부담금과
운용수익에 따라 금액이 달라집니다. DC형이라면 이 계산 결과와 실제 수령액이 다릅니다.</p>

<h3>퇴직소득세</h3>
<p>퇴직금에는 퇴직소득세가 부과됩니다. 근속연수에 따른 공제가 커서 일반 소득세보다 부담이 적고,
근속기간이 길수록 실효세율이 낮아집니다. 이 계산기는 세전 금액을 보여줍니다.</p>
""",
    faq=[
        (u"퇴사일은 언제로 넣나요?",
         u"마지막 근무일의 다음날을 넣습니다. 12월 31일까지 근무했다면 다음 해 1월 1일입니다."),
        (u"3개월 급여에 무엇을 포함하나요?",
         u"기본급과 정기적으로 지급된 수당을 포함한 세전 총액입니다. 상여금과 연차수당은 별도 칸에 "
         u"연간 금액으로 넣으면 3/12만 반영됩니다."),
        (u"1년에서 며칠 모자랍니다.",
         u"계속근로기간이 1년 미만이면 법정 퇴직금 대상이 아닙니다. 하루 차이로 갈리므로 "
         u"입사일과 퇴사일을 정확히 확인하세요."),
        (u"실제 받은 금액과 다릅니다.",
         u"퇴직연금 제도(DB·DC), 회사 규정, 통상임금 적용 여부, 퇴직소득세에 따라 달라집니다. "
         u"이 계산은 법정 최저 기준의 세전 추정치입니다."),
    ],
)

# ───────────────────────── 전월세 전환 ─────────────────────────
add(
    slug="jeonwolse", name=u"전월세 전환 계산기", group=u"부동산·생활",
    title=u"전월세 전환 계산기 | 전세를 월세로, 월세를 전세로 환산",
    desc=u"전월세 전환율로 전세보증금을 월세로 바꾸거나, 월세를 전세로 환산합니다.",
    kw=u"전세↔월세 환산, 전환율 역산",
    spec=u"""
Calc.mount({
  id:"jeonwolse",
  formTitle:"전환 조건",
  fields:[
    {k:"mode", label:"계산 방향", type:"seg", options:[
      {value:"toMonthly", label:"전세 → 월세"},
      {value:"toJeonse", label:"월세 → 전세"},
      {value:"findRate", label:"전환율 구하기"}]},
    {k:"jeonse", label:"전세보증금", suffix:"원", value:300000000, step:10000000, min:0},
    {k:"deposit", label:"월세보증금", suffix:"원", value:50000000, step:1000000, min:0},
    {k:"monthly", label:"월세", sub:"월세→전세, 전환율 구하기에서 사용", suffix:"원", value:1000000, step:50000, min:0},
    {k:"rate", label:"전환율", sub:"연", suffix:"%", value:5.5, step:0.1, min:0}
  ],
  compute:function(v,F){
    var J=v.jeonse||0, D=v.deposit||0, M=v.monthly||0, r=(v.rate||0)/100;
    var hero, stats, note;

    if(v.mode==="toMonthly"){
      var gap=Math.max(0,J-D);
      var m=gap*r/12;
      hero={k:"환산 월세", v:F.kor(m), sub:F.won(m)};
      stats=[{k:"보증금", v:F.won(D)},
             {k:"전환 대상 금액", v:F.won(gap), sub:"전세 − 보증금"},
             {k:"연 월세 합계", v:F.won(m*12)}];
      note="보증금 <b>"+F.won(D)+"</b> 에 월세 <b>"+F.won(m)+"</b> 조건이 전세 <b>"+F.kor(J)+"</b> 와 같은 값입니다.";
    } else if(v.mode==="toJeonse"){
      var j = r>0 ? D + M*12/r : D;
      hero={k:"환산 전세보증금", v:F.kor(j), sub:F.won(j)};
      stats=[{k:"월세보증금", v:F.won(D)},
             {k:"월세 환산분", v:F.won(j-D)},
             {k:"연 월세", v:F.won(M*12)}];
      note="보증금 <b>"+F.won(D)+"</b> + 월세 <b>"+F.won(M)+"</b> 는 전세 <b>"+F.kor(j)+"</b> 에 해당합니다.";
    } else {
      var gap2=Math.max(0,J-D);
      var rr = gap2>0 ? M*12/gap2*100 : 0;
      hero={k:"전환율 (연)", v:F.pct(rr,2), cls: rr>6?"down":"up"};
      stats=[{k:"전환 대상 금액", v:F.won(gap2)},
             {k:"연 월세", v:F.won(M*12)},
             {k:"월세", v:F.won(M)}];
      note="이 조건의 실제 전환율은 <b>"+F.pct(rr,2)+"</b> 입니다. 숫자가 높을수록 세입자에게 불리합니다.";
    }
    return {hero:hero, stats:stats, hint:"전환율 "+F.num(v.rate,2)+"%",
            extra:"<div class='note'>"+note+"<br><br>주택임대차보호법은 전세를 월세로 전환할 때 "+
              "<b>전환율 상한</b>을 두고 있습니다. 상한은 기준금리에 연동돼 바뀌므로 계약 시점의 기준을 확인하세요. "+
              "이 상한은 기존 계약을 전환하는 경우에 적용되며, 신규 계약에는 그대로 적용되지 않습니다.</div>"};
  }
});""",
    guide=u"""
<h3>전월세 전환율이란</h3>
<p>전세보증금을 월세로 바꿀 때 적용하는 <strong>연 이율</strong>입니다.</p>
<p><strong>월세 = (전세보증금 − 월세보증금) × 전환율 ÷ 12</strong></p>
<p>전세 3억, 보증금 5,000만원, 전환율 5.5%라면
(3억 − 5,000만) × 5.5% ÷ 12 = 약 115만원이 월세가 됩니다.</p>

<h3>전환율이 높을수록 세입자가 불리합니다</h3>
<p>같은 전세금이라도 전환율이 4%면 월세 83만원, 6%면 125만원입니다.
집주인 입장에서는 전환율이 높을수록 유리하고 세입자는 반대입니다.
계약 조건을 비교할 때 ‘전환율 구하기’ 모드로 실제 몇 %인지 확인해 보세요.</p>

<h3>법정 상한</h3>
<p>주택임대차보호법은 기존 계약을 전세에서 월세로 전환할 때 전환율 상한을 정하고 있습니다.
한국은행 기준금리에 연동돼 바뀌므로 계약 시점의 수치를 확인해야 합니다.
다만 이 상한은 <strong>존속 중인 계약을 전환</strong>하는 경우에 적용되고,
새로 맺는 계약에는 그대로 적용되지 않습니다.</p>

<h3>월세와 전세 중 무엇이 유리한가</h3>
<p>단순 비교는 <strong>전환율과 대출금리</strong>를 견주는 것입니다.
전세대출 금리가 전환율보다 낮으면 전세가, 높으면 월세가 유리할 수 있습니다.
전세 3억을 위해 연 4% 대출을 받으면 이자가 월 100만원인데
월세가 115만원이라면 전세 쪽이 낫습니다.
<a href="../loan/">대출 이자 계산기</a>로 실제 이자를 계산해 비교해 보세요.</p>
<p>다만 전세는 보증금 반환 위험이, 월세는 목돈이 묶이지 않는다는 차이가 있어
금액만으로 결정할 문제는 아닙니다.</p>
""",
    faq=[
        (u"전환율은 얼마가 적정한가요?",
         u"시장 상황과 지역에 따라 다릅니다. 법정 상한은 기준금리에 연동돼 바뀌므로 "
         u"계약 시점의 기준을 확인하세요."),
        (u"법정 상한을 넘는 계약은 무효인가요?",
         u"상한 규정은 존속 중인 계약을 전환하는 경우에 적용됩니다. 신규 계약은 다르게 다뤄지므로 "
         u"구체적인 사안은 전문가 상담을 권합니다."),
        (u"반전세는 어떻게 계산하나요?",
         u"월세보증금 칸에 실제 보증금을 넣으면 됩니다. 나머지 차액만 월세로 환산됩니다."),
    ],
)

# ───────────────────────── 중개보수 ─────────────────────────
add(
    slug="brokerage", name=u"부동산 중개보수 계산기", group=u"부동산·생활",
    title=u"부동산 중개수수료 계산기 | 매매·임대차 중개보수 상한",
    desc=u"거래금액에 따른 부동산 중개보수 상한을 계산합니다. 매매와 임대차, 주택과 오피스텔을 구분합니다.",
    kw=u"매매·임대차 거래금액별 중개보수 상한",
    spec=u"""
Calc.mount({
  id:"brokerage",
  formTitle:"거래 정보",
  sideNote:"요율은 지방자치단체 조례로 정해져 지역에 따라 다를 수 있습니다. 해당 시·도 조례를 확인하세요.",
  fields:[
    {k:"type", label:"거래 유형", type:"seg", options:[
      {value:"sale", label:"매매·교환"}, {value:"rent", label:"임대차"}]},
    {k:"price", label:"거래금액", sub:"매매가 또는 보증금", suffix:"원", value:500000000, step:10000000, min:0},
    {k:"monthly", label:"월세", sub:"임대차에서만 사용", suffix:"원", value:0, step:50000, min:0},
    {k:"vat", label:"부가세", type:"seg", options:[
      {value:"0", label:"별도"}, {value:"1", label:"10% 포함"}]}
  ],
  compute:function(v,F){
    var isRent=v.type==="rent", dep=v.price||0, m=v.monthly||0;
    /* 임대차 거래금액 = 보증금 + 월세×100, 5천만원 미만이면 월세×70 */
    var amount = isRent ? (function(){
      var a=dep+m*100;
      if(a<50000000) a=dep+m*70;
      return a;
    })() : dep;

    var table = isRent
      ? [[50000000,0.005,200000],[100000000,0.004,300000],[600000000,0.003,null],
         [1200000000,0.004,null],[1500000000,0.005,null],[Infinity,0.007,null]]
      : [[50000000,0.006,250000],[200000000,0.005,800000],[900000000,0.004,null],
         [1200000000,0.005,null],[1500000000,0.006,null],[Infinity,0.007,null]];

    var rate=0, cap=null;
    for(var i=0;i<table.length;i++){
      if(amount<table[i][0]){ rate=table[i][1]; cap=table[i][2]; break; }
    }
    var fee=amount*rate;
    if(cap!=null) fee=Math.min(fee,cap);
    var vat = v.vat==1 ? fee*0.1 : 0;

    return {
      hero:{k:"중개보수 상한", v:F.kor(fee+vat), sub:F.won(fee+vat), cls:"down"},
      stats:[
        {k:"적용 요율", v:F.pct(rate*100,2), sub: cap!=null ? "한도 "+F.won(cap) : "한도 없음"},
        {k:"산정 거래금액", v:F.won(amount), sub: isRent ? "보증금+월세 환산" : "매매가"},
        {k:"부가세", v: v.vat==1 ? F.won(vat) : "별도", cls:"down"}
      ],
      hint:(isRent?"임대차":"매매")+" · "+F.kor(amount),
      extra:"<div class='note'>표시된 금액은 <b>상한</b>이며 실제 보수는 중개사와 협의해 정합니다. "+
        (isRent ? "임대차 거래금액은 <b>보증금 + 월세×100</b> 으로 계산하고, 그 값이 5천만원 미만이면 "+
                  "<b>보증금 + 월세×70</b> 을 적용합니다. " : "")+
        "요율은 지자체 조례로 정해져 지역·물건 종류(주택/오피스텔/상가)에 따라 다릅니다.</div>"
    };
  }
});""",
    guide=u"""
<h3>중개보수는 “상한”입니다</h3>
<p>법정 요율은 <strong>최대 이만큼까지 받을 수 있다</strong>는 상한이지 정해진 금액이 아닙니다.
실제 보수는 중개사와 협의해 정하며, 계약 전에 합의하는 것이 원칙입니다.
계약서에 보수 금액을 명시해 두는 편이 분쟁을 막습니다.</p>

<h3>임대차 거래금액 계산이 따로 있습니다</h3>
<p>월세 계약은 보증금만으로 계산하지 않습니다.</p>
<p><strong>거래금액 = 보증금 + (월세 × 100)</strong></p>
<p>다만 이렇게 계산한 금액이 5,000만원 미만이면 <strong>보증금 + (월세 × 70)</strong>을 적용합니다.
보증금 1,000만원에 월세 50만원이면 1,000만 + 5,000만 = 6,000만원이 거래금액입니다.</p>

<h3>구간별 요율</h3>
<div class="tablewrap"><table>
<thead><tr><th>거래금액</th><th>매매·교환</th><th>임대차</th></tr></thead>
<tbody>
<tr><td>5천만원 미만</td><td class="n">0.6% (최대 25만원)</td><td class="n">0.5% (최대 20만원)</td></tr>
<tr><td>5천만~2억</td><td class="n">0.5% (최대 80만원)</td><td class="n">0.4% (최대 30만원)</td></tr>
<tr><td>2억~6억</td><td class="n">0.4%</td><td class="n">0.3%</td></tr>
<tr><td>6억~9억</td><td class="n">0.4%</td><td class="n">0.4%</td></tr>
<tr><td>9억~12억</td><td class="n">0.5%</td><td class="n">0.4%</td></tr>
<tr><td>12억~15억</td><td class="n">0.6%</td><td class="n">0.5%</td></tr>
<tr><td>15억 이상</td><td class="n">0.7%</td><td class="n">0.6%</td></tr>
</tbody></table></div>
<p>주택 기준이며 <strong>지방자치단체 조례로 정해져 지역에 따라 다를 수 있습니다.</strong>
오피스텔은 요건에 따라 별도 요율이, 상가·토지는 협의 요율(최대 0.9%)이 적용됩니다.</p>

<h3>부가가치세</h3>
<p>중개사가 일반과세자면 보수에 부가세 10%가 붙습니다. 간이과세자는 다를 수 있으니
사업자 유형을 확인하세요. 계산기의 부가세 항목으로 포함·별도를 비교할 수 있습니다.</p>

<h3>양쪽에서 받습니다</h3>
<p>중개보수는 매도인과 매수인(또는 임대인과 임차인) <strong>각각</strong>에게서 받습니다.
표시된 금액은 한쪽이 내는 금액입니다.</p>
""",
    faq=[
        (u"계산된 금액을 반드시 내야 하나요?",
         u"아닙니다. 법정 요율은 상한이며 실제 보수는 협의해 정합니다. 계약 전에 합의하고 "
         u"금액을 명시해 두시는 편이 좋습니다."),
        (u"월세 계약은 왜 보증금만으로 계산하지 않나요?",
         u"임대차 거래금액은 보증금 + 월세×100 으로 산정합니다. 그 값이 5천만원 미만이면 "
         u"보증금 + 월세×70 을 적용합니다."),
        (u"오피스텔도 같은 요율인가요?",
         u"오피스텔은 면적과 설비 요건에 따라 주택 요율이 적용되기도 하고 별도 요율이 적용되기도 합니다. "
         u"해당 물건의 요건을 확인하세요."),
        (u"지역마다 다른가요?",
         u"요율은 지방자치단체 조례로 정해져 지역에 따라 차이가 있을 수 있습니다. "
         u"해당 시·도 조례를 확인하세요."),
    ],
)

# ───────────────────────── 연차 개수 ─────────────────────────
add(
    slug="yeoncha", name=u"연차 개수 계산기", group=u"급여·노무",
    title=u"연차 계산기 | 입사일 기준 연차 개수와 가산 연차",
    desc=u"입사일과 기준일로 발생한 연차휴가 일수를 계산합니다. 1년 미만 월차와 3년 이상 가산 연차를 반영합니다.",
    kw=u"입사일 기준 연차 일수와 가산 연차",
    spec=u"""
Calc.mount({
  id:"yeoncha",
  formTitle:"재직 정보",
  fields:[
    {k:"join", label:"입사일", type:"date", value:"2022-03-02"},
    {k:"base", label:"기준일", sub:"비우면 오늘", type:"date", value:""},
    {k:"rate", label:"통상시급", sub:"미사용 연차수당 계산용", suffix:"원", value:0, step:100, min:0},
    {k:"hours", label:"1일 근로시간", suffix:"시간", value:8, step:0.5, min:0}
  ],
  compute:function(v,F){
    var D=24*3600*1000;
    var a=new Date((v.join||"2022-01-01")+"T00:00:00");
    var b=v.base ? new Date(v.base+"T00:00:00") : new Date(new Date().toDateString());
    if(isNaN(a)||isNaN(b)||b<a) return {hero:{k:"오류",v:"날짜를 확인해 주세요"}};

    var days=Math.round((b-a)/D);
    var years=Math.floor(days/365);
    var months=Math.floor(days/30.44);

    var monthly=0, annual=0, added=0;
    if(years<1){
      /* 1년 미만: 1개월 개근마다 1일, 최대 11일 */
      monthly=Math.min(11, Math.floor(days/30.44));
    } else {
      annual=15;
      /* 3년차부터 2년마다 1일 가산, 총 25일 상한 */
      if(years>=3) added=Math.min(10, Math.floor((years-1)/2));
      annual=Math.min(25, 15+added);
    }
    var total=years<1 ? monthly : annual;
    var pay=(v.rate||0)*(v.hours||8)*total;

    return {
      hero:{k: years<1 ? "발생한 연차 (1년 미만)" : years+"년차 연차",
            v:F.num(total)+"일", cls:"up",
            sub: years<1 ? "1개월 개근마다 1일" : (added? "기본 15일 + 가산 "+added+"일" : "기본 15일")},
      stats:[
        {k:"재직기간", v:years+"년 "+(months-years*12)+"개월", sub:F.num(days)+"일"},
        {k:"미사용 시 수당", v: v.rate ? F.won(pay) : "—", sub: v.rate ? total+"일 × "+F.num(v.hours,1)+"시간" : "통상시급 입력 시"},
        {k:"다음 갱신", v: years<1 ? "입사 1년 후" : (years+1)+"년차"}
      ],
      hint:F.num(days)+"일 근속",
      cols:["연차","발생 일수","비고"],
      rows:(function(){
        var r=[["1년 미만","최대 11일","1개월 개근마다 1일"]];
        for(var y=1;y<=10;y++){
          var ad = y>=3 ? Math.min(10,Math.floor((y-1)/2)) : 0;
          var d=Math.min(25,15+ad);
          r.push([y+"년차", d+"일", ad? "기본 15 + 가산 "+ad : "기본"]);
        }
        return r;
      })(),
      tableHint:"근속연수별 연차",
      extra:"<div class='note'>회계연도 기준으로 운영하는 회사는 입사일 기준과 결과가 다를 수 있습니다. "+
        "취업규칙과 근로계약서를 확인하세요. 주 15시간 미만 근로자는 연차휴가 대상이 아닙니다.</div>"
    };
  }
});""",
    guide=u"""
<h3>연차는 언제 몇 개 생기나</h3>
<p>근로기준법상 연차유급휴가는 근속기간에 따라 이렇게 발생합니다.</p>
<ul>
<li><strong>1년 미만</strong> — 1개월을 개근할 때마다 1일씩, 최대 11일</li>
<li><strong>1년 이상</strong> — 1년간 80% 이상 출근하면 15일</li>
<li><strong>3년 이상</strong> — 2년마다 1일씩 가산, <strong>최대 25일</strong>까지</li>
</ul>

<h3>가산 연차 계산</h3>
<p>3년차에 1일이 붙어 16일, 5년차에 17일, 7년차에 18일 식으로 2년마다 하루씩 늘어납니다.
21년차에 25일이 되면 그 뒤로는 더 늘지 않습니다.</p>
<div class="tablewrap"><table>
<thead><tr><th>근속</th><th>연차</th><th>근속</th><th>연차</th></tr></thead>
<tbody>
<tr><td>1~2년</td><td class="n">15일</td><td>11~12년</td><td class="n">20일</td></tr>
<tr><td>3~4년</td><td class="n">16일</td><td>13~14년</td><td class="n">21일</td></tr>
<tr><td>5~6년</td><td class="n">17일</td><td>15~16년</td><td class="n">22일</td></tr>
<tr><td>7~8년</td><td class="n">18일</td><td>17~18년</td><td class="n">23일</td></tr>
<tr><td>9~10년</td><td class="n">19일</td><td>21년~</td><td class="n">25일 (상한)</td></tr>
</tbody></table></div>

<h3>입사일 기준과 회계연도 기준</h3>
<p>법이 정한 원칙은 <strong>입사일 기준</strong>입니다. 다만 관리 편의를 위해
<strong>회계연도(보통 1월 1일)</strong>를 기준으로 일괄 부여하는 회사가 많습니다.
회계연도 기준으로 운영하더라도 퇴사 시점에는 입사일 기준으로 정산해
근로자에게 불리하지 않게 맞춰야 합니다.</p>
<p>이 계산기는 <strong>입사일 기준</strong>으로 계산합니다.
회사가 회계연도 기준이라면 실제 부여 일수가 다를 수 있으니 취업규칙을 확인하세요.</p>

<h3>연차수당</h3>
<p>쓰지 못한 연차는 수당으로 받습니다. <strong>연차수당 = 통상임금(시급) × 1일 근로시간 × 미사용 일수</strong>입니다.
8시간 근무에 통상시급 15,000원이고 5일이 남았다면 60만원입니다.
통상시급 칸에 값을 넣으면 계산해 드립니다.</p>

<h3>연차 사용 촉진</h3>
<p>회사가 법에 정한 절차대로 사용을 촉진했는데도 근로자가 쓰지 않으면
미사용 연차에 대한 수당 지급 의무가 없어질 수 있습니다.
촉진 절차에는 서면 통보 등 요건이 있으니, 분쟁이 있다면 고용노동부에 문의하세요.</p>

<h3>대상에서 빠지는 경우</h3>
<p>주 소정근로시간이 15시간 미만인 근로자는 연차휴가 대상이 아닙니다.
상시 근로자 5인 미만 사업장도 연차휴가 규정이 적용되지 않습니다.</p>
""",
    faq=[
        (u"입사 6개월인데 연차가 있나요?",
         u"1년 미만이면 1개월 개근마다 1일씩 발생합니다. 6개월이면 최대 6일입니다."),
        (u"회사가 회계연도 기준이라는데 다른가요?",
         u"부여 시점이 달라 중간에는 일수가 다를 수 있습니다. 다만 퇴사 시에는 입사일 기준으로 "
         u"정산해 근로자에게 불리하지 않아야 합니다."),
        (u"연차가 25일보다 많아질 수 있나요?",
         u"법정 한도는 25일입니다. 다만 회사가 취업규칙으로 더 줄 수는 있습니다."),
        (u"5인 미만 사업장도 연차가 있나요?",
         u"상시 근로자 5인 미만 사업장에는 연차휴가 규정이 적용되지 않습니다."),
    ],
)

# ───────────────────────── BMI · 칼로리 ─────────────────────────
add(
    slug="bmi", name=u"BMI·칼로리 계산기", group=u"부동산·생활",
    title=u"BMI 계산기 | 체질량지수와 하루 필요 칼로리",
    desc=u"키와 몸무게로 BMI를 계산하고, 기초대사량과 활동량을 반영한 하루 필요 칼로리를 알려줍니다.",
    kw=u"체질량지수, 기초대사량, 하루 필요 칼로리",
    spec=u"""
Calc.mount({
  id:"bmi",
  formTitle:"신체 정보",
  fields:[
    {k:"sex", label:"성별", type:"seg", options:[
      {value:"m", label:"남성"}, {value:"f", label:"여성"}]},
    {k:"height", label:"키", suffix:"cm", value:170, step:0.1, min:1},
    {k:"weight", label:"몸무게", suffix:"kg", value:70, step:0.1, min:1},
    {k:"age", label:"나이", suffix:"세", value:35, step:1, min:1},
    {k:"act", label:"활동량", type:"select", value:"1.375", options:[
      {value:"1.2", label:"거의 안 움직임 (사무직)"},
      {value:"1.375", label:"가벼운 활동 (주 1~3회 운동)"},
      {value:"1.55", label:"보통 (주 3~5회 운동)"},
      {value:"1.725", label:"많음 (주 6~7회 운동)"},
      {value:"1.9", label:"매우 많음 (육체노동·선수)"}]},
    {k:"goal", label:"목표", type:"seg", options:[
      {value:"keep", label:"유지"}, {value:"lose", label:"감량"}, {value:"gain", label:"증량"}]}
  ],
  compute:function(v,F){
    var h=(v.height||1)/100, w=v.weight||1, age=v.age||1;
    var bmi=w/(h*h);
    /* 대한비만학회 아시아·태평양 기준 */
    var label, cls;
    if(bmi<18.5){label="저체중";cls="down";}
    else if(bmi<23){label="정상";cls="up";}
    else if(bmi<25){label="과체중";cls="";}
    else if(bmi<30){label="비만 1단계";cls="down";}
    else if(bmi<35){label="비만 2단계";cls="down";}
    else {label="비만 3단계";cls="down";}

    /* Mifflin-St Jeor */
    var bmr = 10*w + 6.25*(v.height||1) - 5*age + (v.sex==="f" ? -161 : 5);
    var tdee = bmr*(+v.act||1.375);
    var target = v.goal==="lose" ? tdee-500 : v.goal==="gain" ? tdee+400 : tdee;

    /* 정상 체중 범위 (BMI 18.5~22.9) */
    var lo=18.5*h*h, hi=22.9*h*h;

    return {
      hero:{k:"체질량지수 (BMI)", v:F.num(bmi,1), cls:cls, sub:label},
      stats:[
        {k:"기초대사량", v:F.num(bmr)+" kcal", sub:"가만히 있어도 쓰는 열량"},
        {k:"하루 소모량", v:F.num(tdee)+" kcal", sub:"활동량 반영"},
        {k:"목표 섭취량", v:F.num(target)+" kcal",
         cls: v.goal==="lose"?"down":v.goal==="gain"?"up":"",
         sub: v.goal==="lose"?"하루 -500":v.goal==="gain"?"하루 +400":"현 체중 유지"}
      ],
      hint:label+" · "+(v.sex==="f"?"여성":"남성")+" "+age+"세",
      extra:"<div class='note'>키 "+F.num(v.height,1)+"cm 기준 정상 체중 범위는 "+
        "<b>"+F.num(lo,1)+"~"+F.num(hi,1)+"kg</b> 입니다 (BMI 18.5~22.9). "+
        (v.goal==="lose" ? "하루 500kcal 적자면 주당 약 0.5kg 감량 속도입니다. " : "")+
        "BMI 는 근육량을 구분하지 못해 운동선수처럼 근육이 많으면 실제보다 높게 나옵니다.</div>",
      cols:["구분","BMI","키 "+F.num(v.height,0)+"cm 기준 체중"],
      rows:[
        ["저체중","18.5 미만","~ "+F.num(18.5*h*h,1)+"kg"],
        ["정상","18.5 ~ 22.9",F.num(18.5*h*h,1)+" ~ "+F.num(22.9*h*h,1)+"kg"],
        ["과체중","23 ~ 24.9",F.num(23*h*h,1)+" ~ "+F.num(24.9*h*h,1)+"kg"],
        ["비만 1단계","25 ~ 29.9",F.num(25*h*h,1)+" ~ "+F.num(29.9*h*h,1)+"kg"],
        ["비만 2단계","30 ~ 34.9",F.num(30*h*h,1)+" ~ "+F.num(34.9*h*h,1)+"kg"],
        ["비만 3단계","35 이상",F.num(35*h*h,1)+"kg ~"]
      ],
      tableHint:"대한비만학회 기준"
    };
  }
});""",
    guide=u"""
<h3>한국 기준은 세계보건기구 기준과 다릅니다</h3>
<p>BMI = 체중(kg) ÷ 키(m)²입니다. 그런데 <strong>비만 판정 기준선이 다릅니다.</strong></p>
<p>WHO 국제 기준은 BMI 25 이상을 과체중, 30 이상을 비만으로 봅니다.
반면 대한비만학회의 아시아·태평양 기준은 <strong>23 이상 과체중, 25 이상 비만</strong>입니다.
같은 체중이라도 아시아인이 더 낮은 BMI에서 대사질환 위험이 올라가기 때문입니다.
이 계산기는 한국 기준을 씁니다.</p>

<h3>기초대사량과 하루 소모량</h3>
<p><strong>기초대사량(BMR)</strong>은 아무것도 안 하고 누워만 있어도 소모되는 열량입니다.
호흡, 체온 유지, 장기 활동에 쓰입니다.</p>
<p><strong>하루 소모량(TDEE)</strong>은 여기에 활동량을 곱한 값입니다.
사무직이면 BMR × 1.2, 주 3~5회 운동하면 × 1.55 정도입니다.
살을 빼려면 이 숫자보다 적게 먹어야 합니다.</p>
<p>계산에는 미플린-세인트 지어(Mifflin-St Jeor) 공식을 씁니다.
현재 가장 널리 쓰이는 추정식이지만 개인차가 있어 ±10% 정도 오차는 정상입니다.</p>

<h3>감량 속도는 하루 500kcal이 기준</h3>
<p>지방 1kg을 빼려면 약 7,700kcal의 적자가 필요합니다.
하루 500kcal씩 덜 먹으면 일주일에 3,500kcal, 약 0.45kg이 빠집니다.
<strong>한 달에 2kg 정도가 무리 없는 속도</strong>입니다.</p>
<p>하루 소모량보다 극단적으로 적게 먹으면 근육이 함께 빠지고 기초대사량이 떨어져
오히려 되돌리기 어려워집니다. 기초대사량 아래로는 내려가지 않는 편이 좋습니다.</p>

<h3>BMI의 한계</h3>
<p>BMI는 체중과 키만 봅니다. <strong>근육과 지방을 구분하지 못합니다.</strong>
근육량이 많은 사람은 BMI가 높게 나오지만 비만이 아닙니다.
반대로 체중은 정상인데 체지방률이 높은 경우도 잡아내지 못합니다.</p>
<p>허리둘레를 함께 보면 도움이 됩니다. 남성 90cm, 여성 85cm 이상이면
복부비만으로 보고 대사질환 위험이 올라갑니다.</p>

<h3>참고 사항</h3>
<p>이 계산기는 일반적인 추정식에 따른 참고 수치이며 의학적 진단이 아닙니다.
체중 변화가 급격하거나 건강 문제가 있다면 의료진과 상담하세요.</p>
""",
    faq=[
        (u"BMI 24인데 비만인가요?",
         u"한국 기준으로는 과체중(23~24.9) 구간입니다. WHO 국제 기준으로는 정상 범위입니다. "
         u"기준선이 달라 생기는 차이입니다."),
        (u"기초대사량보다 적게 먹어도 되나요?",
         u"권장하지 않습니다. 근육이 함께 빠지고 기초대사량이 떨어져 장기적으로 불리합니다."),
        (u"운동을 많이 하는데 BMI가 높게 나옵니다.",
         u"BMI는 근육과 지방을 구분하지 못합니다. 근육량이 많으면 실제보다 높게 나오므로 "
         u"체지방률이나 허리둘레를 함께 보시는 편이 정확합니다."),
        (u"하루 500kcal 줄이면 얼마나 빠지나요?",
         u"지방 1kg은 약 7,700kcal에 해당합니다. 하루 500kcal 적자면 주당 약 0.45kg 속도입니다."),
    ],
)

# ───────────────────────── 취득세 ─────────────────────────
add(
    slug="chwideukse", name=u"취득세 계산기", group=u"부동산·생활",
    title=u"취득세 계산기 | 주택 취득세·지방교육세·농특세 계산",
    desc=u"주택 취득가액으로 취득세와 지방교육세, 농어촌특별세를 계산합니다. 주택 수와 전용면적에 따른 차이를 반영합니다.",
    kw=u"주택 취득세·지방교육세·농특세 합계",
    spec=u"""
Calc.mount({
  id:"chwideukse",
  formTitle:"취득 정보",
  sideNote:"세율은 개정될 수 있습니다. 실제 신고 전 위택스나 관할 지자체에서 확인하세요.",
  fields:[
    {k:"price", label:"취득가액", suffix:"원", value:600000000, step:10000000, min:0},
    {k:"area", label:"전용면적", sub:"85㎡ 초과 시 농특세", suffix:"㎡", value:84.9, step:0.01, min:0},
    /* 값에 숫자만 쓰면 엔진이 숫자로 변환해 문자열 비교가 어긋난다. 접두사를 붙인다. */
    {k:"houses", label:"취득 후 주택 수", type:"select", value:"h1", options:[
      {value:"h1", label:"1주택"},
      {value:"h2c", label:"2주택 (조정대상지역)"},
      {value:"h2n", label:"2주택 (비조정)"},
      {value:"h3c", label:"3주택 (조정) 또는 4주택 이상"},
      {value:"h3n", label:"3주택 (비조정)"}]}
  ],
  compute:function(v,F){
    var p=v.price||0, area=v.area||0, h=v.houses;
    var rate, note="";

    if(h==="h1" || h==="h2n"){
      /* 표준세율: 6억 이하 1%, 6~9억 비례, 9억 초과 3% */
      if(p<=600000000) rate=1;
      else if(p<=900000000){
        rate = (p*2/300000000 - 3);
        rate = Math.round(rate*100)/100;
      } else rate=3;
      note = h==="h2n" ? "비조정지역 2주택은 표준세율" : "1주택 표준세율";
    } else if(h==="h2c" || h==="h3n"){
      rate=8; note="중과세율 8%";
    } else {
      rate=12; note="중과세율 12%";
    }

    var acq=p*rate/100;
    /* 지방교육세: 표준세율 구간은 취득세율의 1/10, 중과 구간은 0.4% */
    var eduRate = rate<=3 ? rate/10 : 0.4;
    var edu=p*eduRate/100;
    /* 농어촌특별세: 전용 85㎡ 초과분만. 표준 0.2%, 중과 구간 가산 */
    var farmRate = area>85 ? (rate<=3 ? 0.2 : (rate===8 ? 0.6 : 1.0)) : 0;
    var farm=p*farmRate/100;
    var total=acq+edu+farm;

    return {
      hero:{k:"취득세 등 합계", v:F.kor(total), sub:F.won(total), cls:"down"},
      stats:[
        {k:"취득세", v:F.won(acq), sub:F.pct(rate,2)},
        {k:"지방교육세", v:F.won(edu), sub:F.pct(eduRate,2)},
        {k:"농어촌특별세", v: farmRate? F.won(farm):"—", sub: area>85 ? F.pct(farmRate,2) : "85㎡ 이하 비과세"}
      ],
      hint:note+" · "+F.kor(p),
      extra:"<div class='note'>"+
        (p>600000000 && p<=900000000 && rate<=3
          ? "6억 초과 9억 이하 구간은 세율이 <b>비례해서 올라갑니다.</b> "+
            "세율(%) = 취득가액 × 2 ÷ 3억 − 3 이며, 이 금액에서는 <b>"+F.pct(rate,2)+"</b> 입니다.<br><br>"
          : "")+
        "표시된 금액에 <b>인지세·법무사 보수·중개보수</b>는 포함되지 않았습니다. "+
        "생애최초 구입, 신혼부부, 일시적 2주택 등 감면 요건에 해당하면 실제 부담이 줄어듭니다. "+
        "감면은 요건이 까다로우니 위택스나 관할 지자체에서 확인하세요.</div>"
    };
  }
});""",
    guide=u"""
<h3>취득세는 세 가지를 함께 냅니다</h3>
<ul>
<li><strong>취득세</strong> — 본세</li>
<li><strong>지방교육세</strong> — 취득세에 부가</li>
<li><strong>농어촌특별세</strong> — 전용면적 85㎡를 넘을 때만</li>
</ul>
<p>흔히 "취득세 1%"라고 하지만 지방교육세 0.1%가 더 붙어 실제로는 1.1%입니다.
85㎡를 넘으면 농특세 0.2%가 더해져 1.3%가 됩니다.</p>

<h3>6억 초과 9억 이하는 세율이 비례해서 올라갑니다</h3>
<p>여기서 계산을 많이 틀립니다. 6억까지는 1%, 9억부터는 3%인데,
그 사이는 <strong>계단이 아니라 직선</strong>으로 올라갑니다.</p>
<p><strong>세율(%) = 취득가액 × 2 ÷ 3억 − 3</strong></p>
<div class="tablewrap"><table>
<thead><tr><th>취득가액</th><th>취득세율</th><th>지방교육세</th><th>합계(85㎡ 이하)</th></tr></thead>
<tbody>
<tr><td>6억</td><td class="n">1.00%</td><td class="n">0.10%</td><td class="n">1.10%</td></tr>
<tr><td>7억</td><td class="n">1.67%</td><td class="n">0.17%</td><td class="n">1.84%</td></tr>
<tr><td>8억</td><td class="n">2.33%</td><td class="n">0.23%</td><td class="n">2.56%</td></tr>
<tr><td>9억</td><td class="n">3.00%</td><td class="n">0.30%</td><td class="n">3.30%</td></tr>
</tbody></table></div>
<p>6억에서 1원만 넘어도 세율이 껑충 뛰는 구조가 아니라는 점이 중요합니다.</p>

<h3>85㎡ 기준선</h3>
<p>전용면적 85㎡ 이하는 농어촌특별세가 <strong>비과세</strong>입니다.
84.9㎡와 85.1㎡의 세금이 달라지는 이유입니다.
아파트 분양 면적이 84㎡에 몰려 있는 데는 이런 배경도 있습니다.</p>

<h3>다주택 중과</h3>
<p>주택 수와 조정대상지역 여부에 따라 8% 또는 12%가 적용됩니다.
중과 구간에서는 지방교육세와 농특세도 함께 올라가 부담이 크게 늘어납니다.
조정대상지역 지정은 수시로 바뀌므로 취득 시점의 지정 여부를 확인해야 합니다.</p>

<h3>감면 제도</h3>
<p>생애최초 주택 구입, 신혼부부, 일시적 2주택 등 요건에 해당하면 감면받을 수 있습니다.
요건이 까다롭고 사후 관리 조건도 있어, 해당한다고 생각되면 반드시
위택스나 관할 시·군·구청에 확인하세요.</p>

<h3>이 계산에 없는 비용</h3>
<p>취득세 외에 <strong>인지세, 법무사 보수, 중개보수, 국민주택채권 매입</strong> 비용이 별도로 듭니다.
중개보수는 <a href="../brokerage/">중개보수 계산기</a>에서 확인하실 수 있습니다.</p>
""",
    faq=[
        (u"6억 1천만원이면 세율이 얼마인가요?",
         u"6억 초과 구간은 비례 계산합니다. 6억 1천만원이면 약 1.07%입니다. "
         u"6억을 넘는 순간 3%가 되는 것이 아닙니다."),
        (u"85㎡ 기준은 공급면적인가요 전용면적인가요?",
         u"전용면적 기준입니다. 84㎡ 아파트는 대부분 농특세가 비과세됩니다."),
        (u"생애최초인데 감면받을 수 있나요?",
         u"요건에 해당하면 감면이 가능합니다. 다만 소득·주택가격·사후 거주 요건 등이 있어 "
         u"위택스나 관할 지자체 확인이 필요합니다. 이 계산기는 감면 전 금액입니다."),
        (u"조정대상지역인지 어떻게 아나요?",
         u"국토교통부 고시로 지정되며 수시로 바뀝니다. 취득 시점 기준으로 확인하셔야 합니다."),
    ],
)

# ───────────────────────── 자동차 할부 ─────────────────────────
add(
    slug="carloan", name=u"자동차 할부 계산기", group=u"대출·예금",
    title=u"자동차 할부 계산기 | 월 납입금과 총 이자 계산",
    desc=u"차량가격, 선수금, 유예금(잔가)으로 자동차 할부의 월 납입금과 총 이자를 계산합니다.",
    kw=u"선수금·유예금 반영한 월 납입금과 총이자",
    spec=u"""
Calc.mount({
  id:"carloan",
  formTitle:"할부 조건",
  fields:[
    {k:"price", label:"차량가격", suffix:"원", value:40000000, step:1000000, min:0},
    {k:"down", label:"선수금", sub:"계약 시 내는 돈", suffix:"원", value:8000000, step:1000000, min:0},
    {k:"balloon", label:"유예금 (잔가)", sub:"만기에 한 번에 갚는 금액", suffix:"원", value:0, step:1000000, min:0},
    {k:"rate", label:"연이자율", suffix:"%", value:6.9, step:0.1, min:0},
    {k:"months", label:"할부기간", suffix:"개월", value:60, step:1, min:1}
  ],
  compute:function(v,F){
    var P=v.price||0, dn=Math.min(v.down||0,P), B=Math.min(v.balloon||0, P-dn);
    var fin=P-dn, i=(v.rate||0)/100/12, n=Math.max(1,Math.round(v.months||1));

    var m;
    if(i>0){
      var disc=Math.pow(1+i,-n);
      m = (fin - B*disc) * i / (1-disc);
    } else {
      m = (fin-B)/n;
    }
    var totalPaid = m*n + B + dn;
    var interest = totalPaid - P;

    var rows=[], bal=fin;
    for(var k=1;k<=n && rows.length<600;k++){
      var it=bal*i, pr=m-it;
      if(k===n){ pr=bal-B; }
      bal-=pr;
      rows.push([k+"회", F.won(pr), F.won(it), F.won(k===n? m+B : m), F.won(Math.max(bal,0))]);
    }

    return {
      hero:{k:"월 납입금", v:F.kor(m), sub:F.won(m)},
      stats:[
        {k:"할부 원금", v:F.won(fin), sub:"차량가 − 선수금"},
        {k:"총 이자", v:F.won(interest), cls:"down"},
        {k:"총 지출", v:F.won(totalPaid), sub:"선수금 포함"}
      ],
      hint:F.num(n)+"개월 · 연 "+F.num(v.rate,1)+"%"+(B?" · 유예 "+F.kor(B):""),
      extra:"<div class='note'>"+
        (B? "만기에 유예금 <b>"+F.won(B)+"</b> 을 한 번에 갚아야 합니다. "+
            "월 납입금은 줄지만 이자를 더 내며, 만기에 목돈이 필요합니다. "
          : "")+
        "취득세·등록세·보험료·탁송료는 포함되지 않았습니다. "+
        "실제 계약에는 중도상환수수료나 저당설정비가 붙을 수 있습니다.</div>",
      cols:["회차","원금","이자","납입액","잔액"],
      rows:rows,
      tableHint: n>600 ? "앞 600회차만" : F.num(n)+"회차"
    };
  }
});""",
    guide=u"""
<h3>할부는 세 덩어리로 나뉩니다</h3>
<ul>
<li><strong>선수금</strong> — 계약할 때 미리 내는 돈. 많이 낼수록 할부 원금이 줄어 이자가 적습니다.</li>
<li><strong>할부 원금</strong> — 매달 나눠 갚는 부분</li>
<li><strong>유예금(잔가)</strong> — 만기에 한 번에 갚는 부분. 월 납입금을 낮추는 대신 목돈이 필요합니다.</li>
</ul>

<h3>유예할부의 함정</h3>
<p>유예금을 크게 잡으면 월 납입금이 눈에 띄게 줄어듭니다.
4,000만원 차를 선수금 800만원에 60개월 할부하면 월 63만원 정도인데,
유예금 1,000만원을 잡으면 월 49만원으로 내려갑니다.</p>
<p>다만 <strong>만기에 1,000만원을 한 번에 마련해야 합니다.</strong>
그때 목돈이 없으면 다시 대출을 받거나 차를 넘기게 되고,
그 과정에서 이자를 또 부담하게 됩니다. 유예금은 미룬 것이지 없어진 것이 아닙니다.</p>
<p>게다가 유예금에도 할부 기간 내내 이자가 붙습니다. 위 조건에서 총 이자는 593만원에서 <strong>753만원</strong>으로 160만원 늘어납니다.
계산기에서 유예금을 0으로 놓고 비교해 보세요.</p>

<h3>차량가격 외에 드는 돈</h3>
<p>계약서에 적힌 차량가격만 준비하면 안 됩니다.</p>
<ul>
<li><strong>취득세</strong> — 승용차 7% (경차·전기차 등 감면 있음)</li>
<li><strong>공채 매입</strong> — 지역과 배기량에 따라 다름</li>
<li><strong>등록비·탁송료</strong></li>
<li><strong>자동차보험</strong> — 첫해 부담이 큽니다</li>
</ul>
<p>이 계산기는 순수 할부금만 다룹니다. 위 비용을 따로 잡아두셔야 합니다.</p>

<h3>이자율을 낮추는 것이 가장 확실합니다</h3>
<p>4,000만원 60개월 기준으로 금리가 1%p 낮아지면 총 이자가 100만원 가까이 줄어듭니다.
제조사 할부, 카드사 할부, 은행 오토론의 금리와 조건을 비교해 보시고,
현금 구매 시 할인(현금가 할인)과도 비교해 보세요.</p>

<h3>중도상환</h3>
<p>일찍 갚으면 남은 이자를 아낄 수 있지만 중도상환수수료가 붙는 경우가 많습니다.
약정서에서 수수료율과 면제 조건을 확인하세요. 이 계산기는 반영하지 않습니다.</p>
""",
    faq=[
        (u"유예금을 크게 잡으면 유리한가요?",
         u"월 납입금은 줄지만 총 이자는 늘고, 만기에 목돈이 필요합니다. "
         u"유예금을 0으로 두고 비교해 보시면 차이가 보입니다."),
        (u"취득세도 계산되나요?",
         u"포함되지 않습니다. 승용차 취득세는 7% 수준이며 차종에 따라 감면이 있습니다. "
         u"차량가격 외에 별도로 준비하셔야 합니다."),
        (u"선수금을 얼마나 넣는 게 좋나요?",
         u"많이 넣을수록 이자가 줄지만 현금 흐름이 빡빡해집니다. "
         u"선수금을 바꿔가며 월 납입금과 총 이자를 비교해 보세요."),
        (u"저금리 할부가 정말 유리한가요?",
         u"저금리 대신 차량 할인이 줄어드는 경우가 많습니다. "
         u"현금가 할인을 받고 별도 대출을 쓰는 쪽과 총 지출을 비교해 보세요."),
    ],
)

# ───────────────────────── 양도소득세 ─────────────────────────
add(
    slug="yangdo", name=u"양도소득세 계산기", group=u"부동산·생활",
    title=u"양도소득세 계산기 | 주택 양도세와 장기보유특별공제",
    desc=u"양도가액과 취득가액으로 양도소득세를 계산합니다. 장기보유특별공제, 1세대1주택 비과세, 단기보유 중과세율을 반영합니다.",
    kw=u"양도차익·장특공제 반영한 양도세와 지방소득세",
    spec=u"""
Calc.mount({
  id:"yangdo",
  formTitle:"양도 정보",
  sideNote:"주택 1건 양도를 전제로 한 개략 계산입니다. 다주택 중과, 조정대상지역, 감면 특례는 반영하지 않습니다.",
  fields:[
    {k:"sale", label:"양도가액", sub:"판 금액", suffix:"원", value:900000000, step:10000000, min:0},
    {k:"buy", label:"취득가액", sub:"산 금액", suffix:"원", value:500000000, step:10000000, min:0},
    {k:"cost", label:"필요경비", sub:"취득세·중개보수·수선비 등", suffix:"원", value:20000000, step:1000000, min:0},
    {k:"hold", label:"보유기간", suffix:"년", value:10, step:0.5, min:0},
    {k:"live", label:"거주기간", sub:"1세대1주택 공제용", suffix:"년", value:10, step:0.5, min:0},
    {k:"one", label:"1세대 1주택", type:"seg", options:[
      {value:"1", label:"해당"}, {value:"0", label:"해당 없음"}]}
  ],
  compute:function(v,F){
    var sale=v.sale||0, buy=v.buy||0, cost=v.cost||0;
    var hold=v.hold||0, live=v.live||0, isOne=v.one==1;
    var gain=sale-buy-cost;

    if(gain<=0){
      return {hero:{k:"양도차익", v:"손실", cls:"down", sub:F.won(gain)},
              extra:"<div class='note'>양도차익이 없으면 양도소득세도 없습니다. "+
                "다만 같은 해 다른 양도소득과 통산할 수 있으니 신고는 확인해 보세요.</div>"};
    }

    /* 1세대1주택: 12억 초과분만 과세 */
    var HIGH=1200000000;
    var taxableGain=gain, exemptNote="";
    if(isOne){
      if(sale<=HIGH){
        return {hero:{k:"양도소득세", v:"비과세", cls:"up", sub:"1세대 1주택 12억 이하"},
                stats:[{k:"양도차익", v:F.won(gain)},{k:"양도가액", v:F.won(sale)},
                       {k:"보유기간", v:F.num(hold,1)+"년"}],
                extra:"<div class='note'>1세대 1주택이고 양도가액이 <b>12억원 이하</b>라 비과세입니다. "+
                  "다만 <b>2년 이상 보유</b>(취득 당시 조정대상지역이면 2년 이상 거주) 요건을 "+
                  "충족해야 합니다. 요건을 못 채우면 과세됩니다.</div>"};
      }
      taxableGain = gain*(sale-HIGH)/sale;
      exemptNote = "12억 초과분만 과세";
    }

    /* 장기보유특별공제 */
    var ltRate=0, ltNote="";
    if(isOne && live>=2 && hold>=3){
      var h=Math.min(Math.floor(hold),10)*4, l=Math.min(Math.floor(live),10)*4;
      ltRate=Math.min(80, h+l);
      ltNote="보유 "+h+"% + 거주 "+l+"%";
    } else if(hold>=3){
      ltRate=Math.min(30, Math.floor(hold)*2);
      ltNote="보유 "+Math.floor(hold)+"년 × 2%";
    } else {
      ltNote="3년 미만은 공제 없음";
    }
    var ltDeduct=taxableGain*ltRate/100;
    var income=taxableGain-ltDeduct;

    var BASIC=2500000;
    var base=Math.max(0, income-BASIC);

    /* 세율: 단기보유 중과 */
    var tax, rateNote;
    if(hold<1){ tax=base*0.70; rateNote="1년 미만 70%"; }
    else if(hold<2){ tax=base*0.60; rateNote="1~2년 60%"; }
    else {
      var t=[[14000000,.06,0],[50000000,.15,1260000],[88000000,.24,5760000],
             [150000000,.35,15440000],[300000000,.38,19940000],[500000000,.40,25940000],
             [1000000000,.42,35940000],[Infinity,.45,65940000]];
      tax=0;
      for(var i=0;i<t.length;i++) if(base<=t[i][0]){ tax=base*t[i][1]-t[i][2]; rateNote="누진세율 "+(t[i][1]*100)+"%"; break; }
    }
    tax=Math.max(0,tax);
    var local=tax*0.1, total=tax+local;

    return {
      hero:{k:"양도소득세 합계", v:F.kor(total), sub:F.won(total), cls:"down"},
      stats:[
        {k:"양도차익", v:F.won(gain), cls:"up", sub:exemptNote||"양도−취득−경비"},
        {k:"장기보유공제", v:F.won(ltDeduct), sub:F.pct(ltRate,0)+" · "+ltNote},
        {k:"실수령 (세후)", v:F.won(gain-total), cls:"up"}
      ],
      hint:rateNote+" · 보유 "+F.num(hold,1)+"년",
      cols:["단계","금액"],
      rows:[
        ["양도가액", F.won(sale)],
        ["취득가액", "− "+F.won(buy)],
        ["필요경비", "− "+F.won(cost)],
        ["양도차익", F.won(gain)],
        [isOne?"과세대상 차익 (12억 초과분)":"과세대상 차익", F.won(taxableGain)],
        ["장기보유특별공제 "+F.pct(ltRate,0), "− "+F.won(ltDeduct)],
        ["양도소득금액", F.won(income)],
        ["기본공제", "− "+F.won(BASIC)],
        ["과세표준", F.won(base)],
        ["양도소득세", F.won(tax)],
        ["지방소득세 10%", F.won(local)],
        ["합계", F.won(total)]
      ],
      extra:"<div class='note'>주택 <b>1건</b> 양도를 전제로 한 개략 계산입니다. "+
        "다주택 중과세율, 조정대상지역 여부, 일시적 2주택, 상속·증여 취득, "+
        "감면 특례는 반영하지 않았습니다. 실제 신고는 홈택스나 세무 전문가를 통해 확인하세요.</div>"
    };
  }
});""",
    guide=u"""
<h3>계산 순서</h3>
<p>양도소득세는 단계를 밟아 내려갑니다.</p>
<ol>
<li><strong>양도차익</strong> = 양도가액 − 취득가액 − 필요경비</li>
<li><strong>장기보유특별공제</strong>를 뺍니다</li>
<li><strong>기본공제 250만원</strong>을 뺍니다 (연 1회)</li>
<li>남은 <strong>과세표준</strong>에 세율을 곱합니다</li>
<li><strong>지방소득세</strong>를 양도세의 10%만큼 더합니다</li>
</ol>

<h3>필요경비에 넣을 수 있는 것</h3>
<p>취득할 때 낸 <strong>취득세·등록세</strong>, <strong>중개보수</strong>, <strong>법무사 비용</strong>,
자본적 지출에 해당하는 <strong>수선비</strong>(발코니 확장, 새시 교체, 난방 교체 등)를 넣습니다.
도배·장판 같은 원상복구성 지출은 인정되지 않습니다.
증빙이 없으면 인정받기 어려우니 계약서와 영수증을 보관하셔야 합니다.</p>

<h3>1세대 1주택 비과세는 12억까지</h3>
<p>1세대가 1주택을 <strong>2년 이상 보유</strong>(취득 당시 조정대상지역이었다면 2년 이상 거주)하고
양도가액이 <strong>12억원 이하</strong>면 비과세입니다.</p>
<p>12억을 넘으면 <strong>초과분에 해당하는 차익만</strong> 과세합니다.
15억에 팔아 차익이 5억이라면, 5억 × (15억−12억) ÷ 15억 = 1억에 대해서만 세금을 냅니다.
전액이 과세되는 것이 아닙니다.</p>

<h3>장기보유특별공제 — 1주택이면 최대 80%</h3>
<p>오래 보유할수록 공제가 커집니다. 두 갈래로 나뉩니다.</p>
<div class="tablewrap"><table>
<thead><tr><th>구분</th><th>공제율</th><th>상한</th></tr></thead>
<tbody>
<tr><td>일반 (3년 이상)</td><td class="n">보유 연 2%</td><td class="n">30% (15년)</td></tr>
<tr><td>1세대1주택 (2년 이상 거주)</td><td class="n">보유 연 4% + 거주 연 4%</td><td class="n">80% (각 10년)</td></tr>
</tbody></table></div>
<p>1주택자가 10년 보유하고 10년 거주하면 40% + 40% = <strong>80% 공제</strong>입니다.
차익의 80%가 빠지므로 세금이 크게 줄어듭니다. 거주 요건이 붙는 이유입니다.</p>
<p><strong>3년 미만은 공제가 아예 없습니다.</strong></p>

<h3>단기 보유는 세율이 크게 올라갑니다</h3>
<div class="tablewrap"><table>
<thead><tr><th>보유기간</th><th>세율</th></tr></thead>
<tbody>
<tr><td>1년 미만</td><td class="n">70%</td></tr>
<tr><td>1년 이상 2년 미만</td><td class="n">60%</td></tr>
<tr><td>2년 이상</td><td class="n">6~45% 누진</td></tr>
</tbody></table></div>
<p>여기에 지방소득세 10%가 더 붙습니다. 1년 미만이면 실질 77%입니다.
단기 매매 차익은 대부분 세금으로 나갑니다.</p>

<h3>신고 기한</h3>
<p>양도일이 속한 달의 말일부터 <strong>2개월 이내</strong>에 예정신고·납부해야 합니다.
같은 해에 두 건 이상 양도했다면 다음 해 5월에 확정신고로 합산합니다.
기한을 넘기면 가산세가 붙습니다.</p>

<h3>이 계산기가 다루지 않는 것</h3>
<p>다주택 중과세율, 조정대상지역 지정, 일시적 2주택 특례, 상속·증여로 취득한 경우,
분양권·입주권, 재개발·재건축, 각종 감면 특례는 반영하지 않았습니다.
양도세는 사안마다 결론이 크게 달라지므로 <strong>실제 신고 전 홈택스나 세무 전문가 확인이 필요합니다.</strong></p>
""",
    faq=[
        (u"1세대 1주택인데 15억에 팔면 세금이 얼마인가요?",
         u"12억 초과분에 해당하는 차익만 과세합니다. 전액이 과세되는 것이 아니라 "
         u"차익 × (양도가액−12억) ÷ 양도가액 만큼만 대상이 됩니다."),
        (u"장기보유특별공제 80%는 누가 받나요?",
         u"1세대 1주택으로 2년 이상 거주한 경우, 보유 연 4%와 거주 연 4%를 합해 최대 80%입니다. "
         u"10년 보유 + 10년 거주가 상한입니다."),
        (u"필요경비에 인테리어 비용을 넣을 수 있나요?",
         u"발코니 확장, 새시 교체처럼 자산 가치를 높이는 자본적 지출은 인정됩니다. "
         u"도배·장판 같은 원상복구성 지출은 인정되지 않습니다. 증빙이 필요합니다."),
        (u"다주택자인데 이 계산이 맞나요?",
         u"이 계산기는 주택 1건 양도를 전제로 합니다. 다주택 중과세율은 반영하지 않았으므로 "
         u"실제 세액은 더 클 수 있습니다. 세무 전문가 상담을 권합니다."),
        (u"언제까지 신고해야 하나요?",
         u"양도일이 속한 달의 말일부터 2개월 이내에 예정신고·납부합니다."),
    ],
)

# ───────────────────────── 실업급여 ─────────────────────────
add(
    slug="silup", name=u"실업급여 계산기", group=u"급여·노무",
    title=u"실업급여 계산기 | 구직급여 일액과 총 수령액",
    desc=u"퇴직 전 평균임금과 고용보험 가입기간으로 구직급여 일액과 소정급여일수, 총 수령액을 계산합니다.",
    kw=u"구직급여 일액·소정급여일수·총 수령액",
    spec=u"""
Calc.mount({
  id:"silup",
  formTitle:"이직 정보",
  sideNote:"상한액과 최저임금은 해마다 바뀝니다. 고용보험 홈페이지에서 당해 연도 기준을 확인해 값을 고쳐 쓰세요.",
  fields:[
    {k:"pay3", label:"퇴직 전 3개월 임금", sub:"세전 총액", suffix:"원", value:9000000, step:100000, min:0},
    {k:"days", label:"3개월 총일수", sub:"달력상 일수", suffix:"일", value:91, step:1, min:1},
    {k:"insured", label:"고용보험 가입기간", type:"select", value:"3", options:[
      {value:"0", label:"1년 미만"},
      {value:"1", label:"1년 이상 3년 미만"},
      {value:"3", label:"3년 이상 5년 미만"},
      {value:"5", label:"5년 이상 10년 미만"},
      {value:"10", label:"10년 이상"}]},
    {k:"age", label:"이직 당시 연령", type:"seg", options:[
      {value:"u50", label:"50세 미만"}, {value:"o50", label:"50세 이상·장애인"}]},
    {k:"cap", label:"1일 상한액", suffix:"원", value:66000, step:1000, min:0},
    {k:"minwage", label:"최저임금 시급", suffix:"원", value:10320, step:10, min:0}
  ],
  compute:function(v,F){
    var avg=(v.pay3||0)/Math.max(1,v.days||1);
    var raw=avg*0.6;
    var cap=v.cap||66000;
    var floor=(v.minwage||0)*0.8*8;          /* 하한 = 최저임금 80% × 8시간 */
    /* 하한이 상한을 넘는 해가 있다(최저임금이 오르는데 상한이 묶여 있을 때).
       그때는 하한이 우선한다. min 을 먼저 걸면 하한 보장이 무너진다. */
    var daily=Math.max(floor, Math.min(cap, raw));
    var capped = floor>cap ? "하한이 상한 초과 — 하한 적용"
               : raw>cap ? "상한 적용"
               : raw<floor ? "하한 적용" : "평균임금 60%";

    var tbl={
      u50:{"0":120,"1":150,"3":180,"5":210,"10":240},
      o50:{"0":120,"1":180,"3":210,"5":240,"10":270}
    };
    var n=tbl[v.age][String(v.insured)] || 120;
    var total=daily*n;

    return {
      hero:{k:"예상 총 수령액", v:F.kor(total), sub:F.won(total), cls:"up"},
      stats:[
        {k:"1일 구직급여", v:F.won(daily), sub:capped},
        {k:"소정급여일수", v:F.num(n)+"일", sub:"약 "+F.num(n/30,1)+"개월"},
        {k:"1일 평균임금", v:F.won(avg)}
      ],
      hint:(v.age==="o50"?"50세 이상":"50세 미만")+" · 가입 "+
           ({"0":"1년 미만","1":"1~3년","3":"3~5년","5":"5~10년","10":"10년 이상"}[String(v.insured)]),
      cols:["가입기간","50세 미만","50세 이상·장애인"],
      rows:[
        ["1년 미만","120일","120일"],
        ["1~3년","150일","180일"],
        ["3~5년","180일","210일"],
        ["5~10년","210일","240일"],
        ["10년 이상","240일","270일"]
      ],
      tableHint:"소정급여일수",
      extra:"<div class='note'>구직급여는 <b>퇴직하면 자동으로 나오는 돈이 아닙니다.</b> "+
        "비자발적 이직(권고사직·계약만료·경영상 해고 등)이고, 이직 전 18개월간 피보험 단위기간이 "+
        "<b>180일 이상</b>이어야 하며, 적극적으로 재취업 활동을 해야 계속 지급됩니다. "+
        "자발적 퇴사는 원칙적으로 대상이 아니지만 임금체불 등 정당한 사유가 인정되면 예외가 있습니다. "+
        "1일 상한액은 <b>"+F.won(cap)+"</b>, 하한액은 최저임금 80%×8시간으로 <b>"+F.won(floor)+"</b> 입니다."+
        (floor>cap ? "<br><br><b>지금 넣으신 값에서는 하한액이 상한액보다 큽니다.</b> "+
          "최저임금은 올랐는데 상한액이 그대로일 때 생기는 상황으로, 이 경우 하한액이 적용됩니다. "+
          "두 값 모두 고용보험 홈페이지에서 당해 연도 기준을 확인해 넣으세요." : "")+"</div>"
    };
  }
});""",
    guide=u"""
<h3>얼마를 받나</h3>
<p><strong>1일 구직급여 = 퇴직 전 3개월 평균임금 × 60%</strong>입니다.
다만 상한과 하한이 있습니다.</p>
<ul>
<li><strong>상한액</strong> — 아무리 임금이 높아도 이 금액을 넘지 않습니다.</li>
<li><strong>하한액</strong> — 최저임금의 80% × 8시간. 임금이 낮아도 이 아래로는 내려가지 않습니다.</li>
</ul>
<p>두 값 모두 해마다 바뀌므로 계산기의 입력 항목으로 열어두었습니다.
고용보험 홈페이지에서 당해 연도 기준을 확인해 넣으세요.</p>

<h3>며칠 받나 — 소정급여일수</h3>
<p>고용보험 가입기간과 이직 당시 연령으로 정해집니다.
가입기간이 길수록, 50세 이상이면 더 오래 받습니다.
최소 120일에서 최대 270일입니다.</p>

<h3>받으려면 갖춰야 할 조건</h3>
<p>퇴직했다고 자동으로 나오지 않습니다. 세 가지를 모두 충족해야 합니다.</p>
<ol>
<li>이직 전 18개월간 <strong>피보험 단위기간 180일 이상</strong></li>
<li><strong>비자발적 이직</strong> — 권고사직, 계약만료, 경영상 해고 등</li>
<li><strong>재취업 노력</strong> — 구직활동을 증명해야 계속 지급됩니다</li>
</ol>

<h3>자발적 퇴사는 원칙적으로 안 됩니다</h3>
<p>본인이 사표를 낸 경우는 대상이 아닙니다. 다만 정당한 사유가 인정되면 예외가 있습니다.</p>
<ul>
<li>임금체불이 있었던 경우</li>
<li>최저임금에 미달한 경우</li>
<li>사업장 이전 등으로 통근이 왕복 3시간 이상 걸리게 된 경우</li>
<li>질병으로 업무 수행이 어렵고 회사가 배치전환을 해주지 못한 경우</li>
<li>직장 내 괴롭힘·성희롱 등</li>
</ul>
<p>인정 여부는 고용센터가 판단합니다. 해당한다고 생각되면 증빙을 준비해 상담받으세요.</p>

<h3>신청은 빨리 하셔야 합니다</h3>
<p>구직급여는 <strong>이직일 다음 날부터 12개월 이내</strong>에만 받을 수 있습니다.
이 기간이 지나면 소정급여일수가 남아 있어도 지급이 끝납니다.
퇴직 후 미루지 말고 워크넷 구직등록과 수급자격 신청을 진행하세요.</p>

<h3>실제 절차</h3>
<ol>
<li>회사가 <strong>이직확인서</strong>와 피보험자격 상실 신고를 제출</li>
<li>워크넷에 <strong>구직등록</strong></li>
<li>고용보험 홈페이지에서 <strong>수급자격 신청자 온라인 교육</strong> 수강</li>
<li>거주지 관할 <strong>고용센터 방문</strong> 신청</li>
<li>수급자격 인정 후 <strong>1~4주마다 실업인정</strong> 받으며 지급</li>
</ol>
""",
    faq=[
        (u"자발적으로 퇴사했는데 받을 수 있나요?",
         u"원칙적으로 대상이 아닙니다. 다만 임금체불, 통근 곤란, 괴롭힘 등 정당한 사유가 "
         u"인정되면 예외가 있습니다. 고용센터에서 판단하므로 증빙을 준비해 상담받으세요."),
        (u"상한액과 하한액이 기본값과 다릅니다.",
         u"해마다 바뀝니다. 상한액과 최저임금을 입력 항목으로 열어두었으니 "
         u"고용보험 홈페이지에서 당해 연도 기준을 확인해 넣으세요."),
        (u"180일은 어떻게 세나요?",
         u"이직 전 18개월 동안의 피보험 단위기간을 셉니다. 실제로 보수를 받은 날 기준이라 "
         u"단순 재직일수와 다를 수 있습니다."),
        (u"퇴직하고 언제까지 신청해야 하나요?",
         u"이직일 다음 날부터 12개월 이내입니다. 이 기간이 지나면 남은 일수가 있어도 "
         u"지급이 종료되므로 서둘러 신청하세요."),
        (u"아르바이트를 하면 못 받나요?",
         u"소득이 발생하면 반드시 실업인정 시 신고해야 합니다. 신고하지 않으면 부정수급이 되어 "
         u"반환은 물론 추가 징수와 처벌을 받을 수 있습니다."),
    ],
)

# ───────────────────────── 환율 ─────────────────────────
add(
    slug="hwanyul", name=u"환율 계산기", group=u"부동산·생활",
    title=u"환율 계산기 | 실시간 환율로 원화 환전 금액 계산",
    desc=u"달러·엔·유로 등 주요 통화와 원화를 환산합니다. 실시간 환율을 불러오고 환전 수수료도 반영합니다.",
    kw=u"실시간 환율 환산, 환전 수수료 반영",
    spec=u"""
(function(){
  var RATES=null;   /* 1 외화 = ? 원 */
  var FALLBACK={USD:1380, JPY:9.1, EUR:1490, CNY:190, GBP:1750,
                AUD:900, CAD:1010, HKD:177, THB:39, VND:0.054, SGD:1030, CHF:1560};

  var C = Calc.mount({
    id:"hwanyul",
    formTitle:"환전 정보",
    fields:[
      {k:"dir", label:"방향", type:"seg", options:[
        {value:"f2k", label:"외화 → 원화"}, {value:"k2f", label:"원화 → 외화"}]},
      {k:"cur", label:"통화", type:"select", value:"USD", options:[
        {value:"USD", label:"미국 달러 (USD)"},
        {value:"JPY", label:"일본 엔 (JPY)"},
        {value:"EUR", label:"유로 (EUR)"},
        {value:"CNY", label:"중국 위안 (CNY)"},
        {value:"GBP", label:"영국 파운드 (GBP)"},
        {value:"AUD", label:"호주 달러 (AUD)"},
        {value:"CAD", label:"캐나다 달러 (CAD)"},
        {value:"HKD", label:"홍콩 달러 (HKD)"},
        {value:"SGD", label:"싱가포르 달러 (SGD)"},
        {value:"CHF", label:"스위스 프랑 (CHF)"},
        {value:"THB", label:"태국 바트 (THB)"},
        {value:"VND", label:"베트남 동 (VND)"}]},
      {k:"amount", label:"금액", suffix:"", value:100, step:1, min:0},
      {k:"rate", label:"환율", sub:"1 외화당 원화. 자동으로 채워집니다", suffix:"원", value:1380, step:0.0001, min:0},
      {k:"fee", label:"환전 수수료", sub:"은행 스프레드", suffix:"%", value:0, step:0.1, min:0}
    ],
    compute:function(v,F){
      var r=v.rate||0, a=v.amount||0, fee=(v.fee||0)/100;
      var cur=v.cur||"USD";
      var out, heroK, heroV, sub;

      if(v.dir==="k2f"){
        var eff=r*(1+fee);                 /* 살 때는 비싸게 */
        out = eff>0 ? a/eff : 0;
        heroK="받는 외화"; heroV=F.num(out,2)+" "+cur;
        sub=F.won(a)+" 기준";
      } else {
        var eff2=r*(1-fee);                /* 팔 때는 싸게 */
        out=a*eff2;
        heroK="받는 원화"; heroV=F.kor(out);
        sub=F.num(a,2)+" "+cur+" 기준";
      }

      var jpyNote = cur==="JPY"
        ? "<br>일본 엔은 보통 <b>100엔당</b> 가격으로 표시합니다. 100엔 = "+F.won(r*100)+" 입니다."
        : "";

      return {
        hero:{k:heroK, v:heroV, sub:sub, cls:"up"},
        stats:[
          {k:"적용 환율", v:F.num(r,2)+"원", sub:"1 "+cur},
          {k:"수수료", v: fee? F.pct(v.fee,2) : "없음",
           sub: fee? (v.dir==="k2f"?"살 때 가산":"팔 때 차감") : "은행별로 다름"},
          {k:"수수료 없을 때", v: v.dir==="k2f" ? F.num(r>0?a/r:0,2)+" "+cur : F.won(a*r)}
        ],
        hint:(RATES? "실시간 시세":"기준 시세")+" · 1 "+cur+" = "+F.num(r,2)+"원",
        extra:"<div class='note'>표시되는 환율은 <b>매매기준율</b>에 가까운 참고 시세입니다. "+
          "실제 은행 창구에서는 살 때와 팔 때 값이 달라 <b>스프레드</b>가 붙습니다. "+
          "현찰 환전은 보통 1.5~2%, 송금은 그보다 낮습니다. 수수료 칸에 넣어 비교해 보세요."+
          jpyNote+"</div>"
      };
    }
  });

  /* 실시간 시세. 실패해도 기본값으로 계속 동작한다. */
  function applyRate(){
    var sel=document.getElementById("f_cur"), inp=document.getElementById("f_rate");
    if(!sel||!inp) return;
    var cur=sel.value;
    var r = (RATES && RATES[cur]) || FALLBACK[cur];
    if(r){ inp.value = r>=100 ? r.toFixed(2) : r.toFixed(4); C.run(); }
  }

  var sel=document.getElementById("f_cur");
  if(sel) sel.addEventListener("change", applyRate);

  try{
    fetch("https://open.er-api.com/v6/latest/KRW")
      .then(function(r){ return r.json(); })
      .then(function(d){
        if(!d || !d.rates) return;
        RATES={};
        for(var k in FALLBACK){
          if(d.rates[k]) RATES[k] = 1/d.rates[k];   /* KRW 기준 -> 1외화당 원화 */
        }
        applyRate();
        var h=document.querySelector(".panel-head .hint");
        if(h && d.time_last_update_utc) h.title = "기준 " + d.time_last_update_utc;
      })
      .catch(function(){ /* 조용히 기본값 유지 */ });
  }catch(e){}
})();""",
    guide=u"""
<h3>매매기준율과 실제 환전 금액은 다릅니다</h3>
<p>포털이나 뉴스에서 보는 "달러 환율 1,380원"은 <strong>매매기준율</strong>입니다.
은행이 서로 거래하는 도매 가격에 가까운 값이라, 개인이 창구에서 그 가격으로 바꾸지 못합니다.</p>
<p>은행은 <strong>살 때(Buy)</strong>와 <strong>팔 때(Sell)</strong> 가격을 따로 매깁니다.
그 차이를 <strong>스프레드</strong>라고 하며, 이것이 은행의 수수료입니다.</p>

<h3>스프레드는 방법에 따라 크게 다릅니다</h3>
<div class="tablewrap"><table>
<thead><tr><th>방법</th><th>대략적인 스프레드</th></tr></thead>
<tbody>
<tr><td>공항 환전소</td><td class="n">3~5%</td></tr>
<tr><td>은행 창구 현찰</td><td class="n">1.5~2%</td></tr>
<tr><td>모바일 앱 환전 (우대 적용)</td><td class="n">0.2~1%</td></tr>
<tr><td>해외송금 (전신환)</td><td class="n">1% 내외</td></tr>
<tr><td>해외 카드 결제</td><td class="n">1~2% + 브랜드 수수료</td></tr>
</tbody></table></div>
<p>100만원을 환전할 때 공항에서 4%면 4만원, 앱에서 0.5%면 5천원입니다.
같은 돈인데 3만 5천원 차이가 납니다. 수수료 칸에 숫자를 넣어 비교해 보세요.</p>

<h3>엔화는 100엔 단위로 표시합니다</h3>
<p>일본 엔은 관행적으로 <strong>100엔당 가격</strong>으로 고시합니다.
"엔화 환율 910원"은 100엔이 910원이라는 뜻이고, 1엔은 9.1원입니다.
이 계산기는 <strong>1엔 기준</strong>으로 입력받되, 100엔 환산 금액도 함께 보여드립니다.</p>

<h3>환전 우대율</h3>
<p>은행 앱에서 미리 신청하면 스프레드의 일정 비율을 깎아주는 <strong>환전 우대</strong>가 있습니다.
"90% 우대"는 스프레드를 90% 깎아준다는 뜻이지 환율을 90%로 해준다는 말이 아닙니다.
스프레드가 2%인데 90% 우대면 실제 부담은 0.2%가 됩니다.</p>

<h3>해외 결제는 환전과 다릅니다</h3>
<p>해외에서 카드로 결제하면 카드 브랜드(비자·마스터) 수수료와 국내 카드사 수수료가 붙습니다.
현지 통화로 결제할지 원화로 결제할지 묻는 <strong>DCC</strong>가 뜨면
반드시 <strong>현지 통화</strong>를 고르세요. 원화 결제를 고르면 수수료가 추가로 붙습니다.</p>

<h3>환율은 실시간으로 변합니다</h3>
<p>이 계산기는 공개 환율 API에서 시세를 불러옵니다. 참고용 값이며 실제 거래 시점의
고시 환율과 다를 수 있습니다. 시세를 불러오지 못하면 기준값이 들어가니,
정확한 계산이 필요하면 거래 은행의 고시 환율을 직접 넣어 쓰세요.</p>
""",
    faq=[
        (u"표시된 환율이 은행과 다릅니다.",
         u"이 계산기는 매매기준율에 가까운 참고 시세를 보여줍니다. 은행 창구는 여기에 "
         u"스프레드를 얹은 값을 적용합니다. 수수료 칸에 스프레드를 넣으면 비슷해집니다."),
        (u"엔화 환율이 9원으로 나옵니다.",
         u"이 계산기는 1엔 기준입니다. 뉴스에 나오는 900원대는 100엔 기준이라 100배 차이입니다. "
         u"결과 아래에 100엔 환산 금액도 표시됩니다."),
        (u"환율을 직접 넣을 수 있나요?",
         u"환율 칸을 고쳐 쓰시면 됩니다. 거래 은행 고시 환율을 넣으면 실제와 가까워집니다."),
        (u"수수료는 얼마로 넣어야 하나요?",
         u"공항 환전 3~5%, 은행 창구 1.5~2%, 앱 우대 환전 0.2~1% 정도가 일반적입니다. "
         u"정확한 값은 이용하시는 은행에서 확인하세요."),
    ],
)

# ───────────────────────── 만 나이 ─────────────────────────
add(
    slug="mannai", name=u"만 나이 계산기", group=u"부동산·생활",
    title=u"만 나이 계산기 | 생년월일로 만 나이·연 나이 확인",
    desc=u"생년월일을 넣으면 만 나이와 연 나이를 계산합니다. 다음 생일까지 남은 날짜와 띠도 함께 보여줍니다.",
    kw=u"생년월일로 만 나이·연 나이, 다음 생일",
    spec=u"""
Calc.mount({
  id:"mannai",
  formTitle:"생년월일",
  fields:[
    {k:"birth", label:"생년월일", type:"date", value:"1990-05-15"},
    {k:"base", label:"기준일", sub:"비우면 오늘", type:"date", value:""}
  ],
  compute:function(v,F){
    var D=24*3600*1000;
    var b=new Date((v.birth||"1990-01-01")+"T00:00:00");
    var t=v.base ? new Date(v.base+"T00:00:00") : new Date(new Date().toDateString());
    if(isNaN(b)||isNaN(t)) return {hero:{k:"오류",v:"날짜를 확인해 주세요"}};
    if(t<b) return {hero:{k:"오류",v:"기준일이 생년월일보다 빨라야 합니다"}};

    /* 만 나이: 생일이 지났으면 연도 차, 아니면 하나 뺀다 */
    var man=t.getFullYear()-b.getFullYear();
    var passed = (t.getMonth()>b.getMonth()) ||
                 (t.getMonth()===b.getMonth() && t.getDate()>=b.getDate());
    if(!passed) man--;

    var yeon=t.getFullYear()-b.getFullYear();      /* 연 나이 */
    var sen=yeon+1;                                 /* 옛 세는 나이 */

    /* 다음 생일 */
    var nb=new Date(t.getFullYear(), b.getMonth(), b.getDate());
    if(nb<t) nb=new Date(t.getFullYear()+1, b.getMonth(), b.getDate());
    var left=Math.round((nb-t)/D);
    var lived=Math.round((t-b)/D);

    var zodiac=["쥐","소","호랑이","토끼","용","뱀","말","양","원숭이","닭","개","돼지"];
    var z=zodiac[(b.getFullYear()-4)%12];
    var wd=["일","월","화","수","목","금","토"];

    return {
      hero:{k:"만 나이", v:F.num(man)+"세", cls:"up",
            sub:b.getFullYear()+"년 "+(b.getMonth()+1)+"월 "+b.getDate()+"일생 · "+z+"띠"},
      stats:[
        {k:"연 나이", v:F.num(yeon)+"세", sub:"현재연도 − 출생연도"},
        {k:"다음 생일", v: left===0 ? "오늘!" : "D-"+F.num(left),
         sub:nb.getFullYear()+"."+(nb.getMonth()+1)+"."+nb.getDate()+" ("+wd[nb.getDay()]+")"},
        {k:"태어난 지", v:F.num(lived)+"일", sub:"약 "+F.num(lived/365.25,1)+"년"}
      ],
      hint:(v.base? v.base : "오늘")+" 기준",
      cols:["구분","나이","쓰이는 곳"],
      rows:[
        ["만 나이", man+"세", "법령·계약·공식 문서 (기본)"],
        ["연 나이", yeon+"세", "병역법·청소년보호법·초등 취학"],
        ["세는 나이", sen+"세", "일상 대화 (공식 기준 아님)"]
      ],
      extra:"<div class='note'>2023년 6월부터 법령상 나이는 <b>만 나이로 통일</b>됐습니다. "+
        "별도 규정이 없으면 문서에 적힌 나이는 만 나이입니다. "+
        "다만 <b>병역법과 청소년보호법 등 일부는 여전히 연 나이</b>를 씁니다. "+
        (passed ? "" : "올해 생일이 아직 지나지 않아 만 나이가 연 나이보다 한 살 적습니다.")+"</div>"
    };
  }
});""",
    guide=u"""
<h3>2023년부터 만 나이로 통일됐습니다</h3>
<p>2023년 6월 28일부터 <strong>행정·민사상 나이는 만 나이가 기본</strong>입니다.
법령이나 계약서에 그냥 "나이"라고 적혀 있으면 만 나이로 봅니다.
이전에는 세는 나이, 연 나이, 만 나이가 뒤섞여 혼선이 많았습니다.</p>

<h3>세 가지 나이의 차이</h3>
<div class="tablewrap"><table>
<thead><tr><th>구분</th><th>계산법</th><th>1990년 5월 15일생 기준</th></tr></thead>
<tbody>
<tr><td><strong>만 나이</strong></td><td>생일이 지나면 +1</td><td class="n">생일 전 35세, 후 36세</td></tr>
<tr><td>연 나이</td><td>현재연도 − 출생연도</td><td class="n">36세 (생일 무관)</td></tr>
<tr><td>세는 나이</td><td>연 나이 + 1</td><td class="n">37세</td></tr>
</tbody></table></div>
<p>같은 사람인데 최대 두 살까지 차이가 납니다.
1월 1일에 태어난 사람과 12월 31일에 태어난 사람의 세는 나이가 같았던 것이 혼란의 원인이었습니다.</p>

<h3>아직 연 나이를 쓰는 곳</h3>
<p>만 나이로 통일됐지만 예외가 있습니다.</p>
<ul>
<li><strong>병역법</strong> — 병역 판정검사, 입영 등</li>
<li><strong>청소년보호법</strong> — 주류·담배 구입 제한. 연도 기준이라 생일 전에도 해당 연도에 만 19세가 되면 구매 가능</li>
<li><strong>초·중등교육법</strong> — 취학 연령</li>
<li><strong>공무원임용시험령</strong> 등 일부 응시 연령</li>
</ul>
<p>이런 법에서는 "만 나이"가 아니라 태어난 해를 기준으로 셉니다.</p>

<h3>보험·연금에서의 나이</h3>
<p>보험은 <strong>보험나이</strong>라는 별도 기준을 쓰기도 합니다.
계약일 기준 만 나이에서 6개월이 지났으면 한 살을 더하는 방식입니다.
가입 시점에 따라 보험료가 달라질 수 있으니 약관을 확인하세요.</p>

<h3>왜 헷갈렸나</h3>
<p>만 나이는 <strong>태어난 날부터 1년이 지나야 한 살</strong>입니다.
태어난 순간은 0세이고 첫 생일에 1세가 됩니다.
반면 세는 나이는 태어나자마자 1세이고 해가 바뀌면 한 살을 더합니다.
12월 31일에 태어난 아기는 다음 날 두 살이 됐습니다. 이 방식이 공식 기준에서 사라진 것입니다.</p>
""",
    faq=[
        (u"만 나이와 연 나이가 왜 다른가요?",
         u"만 나이는 생일이 지나야 한 살이 오르고, 연 나이는 생일과 무관하게 "
         u"현재 연도에서 출생 연도를 뺍니다. 생일 전이면 만 나이가 한 살 적습니다."),
        (u"술·담배는 어느 나이 기준인가요?",
         u"청소년보호법은 연 나이를 씁니다. 해당 연도에 만 19세가 되는 사람은 "
         u"생일이 지나지 않았어도 구매할 수 있습니다."),
        (u"이제 세는 나이는 안 쓰나요?",
         u"법령상 공식 기준에서는 쓰지 않습니다. 다만 일상 대화에서는 여전히 쓰이므로 "
         u"참고용으로 함께 표시합니다."),
        (u"계약서의 나이는 어느 기준인가요?",
         u"별도 규정이 없으면 만 나이입니다. 2023년 6월부터 그렇게 정해졌습니다."),
    ],
)

# ───────────────────────── 주택담보대출 한도 ─────────────────────────
add(
    slug="ltv", name=u"주택담보대출 한도 계산기", group=u"대출·예금",
    title=u"주택담보대출 한도 계산기 | LTV·DSR 기준 대출 가능 금액",
    desc=u"주택가격과 연소득으로 LTV와 DSR 기준 대출 한도를 각각 계산하고, 실제 받을 수 있는 금액을 알려줍니다.",
    kw=u"LTV·DSR 기준 대출 가능 금액과 월 상환액",
    spec=u"""
Calc.mount({
  id:"ltv",
  formTitle:"대출 조건",
  sideNote:"LTV와 DSR 규제 비율은 지역·주택수·정책에 따라 수시로 바뀝니다. 금융기관에서 본인 적용 기준을 확인하세요.",
  fields:[
    {k:"price", label:"주택가격", suffix:"원", value:600000000, step:10000000, min:0},
    {k:"ltv", label:"LTV 비율", sub:"규제지역·주택수에 따라 다름", suffix:"%", value:70, step:5, min:0},
    {k:"income", label:"연소득", sub:"세전", suffix:"원", value:60000000, step:1000000, min:0},
    {k:"dsr", label:"DSR 한도", sub:"은행권 통상 40%", suffix:"%", value:40, step:5, min:0},
    {k:"other", label:"기존 대출 연간 원리금", sub:"신용대출·기존 주담대 등", suffix:"원", value:0, step:1000000, min:0},
    {k:"rate", label:"연이자율", suffix:"%", value:4.5, step:0.01, min:0},
    {k:"years", label:"대출기간", suffix:"년", value:30, step:1, min:1}
  ],
  compute:function(v,F){
    var price=v.price||0, income=v.income||0;
    var i=(v.rate||0)/100/12, n=Math.max(1,Math.round((v.years||1)*12));

    var ltvCap = price*(v.ltv||0)/100;

    /* DSR: 연간 원리금상환액이 연소득의 일정 비율을 넘지 못한다 */
    var allowed = income*(v.dsr||0)/100 - (v.other||0);
    var factor = i>0 ? i*Math.pow(1+i,n)/(Math.pow(1+i,n)-1) : 1/n;   /* 월상환/원금 */
    var dsrCap = allowed>0 ? allowed/(12*factor) : 0;

    var limit=Math.min(ltvCap, dsrCap);
    var binding = dsrCap<ltvCap ? "DSR" : "LTV";
    var monthly=limit*factor;
    var need=price-limit;

    return {
      hero:{k:"대출 가능 금액", v:F.kor(limit), sub:F.won(limit), cls:"up"},
      stats:[
        {k:"LTV 기준", v:F.kor(ltvCap), sub:"주택가 × "+F.num(v.ltv,0)+"%",
         cls: binding==="LTV" ? "down":""},
        {k:"DSR 기준", v:F.kor(Math.max(dsrCap,0)), sub:"연소득 × "+F.num(v.dsr,0)+"%",
         cls: binding==="DSR" ? "down":""},
        {k:"월 상환액", v:F.won(monthly), sub:F.num(v.years,0)+"년 원리금균등"}
      ],
      hint:binding+" 가 한도를 결정",
      extra:"<div class='note'>"+
        "<b>"+binding+"</b> 기준이 더 낮아 실제 한도를 결정합니다. "+
        "자기자금은 <b>"+F.kor(need)+"</b> 가 필요합니다"+
        (need>0 ? " (취득세·중개보수 별도)" : "")+".<br><br>"+
        (dsrCap<ltvCap
          ? "소득이 한도를 묶고 있습니다. 기간을 늘리면 연간 상환액이 줄어 DSR 한도가 올라갑니다."
          : "담보가 한도를 묶고 있습니다. 소득이 늘어도 LTV 이상은 받을 수 없습니다.")+
        "</div>",
      cols:["대출기간","월 상환액","DSR 기준 한도"],
      rows:[10,15,20,25,30,35,40].map(function(y){
        var m=y*12;
        var f = i>0 ? i*Math.pow(1+i,m)/(Math.pow(1+i,m)-1) : 1/m;
        var cap = allowed>0 ? allowed/(12*f) : 0;
        var lim = Math.min(ltvCap, cap);
        return [y+"년", F.won(lim*f), F.kor(Math.max(cap,0))];
      }),
      tableHint:"기간별 비교"
    };
  }
});""",
    guide=u"""
<h3>한도는 두 가지 중 낮은 쪽으로 정해집니다</h3>
<p><strong>LTV</strong>는 집값 대비, <strong>DSR</strong>은 소득 대비 한도입니다.
둘 다 통과해야 하므로 <strong>더 낮은 쪽이 실제 한도</strong>가 됩니다.</p>
<ul>
<li><strong>LTV (주택담보인정비율)</strong> = 대출금 ÷ 주택가격.
70%면 6억 집에 4.2억까지입니다.</li>
<li><strong>DSR (총부채원리금상환비율)</strong> = 연간 원리금상환액 ÷ 연소득.
40%면 연소득 6천만원인 사람은 연 2,400만원, 월 200만원까지만 갚을 수 있습니다.</li>
</ul>

<h3>DSR이 막히는 경우가 많습니다</h3>
<p>집값이 올라도 소득이 그대로면 DSR에서 걸립니다.
연소득 6천만원에 DSR 40%면 월 상환액 200만원이 상한인데,
금리 4.5%에 30년이면 대출 약 3.9억이 한계입니다.
집이 10억이어도 LTV와 무관하게 여기서 막힙니다.</p>

<h3>기간을 늘리면 DSR 한도가 올라갑니다</h3>
<p>같은 금액이라도 30년으로 나누면 40년으로 나눌 때보다 월 상환액이 큽니다.
기간을 늘리면 연간 상환액이 줄어 DSR 한도가 올라갑니다.
다만 <strong>총 이자는 크게 늘어납니다.</strong> 계산기 아래 표에서 기간별 차이를 비교해 보세요.</p>

<h3>기존 대출이 한도를 갉아먹습니다</h3>
<p>DSR은 <strong>모든 대출</strong>의 원리금을 합산합니다.
신용대출, 자동차 할부, 카드론, 학자금 대출이 전부 들어갑니다.
마이너스 통장은 한도 금액 기준으로 잡히는 경우가 많습니다.
주담대를 받기 전에 다른 대출을 정리하면 한도가 늘어납니다.</p>

<h3>규제 비율은 계속 바뀝니다</h3>
<p>LTV는 규제지역 여부, 주택 수, 생애최초 여부에 따라 달라집니다.
DSR도 대출 규모와 금융권(은행·2금융)에 따라 다르게 적용되고,
스트레스 DSR처럼 가산금리를 얹어 계산하는 제도가 도입되기도 합니다.</p>
<p>이 계산기는 비율을 <strong>직접 입력</strong>하도록 열어두었습니다.
본인에게 적용되는 수치를 금융기관에서 확인해 넣으세요.</p>

<h3>집값 외에 필요한 돈</h3>
<p>대출로 안 되는 금액이 자기자금인데, 여기에 <strong>취득세와 중개보수</strong>가 더 듭니다.
6억 주택이면 취득세만 660만원 안팎입니다.
<a href="../chwideukse/">취득세 계산기</a>와 <a href="../brokerage/">중개보수 계산기</a>로
함께 계산해 보세요.</p>
""",
    faq=[
        (u"LTV는 되는데 DSR에서 막힙니다.",
         u"둘 다 통과해야 해서 낮은 쪽이 한도가 됩니다. 대출기간을 늘리거나 기존 대출을 "
         u"줄이면 DSR 한도가 올라갑니다."),
        (u"마이너스 통장도 DSR에 잡히나요?",
         u"보통 약정 한도 기준으로 잡힙니다. 실제로 안 썼어도 한도가 있으면 부채로 계산되는 "
         u"경우가 많으니 금융기관에 확인하세요."),
        (u"LTV 비율을 얼마로 넣어야 하나요?",
         u"규제지역 여부, 주택 수, 생애최초 여부에 따라 다릅니다. 정책이 자주 바뀌므로 "
         u"금융기관에서 본인 적용 비율을 확인해 넣으세요."),
        (u"전세대출도 DSR에 들어가나요?",
         u"전세자금대출은 이자만 반영되거나 제외되는 등 취급이 달라져 왔습니다. "
         u"시점과 상품에 따라 다르므로 확인이 필요합니다."),
    ],
)

# ───────────────────────── 증여세 ─────────────────────────
add(
    slug="jeungyeo", name=u"증여세 계산기", group=u"사업·세금",
    title=u"증여세 계산기 | 증여재산공제와 세율 적용",
    desc=u"증여재산가액과 증여자와의 관계로 증여세를 계산합니다. 증여재산공제와 신고세액공제를 반영합니다.",
    kw=u"관계별 증여재산공제 반영한 증여세",
    spec=u"""
Calc.mount({
  id:"jeungyeo",
  formTitle:"증여 정보",
  sideNote:"10년 이내 같은 관계에서 받은 증여는 합산해 계산합니다. 공제 한도도 10년 기준입니다.",
  fields:[
    {k:"amount", label:"증여재산가액", suffix:"원", value:200000000, step:10000000, min:0},
    {k:"prior", label:"10년 내 사전증여", sub:"같은 증여자에게 받은 금액", suffix:"원", value:0, step:10000000, min:0},
    {k:"rel", label:"증여자와의 관계", type:"select", value:"lineal", options:[
      {value:"spouse", label:"배우자 (6억 공제)"},
      {value:"lineal", label:"직계존속 → 성년 자녀 (5천만)"},
      {value:"minor", label:"직계존속 → 미성년 자녀 (2천만)"},
      {value:"down", label:"직계비속 → 부모 (5천만)"},
      {value:"rel6", label:"기타 친족 (1천만)"},
      {value:"none", label:"타인 (공제 없음)"}]},
    {k:"wedding", label:"혼인·출산 공제", sub:"직계존속에게 받을 때, 1억 한도", suffix:"원", value:0, step:10000000, min:0},
    {k:"report", label:"기한 내 신고", type:"seg", options:[
      {value:"1", label:"신고 (3% 공제)"}, {value:"0", label:"미신고"}]}
  ],
  compute:function(v,F){
    var gift=(v.amount||0)+(v.prior||0);
    var BASE={spouse:600000000, lineal:50000000, minor:20000000,
              down:50000000, rel6:10000000, none:0};
    var ded=BASE[v.rel]||0;
    var wed = (v.rel==="lineal"||v.rel==="minor") ? Math.min(v.wedding||0, 100000000) : 0;
    var totalDed=ded+wed;

    var base=Math.max(0, gift-totalDed);
    var t=[[100000000,.10,0],[500000000,.20,10000000],[1000000000,.30,60000000],
           [3000000000,.40,160000000],[Infinity,.50,460000000]];
    var tax=0, rateNote="";
    for(var i=0;i<t.length;i++) if(base<=t[i][0]){ tax=base*t[i][1]-t[i][2]; rateNote=(t[i][1]*100)+"%"; break; }
    tax=Math.max(0,tax);

    var credit = v.report==1 ? tax*0.03 : 0;
    var pay=tax-credit;

    return {
      hero:{k:"납부할 증여세", v:F.kor(pay), sub:F.won(pay), cls: pay>0?"down":"up"},
      stats:[
        {k:"증여재산공제", v:F.won(totalDed), sub: wed? "기본 "+F.kor(ded)+" + 혼인·출산 "+F.kor(wed) : "10년 합산 한도"},
        {k:"과세표준", v:F.won(base), sub:"세율 "+rateNote},
        {k:"실수령", v:F.won((v.amount||0)-pay), cls:"up"}
      ],
      hint: base<=0 ? "공제 범위 내 — 세금 없음" : "세율 "+rateNote,
      cols:["단계","금액"],
      rows:[
        ["증여재산가액", F.won(v.amount||0)],
        ["10년 내 사전증여", "+ "+F.won(v.prior||0)],
        ["합산 증여재산", F.won(gift)],
        ["증여재산공제", "− "+F.won(totalDed)],
        ["과세표준", F.won(base)],
        ["산출세액 ("+rateNote+")", F.won(tax)],
        ["신고세액공제 3%", "− "+F.won(credit)],
        ["납부세액", F.won(pay)]
      ],
      extra:"<div class='note'>"+
        (base<=0 ? "공제 한도 안이라 낼 세금이 없습니다. 다만 <b>신고는 하는 편이 안전합니다.</b> "+
                   "나중에 자금출처를 소명해야 할 때 근거가 됩니다.<br><br>" : "")+
        "증여세는 <b>받는 사람(수증자)</b>이 냅니다. 신고·납부 기한은 증여받은 날이 속한 달의 "+
        "말일부터 <b>3개월 이내</b>입니다. 기한을 넘기면 신고세액공제 3%를 못 받고 가산세가 붙습니다.<br><br>"+
        "공제 한도는 <b>10년 단위로 합산</b>합니다. 5년 전에 부모에게 3천만원을 받았다면 "+
        "이번에 쓸 수 있는 공제는 2천만원뿐입니다.</div>"
    };
  }
});""",
    guide=u"""
<h3>증여세는 받는 사람이 냅니다</h3>
<p>주는 사람이 아니라 <strong>받는 사람(수증자)</strong>이 신고하고 납부합니다.
신고·납부 기한은 증여받은 날이 속한 달의 말일부터 <strong>3개월 이내</strong>입니다.</p>

<h3>관계에 따라 공제액이 다릅니다</h3>
<div class="tablewrap"><table>
<thead><tr><th>증여자</th><th>공제 한도 (10년)</th></tr></thead>
<tbody>
<tr><td>배우자</td><td class="n">6억원</td></tr>
<tr><td>직계존속 → 성년 자녀</td><td class="n">5,000만원</td></tr>
<tr><td>직계존속 → 미성년 자녀</td><td class="n">2,000만원</td></tr>
<tr><td>직계비속 → 부모</td><td class="n">5,000만원</td></tr>
<tr><td>기타 친족 (6촌 이내 혈족 등)</td><td class="n">1,000만원</td></tr>
<tr><td>타인</td><td class="n">없음</td></tr>
</tbody></table></div>

<h3>10년 합산이 핵심입니다</h3>
<p>공제 한도는 <strong>10년 동안 합쳐서</strong> 적용됩니다.
부모에게 5년 전에 3,000만원을 받았다면, 지금 쓸 수 있는 공제는 2,000만원뿐입니다.
10년이 지나면 한도가 다시 채워집니다.</p>
<p>이 때문에 자녀가 어릴 때부터 10년 단위로 나눠 증여하는 방식이 많이 쓰입니다.
미성년일 때 2,000만원, 성년이 된 뒤 5,000만원 식입니다.</p>

<h3>혼인·출산 증여재산공제</h3>
<p>직계존속에게 증여받는 경우, 혼인신고 전후 2년 이내 또는 출산·입양 후 2년 이내라면
<strong>1억원까지 추가 공제</strong>를 받을 수 있습니다.
기본 공제 5,000만원과 합치면 1억 5,000만원까지 세금 없이 받을 수 있습니다.
요건과 적용 시점이 정해져 있으니 국세청이나 세무 전문가에게 확인하세요.</p>

<h3>세율</h3>
<div class="tablewrap"><table>
<thead><tr><th>과세표준</th><th>세율</th><th>누진공제</th></tr></thead>
<tbody>
<tr><td>1억원 이하</td><td class="n">10%</td><td class="n">—</td></tr>
<tr><td>5억원 이하</td><td class="n">20%</td><td class="n">1,000만원</td></tr>
<tr><td>10억원 이하</td><td class="n">30%</td><td class="n">6,000만원</td></tr>
<tr><td>30억원 이하</td><td class="n">40%</td><td class="n">1억 6,000만원</td></tr>
<tr><td>30억원 초과</td><td class="n">50%</td><td class="n">4억 6,000만원</td></tr>
</tbody></table></div>

<h3>기한 내 신고하면 3%를 깎아줍니다</h3>
<p>기한 안에 신고하면 산출세액의 <strong>3%를 신고세액공제</strong>로 빼줍니다.
반대로 기한을 넘기면 이 공제를 못 받고 무신고가산세(20%)와 납부지연가산세가 붙습니다.</p>

<h3>세금이 없어도 신고하는 편이 낫습니다</h3>
<p>공제 범위 안이라 낼 세금이 없더라도 신고해 두면 <strong>자금 출처 근거</strong>가 됩니다.
나중에 부동산을 사거나 큰돈이 오갈 때 자금출처조사를 받게 되면
"증여받은 돈"이라는 것을 입증해야 하는데, 신고 내역이 그 근거가 됩니다.</p>

<h3>이 계산기가 다루지 않는 것</h3>
<p>부담부증여(채무를 함께 넘기는 경우), 창업자금·가업승계 특례, 비상장주식 평가,
부동산의 시가 산정, 재차증여 합산의 세부 규정은 반영하지 않았습니다.
금액이 크거나 부동산·주식이 포함되면 반드시 세무 전문가와 상담하세요.</p>
""",
    faq=[
        (u"부모에게 1억을 받으면 세금이 얼마인가요?",
         u"성년 자녀 기준 공제 5,000만원을 빼면 과세표준 5,000만원, 세율 10%로 산출세액 500만원입니다. "
         u"기한 내 신고하면 3% 공제로 485만원입니다."),
        (u"세금이 없으면 신고 안 해도 되나요?",
         u"의무는 아니지만 하는 편이 안전합니다. 나중에 자금출처를 소명해야 할 때 근거가 됩니다."),
        (u"10년이 지나면 공제가 다시 생기나요?",
         u"네. 공제 한도는 10년 단위로 합산하므로 마지막 증여로부터 10년이 지나면 다시 채워집니다."),
        (u"혼인 공제 1억은 누구나 받나요?",
         u"직계존속에게 받는 경우로, 혼인신고 전후 2년 또는 출산·입양 후 2년 이내라는 요건이 있습니다. "
         u"국세청 기준을 확인하세요."),
        (u"부동산을 증여받으면 어떻게 계산하나요?",
         u"시가 평가가 필요하고 취득세도 별도로 발생합니다. 이 계산기는 현금 기준의 개략 계산이므로 "
         u"부동산은 세무 전문가 상담을 권합니다."),
    ],
)

# ───────────────────────── 종합소득세 ─────────────────────────
add(
    slug="jonghap", name=u"종합소득세 계산기", group=u"사업·세금",
    title=u"종합소득세 계산기 | 프리랜서·사업자 5월 신고 세액",
    desc=u"총수입금액과 필요경비로 종합소득세를 계산합니다. 인적공제와 누진세율, 지방소득세를 반영합니다.",
    kw=u"프리랜서·사업자 종합소득세 개략 계산",
    spec=u"""
Calc.mount({
  id:"jonghap",
  formTitle:"소득 정보",
  sideNote:"단순경비율·기준경비율 적용 대상은 업종과 수입 규모에 따라 다릅니다. 홈택스에서 본인 기준을 확인하세요.",
  fields:[
    {k:"revenue", label:"총수입금액", sub:"1년 매출", suffix:"원", value:60000000, step:1000000, min:0},
    {k:"mode", label:"필요경비", type:"seg", options:[
      {value:"rate", label:"경비율 적용"}, {value:"direct", label:"직접 입력"}]},
    {k:"expRate", label:"경비율", sub:"업종별 단순경비율", suffix:"%", value:64.1, step:0.1, min:0},
    {k:"expense", label:"필요경비 금액", sub:"직접 입력 시", suffix:"원", value:0, step:1000000, min:0},
    {k:"family", label:"부양가족", sub:"본인 포함", suffix:"명", value:1, step:1, min:1},
    {k:"pension", label:"연금보험료 공제", sub:"국민연금 등 납부액", suffix:"원", value:0, step:100000, min:0},
    {k:"prepaid", label:"기납부세액", sub:"원천징수 3.3% 등", suffix:"원", value:0, step:100000, min:0}
  ],
  compute:function(v,F){
    var rev=v.revenue||0;
    var exp = v.mode==="direct" ? (v.expense||0) : rev*(v.expRate||0)/100;
    exp=Math.min(exp,rev);
    var income=rev-exp;

    var personal=1500000*Math.max(1,v.family||1);
    var ded=personal+(v.pension||0);
    var base=Math.max(0, income-ded);

    var t=[[14000000,.06,0],[50000000,.15,1260000],[88000000,.24,5760000],
           [150000000,.35,15440000],[300000000,.38,19940000],[500000000,.40,25940000],
           [1000000000,.42,35940000],[Infinity,.45,65940000]];
    var tax=0, rateNote="";
    for(var i=0;i<t.length;i++) if(base<=t[i][0]){ tax=base*t[i][1]-t[i][2]; rateNote=(t[i][1]*100)+"%"; break; }
    tax=Math.max(0,tax);

    var standard=70000;                       /* 표준세액공제 */
    var income_tax=Math.max(0, tax-standard);
    var local=income_tax*0.1;
    var total=income_tax+local;
    var due=total-(v.prepaid||0);

    return {
      hero:{k: due>=0 ? "추가 납부액" : "환급 예상액",
            v:F.kor(Math.abs(due)), sub:F.won(Math.abs(due)),
            cls: due>=0 ? "down":"up"},
      stats:[
        {k:"소득금액", v:F.won(income), sub:"수입 − 경비"},
        {k:"결정세액", v:F.won(total), sub:"지방소득세 포함"},
        {k:"기납부세액", v:F.won(v.prepaid||0), sub:"원천징수 등"}
      ],
      hint:"과세표준 "+F.kor(base)+" · 세율 "+rateNote,
      cols:["단계","금액"],
      rows:[
        ["총수입금액", F.won(rev)],
        ["필요경비", "− "+F.won(exp)],
        ["소득금액", F.won(income)],
        ["인적공제 ("+F.num(v.family)+"명)", "− "+F.won(personal)],
        ["연금보험료공제", "− "+F.won(v.pension||0)],
        ["과세표준", F.won(base)],
        ["산출세액 ("+rateNote+")", F.won(tax)],
        ["표준세액공제", "− "+F.won(Math.min(standard,tax))],
        ["소득세", F.won(income_tax)],
        ["지방소득세 10%", F.won(local)],
        ["결정세액", F.won(total)],
        ["기납부세액", "− "+F.won(v.prepaid||0)],
        [due>=0?"추가 납부":"환급", F.won(Math.abs(due))]
      ],
      extra:"<div class='note'>종합소득세 신고 기한은 <b>매년 5월 1일~31일</b>입니다 "+
        "(성실신고확인 대상은 6월 말). 프리랜서는 보통 3.3%가 원천징수되어 있으니 "+
        "<b>기납부세액</b> 칸에 넣으면 환급인지 추가 납부인지 나옵니다.<br><br>"+
        "의료비·교육비·기부금·연금저축·노란우산공제 등 개인별 공제는 반영하지 않았습니다. "+
        "이런 공제가 있으면 실제 세액은 이보다 줄어듭니다.</div>"
    };
  }
});""",
    guide=u"""
<h3>누가 신고하나</h3>
<p>근로소득만 있고 연말정산을 마쳤다면 따로 신고하지 않아도 됩니다.
다음에 해당하면 <strong>5월에 종합소득세를 신고</strong>해야 합니다.</p>
<ul>
<li>프리랜서 (3.3% 원천징수를 받는 인적용역 소득자)</li>
<li>개인사업자</li>
<li>근로소득 외에 사업·임대·기타소득이 있는 경우</li>
<li>두 곳 이상에서 근로소득이 있는데 합산 연말정산을 하지 않은 경우</li>
</ul>

<h3>필요경비를 어떻게 잡느냐가 세금을 좌우합니다</h3>
<p>수입에서 경비를 빼야 소득금액이 나옵니다. 방법은 두 가지입니다.</p>
<p><strong>장부 작성 (직접 입력)</strong> — 실제 쓴 비용을 증빙과 함께 경비로 인정받습니다.
경비가 많은 업종이면 유리하고, 적자면 결손금으로 이월할 수도 있습니다.</p>
<p><strong>경비율 적용 (추계신고)</strong> — 장부가 없을 때 업종별로 정해진 비율만큼 경비로 인정합니다.
<strong>단순경비율</strong>은 수입이 적은 사업자에게 적용되고 비율이 높아 유리합니다.
수입이 일정 규모를 넘으면 비율이 낮은 <strong>기준경비율</strong> 대상이 되어 세금이 크게 늘 수 있습니다.</p>
<p>업종별 경비율과 적용 대상 기준은 국세청이 고시합니다. 홈택스에서 본인 업종 코드로 확인하세요.</p>

<h3>프리랜서 3.3%는 미리 낸 세금입니다</h3>
<p>용역비에서 3.3%(소득세 3% + 지방소득세 0.3%)가 원천징수됩니다.
이것은 <strong>세금을 다 낸 것이 아니라 미리 낸 것</strong>입니다.
5월에 실제 세액을 계산해 더 냈으면 돌려받고, 덜 냈으면 더 냅니다.</p>
<p>수입이 적으면 대부분 환급을 받습니다. 반대로 수입이 커서 높은 세율 구간에 들어가면
추가 납부가 나옵니다. 기납부세액 칸에 원천징수된 금액을 넣어 확인해 보세요.</p>

<h3>세율 구간</h3>
<div class="tablewrap"><table>
<thead><tr><th>과세표준</th><th>세율</th><th>누진공제</th></tr></thead>
<tbody>
<tr><td>1,400만원 이하</td><td class="n">6%</td><td class="n">—</td></tr>
<tr><td>5,000만원 이하</td><td class="n">15%</td><td class="n">126만원</td></tr>
<tr><td>8,800만원 이하</td><td class="n">24%</td><td class="n">576만원</td></tr>
<tr><td>1억 5,000만원 이하</td><td class="n">35%</td><td class="n">1,544만원</td></tr>
<tr><td>3억원 이하</td><td class="n">38%</td><td class="n">1,994만원</td></tr>
<tr><td>5억원 이하</td><td class="n">40%</td><td class="n">2,594만원</td></tr>
<tr><td>10억원 이하</td><td class="n">42%</td><td class="n">3,594만원</td></tr>
<tr><td>10억원 초과</td><td class="n">45%</td><td class="n">6,594만원</td></tr>
</tbody></table></div>
<p>여기에 지방소득세가 소득세의 10%만큼 더 붙습니다.</p>

<h3>세금을 줄이는 합법적인 방법</h3>
<ul>
<li><strong>노란우산공제</strong> — 소기업·소상공인 공제부금. 연 최대 500만원 소득공제</li>
<li><strong>연금저축·IRP</strong> — 세액공제</li>
<li><strong>국민연금 보험료</strong> — 전액 소득공제</li>
<li><strong>장부 작성</strong> — 경비를 제대로 반영하고 기장세액공제도 받을 수 있습니다</li>
</ul>
<p>이 계산기는 인적공제와 연금보험료만 반영합니다. 위 항목이 있으면 실제 세금은 더 줄어듭니다.</p>

<h3>부가세와는 다른 세금입니다</h3>
<p>부가가치세는 1월·7월에 신고하고, 종합소득세는 5월에 신고합니다.
별개의 세금이니 둘 다 챙기셔야 합니다.
부가세는 <a href="../bugagse/">부가세 계산기</a>에서 확인하실 수 있습니다.</p>
""",
    faq=[
        (u"프리랜서인데 3.3% 떼고 받았습니다. 또 내야 하나요?",
         u"3.3%는 미리 낸 세금입니다. 5월에 실제 세액을 계산해 정산합니다. "
         u"수입이 적으면 보통 환급받고, 많으면 추가 납부가 나옵니다."),
        (u"경비율을 얼마로 넣어야 하나요?",
         u"업종별로 국세청이 고시합니다. 홈택스에서 본인 업종 코드의 단순경비율·기준경비율을 "
         u"확인해 넣으세요. 기본값은 예시입니다."),
        (u"장부를 쓰는 게 유리한가요?",
         u"실제 경비가 경비율보다 많으면 장부가 유리합니다. 수입이 커지면 기준경비율 대상이 되어 "
         u"인정 경비가 줄기 때문에 장부 작성이 사실상 필요해집니다."),
        (u"근로소득도 있는데 어떻게 하나요?",
         u"근로소득과 사업소득을 합산해 신고해야 합니다. 이 계산기는 사업·기타소득 단독 기준의 "
         u"개략 계산이므로 합산 신고는 홈택스나 세무 전문가를 이용하세요."),
        (u"신고 기한을 놓치면 어떻게 되나요?",
         u"무신고가산세와 납부지연가산세가 붙습니다. 기한 후 신고를 빨리 할수록 가산세가 줄어듭니다."),
    ],
)

# ───────────────────────── 연말정산 환급금 ─────────────────────────
add(
    slug="yeonmal", name=u"연말정산 환급금 계산기", group=u"급여·노무",
    title=u"연말정산 계산기 | 환급금·추가납부액 미리 계산",
    desc=u"총급여와 공제 항목으로 연말정산 결정세액을 계산하고, 이미 낸 세금과 비교해 환급 또는 추가 납부액을 알려줍니다.",
    kw=u"신용카드·의료비·연금저축 반영한 환급 예상액",
    spec=u"""
Calc.mount({
  id:"yeonmal",
  formTitle:"급여와 공제",
  sideNote:"주요 공제만 반영한 개략 계산입니다. 정확한 금액은 홈택스 연말정산 미리보기를 이용하세요.",
  fields:[
    {k:"pay", label:"총급여", sub:"연간, 비과세 제외", suffix:"원", value:50000000, step:1000000, min:0},
    {k:"prepaid", label:"기납부세액", sub:"올해 원천징수된 소득세 합계", suffix:"원", value:2000000, step:100000, min:0},
    {k:"family", label:"부양가족", sub:"본인 포함", suffix:"명", value:1, step:1, min:1},
    {k:"child", label:"20세 이하 자녀", suffix:"명", value:0, step:1, min:0},
    {k:"card", label:"신용·체크카드 사용액", suffix:"원", value:15000000, step:1000000, min:0},
    {k:"medical", label:"의료비", suffix:"원", value:0, step:100000, min:0},
    {k:"edu", label:"교육비", suffix:"원", value:0, step:100000, min:0},
    {k:"insur", label:"보장성 보험료", sub:"연 100만 한도", suffix:"원", value:0, step:100000, min:0},
    {k:"pension", label:"연금저축·IRP 납입액", sub:"연 900만 한도", suffix:"원", value:0, step:100000, min:0},
    {k:"donate", label:"기부금", suffix:"원", value:0, step:100000, min:0}
  ],
  compute:function(v,F){
    var g=v.pay||0;

    /* 근로소득공제 */
    var wd;
    if(g<=5000000) wd=g*0.7;
    else if(g<=15000000) wd=3500000+(g-5000000)*0.4;
    else if(g<=45000000) wd=7500000+(g-15000000)*0.15;
    else if(g<=100000000) wd=12000000+(g-45000000)*0.05;
    else wd=14750000+(g-100000000)*0.02;
    wd=Math.min(wd,20000000);

    /* 4대보험 근로자 부담 (개략) */
    var ins = Math.min(g,74040000)*0.045 + g*0.03545*1.1295 + g*0.009;

    var personal=1500000*Math.max(1,v.family||1);

    /* 신용카드 소득공제: 총급여 25% 초과분 × 15%, 한도 300만 */
    var threshold=g*0.25;
    var cardDed=Math.max(0, (v.card||0)-threshold)*0.15;
    var cardCap = g<=70000000 ? 3000000 : 2500000;
    cardDed=Math.min(cardDed, cardCap);

    var base=Math.max(0, g-wd-personal-ins-cardDed);

    function calcTax(b){
      var t=[[14000000,.06,0],[50000000,.15,1260000],[88000000,.24,5760000],
             [150000000,.35,15440000],[300000000,.38,19940000],[500000000,.40,25940000],
             [1000000000,.42,35940000],[Infinity,.45,65940000]];
      for(var i=0;i<t.length;i++) if(b<=t[i][0]) return b*t[i][1]-t[i][2];
      return 0;
    }
    var gross=Math.max(0,calcTax(base));

    /* 근로소득세액공제 */
    var wc = gross<=1300000 ? gross*0.55 : 715000+(gross-1300000)*0.30;
    var wcCap = g<=33000000 ? 740000
              : g<=70000000 ? Math.max(660000, 740000-(g-33000000)*0.008)
              : Math.max(500000, 660000-(g-70000000)*0.005);
    wc=Math.min(wc,wcCap);

    var childC=(v.child||0)>0 ? ((v.child==1)?150000:(v.child==2)?350000:350000+(v.child-2)*300000) : 0;
    var insurC=Math.min(v.insur||0,1000000)*0.12;
    var medC=Math.max(0,(v.medical||0)-g*0.03)*0.15;
    var eduC=(v.edu||0)*0.15;
    var donC=(v.donate||0)*0.15;
    var penRate = g<=55000000 ? 0.15 : 0.12;
    var penC=Math.min(v.pension||0,9000000)*penRate;

    var credits=wc+childC+insurC+medC+eduC+donC+penC;
    var income=Math.max(0, gross-credits);
    var local=income*0.1;
    var decided=income+local;
    var refund=(v.prepaid||0)-decided;

    return {
      hero:{k: refund>=0 ? "환급 예상액" : "추가 납부액",
            v:F.kor(Math.abs(refund)), sub:F.won(Math.abs(refund)),
            cls: refund>=0 ? "up":"down"},
      stats:[
        {k:"결정세액", v:F.won(decided), sub:"지방소득세 포함"},
        {k:"기납부세액", v:F.won(v.prepaid||0)},
        {k:"세액공제 합계", v:F.won(credits), cls:"up"}
      ],
      hint: refund>=0 ? "돌려받습니다" : "더 내야 합니다",
      cols:["단계","금액"],
      rows:[
        ["총급여", F.won(g)],
        ["근로소득공제", "− "+F.won(wd)],
        ["인적공제 ("+F.num(v.family)+"명)", "− "+F.won(personal)],
        ["4대보험료", "− "+F.won(ins)],
        ["신용카드 소득공제", "− "+F.won(cardDed)],
        ["과세표준", F.won(base)],
        ["산출세액", F.won(gross)],
        ["근로소득세액공제", "− "+F.won(wc)],
        ["자녀세액공제", "− "+F.won(childC)],
        ["보험료·의료비·교육비·기부금", "− "+F.won(insurC+medC+eduC+donC)],
        ["연금저축 ("+(penRate*100)+"%)", "− "+F.won(penC)],
        ["소득세", F.won(income)],
        ["지방소득세 10%", F.won(local)],
        ["결정세액", F.won(decided)],
        [refund>=0?"환급":"추가 납부", F.won(Math.abs(refund))]
      ],
      extra:"<div class='note'>"+
        "신용카드는 <b>총급여의 25%를 넘게 쓴 부분</b>만 공제됩니다. "+
        "여기서는 "+F.won(threshold)+" 를 넘는 금액이 대상입니다."+
        ((v.card||0)<threshold ? " <b>지금 사용액은 기준에 못 미쳐 공제가 없습니다.</b>" : "")+
        "<br><br>의료비는 <b>총급여의 3%를 넘는 부분</b>만 공제됩니다 ("+F.won(g*0.03)+" 초과분).<br><br>"+
        "체크카드·현금영수증은 공제율이 더 높고(30%), 전통시장·대중교통은 별도 추가 공제가 있습니다. "+
        "여기서는 신용카드 기준 15%로 단순화했습니다. 월세액·주택자금·기부금 유형별 차등 등은 "+
        "반영하지 않았으니 실제 금액은 홈택스 미리보기로 확인하세요.</div>"
    };
  }
});""",
    guide=u"""
<h3>연말정산은 정산입니다</h3>
<p>회사는 매달 <strong>간이세액표</strong>에 따라 대략적인 소득세를 떼어 갑니다.
이건 어림잡아 미리 낸 금액입니다. 한 해가 끝나면 실제로 내야 할 세금(결정세액)을 계산해서,
더 냈으면 <strong>돌려받고(환급)</strong> 덜 냈으면 <strong>더 냅니다(추가 납부)</strong>.</p>
<p>그래서 "13월의 월급"이라는 말이 나오지만, 반대로 토해내는 경우도 있습니다.
환급이 많다고 좋은 것도 아닙니다. 그만큼 1년 동안 세금을 과하게 내고 있었다는 뜻이기도 합니다.</p>

<h3>소득공제와 세액공제는 다릅니다</h3>
<p><strong>소득공제</strong>는 세금을 매기는 <em>대상 금액</em>을 줄입니다.
신용카드, 인적공제, 4대보험료가 여기 해당합니다.
같은 100만원 공제라도 세율이 높은 사람이 더 많이 아낍니다.</p>
<p><strong>세액공제</strong>는 계산된 <em>세금 자체</em>를 깎습니다.
의료비, 교육비, 연금저축, 기부금이 여기 해당합니다.
소득에 관계없이 깎이는 금액이 같습니다.</p>

<h3>신용카드는 총급여의 25%를 넘겨야 시작됩니다</h3>
<p>가장 오해가 많은 부분입니다. 카드를 아무리 써도 <strong>총급여의 25%까지는 공제가 0원</strong>입니다.
연봉 5,000만원이면 1,250만원을 넘게 쓴 부분부터 공제 대상입니다.</p>
<p>공제율도 결제 수단에 따라 다릅니다.</p>
<div class="tablewrap"><table>
<thead><tr><th>수단</th><th>공제율</th></tr></thead>
<tbody>
<tr><td>신용카드</td><td class="n">15%</td></tr>
<tr><td>체크카드·현금영수증</td><td class="n">30%</td></tr>
<tr><td>전통시장·대중교통</td><td class="n">40% (추가 한도 별도)</td></tr>
</tbody></table></div>
<p>따라서 <strong>25%까지는 혜택 좋은 신용카드로 쓰고, 그 위로는 체크카드를 쓰는 것</strong>이
공제 측면에서 유리합니다. 이 계산기는 신용카드 기준 15%로 단순화했습니다.</p>

<h3>의료비도 문턱이 있습니다</h3>
<p>의료비는 <strong>총급여의 3%를 넘는 부분</strong>만 공제됩니다.
연봉 5,000만원이면 150만원을 넘게 쓴 금액부터입니다.
안경·콘택트렌즈(1인 50만원 한도), 산후조리원(200만원 한도)도 포함됩니다.
다만 미용·성형 목적이나 건강기능식품은 제외됩니다.</p>

<h3>연금저축·IRP가 가장 확실한 절세 수단입니다</h3>
<p>연금저축과 IRP를 합쳐 <strong>연 900만원까지</strong> 세액공제를 받습니다.
총급여 5,500만원 이하면 15%, 초과하면 12%입니다.
900만원을 채우면 총급여 5,500만원 이하인 사람은 <strong>135만원</strong>을 돌려받습니다.</p>
<p>다른 공제와 달리 <strong>내가 결정해서 늘릴 수 있는 항목</strong>이라는 점이 중요합니다.
다만 55세 이후 연금으로 받아야 하고 중도 인출하면 세금을 토해내니 여유자금으로 하셔야 합니다.</p>

<h3>맞벌이라면 누구에게 몰아줄지 계산해 보세요</h3>
<p>부양가족 공제는 한 사람만 받을 수 있습니다.
일반적으로 <strong>소득이 높은 쪽</strong>에 몰아주는 것이 유리하지만,
의료비처럼 <em>총급여의 3% 초과분</em>만 인정되는 항목은
<strong>소득이 낮은 쪽</strong>이 문턱이 낮아 유리할 수 있습니다.
두 경우를 각각 계산해 비교해 보세요.</p>

<h3>이 계산기의 한계</h3>
<p>월세액 세액공제, 주택자금·주택청약 공제, 기부금 유형별 차등,
중소기업 취업자 감면, 출산·입양 공제, 장애인·경로우대 추가공제는 반영하지 않았습니다.
결과는 개략적인 추정이며, 정확한 금액은
<strong>국세청 홈택스의 연말정산 미리보기</strong>에서 확인하세요.</p>
""",
    faq=[
        (u"카드를 많이 썼는데 공제가 0원으로 나옵니다.",
         u"신용카드 공제는 총급여의 25%를 넘게 쓴 부분부터 시작됩니다. "
         u"연봉 5,000만원이면 1,250만원을 넘겨야 공제가 생깁니다."),
        (u"환급을 많이 받으려면 어떻게 해야 하나요?",
         u"내가 조절할 수 있는 항목은 연금저축·IRP 납입액입니다. 연 900만원까지 12~15% "
         u"세액공제를 받습니다. 다만 55세 이후 연금 수령이 전제입니다."),
        (u"기납부세액은 어디서 확인하나요?",
         u"급여명세서의 소득세를 1년치 합하거나, 원천징수영수증의 기납부세액 항목을 보시면 됩니다."),
        (u"맞벌이인데 누구에게 몰아야 하나요?",
         u"보통 소득이 높은 쪽이 유리하지만, 의료비처럼 총급여 대비 문턱이 있는 항목은 "
         u"소득이 낮은 쪽이 유리할 수 있습니다. 두 경우를 계산해 비교해 보세요."),
        (u"계산 결과가 실제와 다릅니다.",
         u"주요 공제만 반영한 개략 계산입니다. 월세·주택자금·중소기업 감면 등은 빠져 있어 "
         u"실제 환급액은 더 클 수 있습니다. 홈택스 미리보기로 확인하세요."),
    ],
)

# ───────────────────────── 재산세 ─────────────────────────
add(
    slug="jaesanse", name=u"재산세 계산기", group=u"부동산·생활",
    title=u"재산세 계산기 | 주택 공시가격으로 재산세 계산",
    desc=u"주택 공시가격으로 재산세와 도시지역분, 지방교육세를 계산합니다. 1주택 특례세율도 반영합니다.",
    kw=u"공시가격 기준 재산세·도시지역분·지방교육세",
    spec=u"""
Calc.mount({
  id:"jaesanse",
  formTitle:"주택 정보",
  sideNote:"공정시장가액비율과 특례세율은 해마다 정책에 따라 조정됩니다. 위택스에서 확인하세요.",
  fields:[
    {k:"price", label:"공시가격", sub:"시세 아님", suffix:"원", value:500000000, step:10000000, min:0},
    {k:"ratio", label:"공정시장가액비율", sub:"주택 통상 60%", suffix:"%", value:60, step:1, min:0},
    {k:"special", label:"1세대 1주택 특례", sub:"공시 9억 이하", type:"seg", options:[
      {value:"0", label:"미적용"}, {value:"1", label:"적용"}]},
    {k:"urban", label:"도시지역분 포함", type:"seg", options:[
      {value:"1", label:"포함"}, {value:"0", label:"제외"}]}
  ],
  compute:function(v,F){
    var p=v.price||0;
    var base=p*(v.ratio||0)/100;
    var useSpecial = v.special==1 && p<=900000000;

    /* 표준 / 1주택 특례 누진구조 */
    var T = useSpecial
      ? [[60000000,.0005,0],[150000000,.001,30000],[300000000,.002,180000],[Infinity,.0035,630000]]
      : [[60000000,.001,0],[150000000,.0015,30000],[300000000,.0025,180000],[Infinity,.004,630000]];

    var tax=0, rateNote="";
    for(var i=0;i<T.length;i++) if(base<=T[i][0]){ tax=base*T[i][1]-T[i][2]; rateNote=(T[i][1]*100).toFixed(3).replace(/0+$/,"").replace(/\\.$/,"")+"%"; break; }
    tax=Math.max(0,tax);

    var urban = v.urban==1 ? base*0.0014 : 0;
    var edu = tax*0.2;
    var total = tax+urban+edu;

    return {
      hero:{k:"재산세 등 합계", v:F.kor(total), sub:F.won(total), cls:"down"},
      stats:[
        {k:"재산세 본세", v:F.won(tax), sub:"세율 "+rateNote+(useSpecial?" (특례)":"")},
        {k:"도시지역분", v: v.urban==1 ? F.won(urban) : "—", sub:"과세표준 0.14%"},
        {k:"지방교육세", v:F.won(edu), sub:"재산세의 20%"}
      ],
      hint:"과세표준 "+F.kor(base)+" (공시 × "+F.num(v.ratio,0)+"%)",
      cols:["단계","금액"],
      rows:[
        ["공시가격", F.won(p)],
        ["공정시장가액비율 "+F.num(v.ratio,0)+"%", "× "+F.num(v.ratio,0)+"%"],
        ["과세표준", F.won(base)],
        ["재산세 본세", F.won(tax)],
        ["도시지역분", F.won(urban)],
        ["지방교육세", F.won(edu)],
        ["합계", F.won(total)]
      ],
      extra:"<div class='note'>"+
        (v.special==1 && p>900000000
          ? "<b>공시가격 9억원을 초과해 1주택 특례세율이 적용되지 않습니다.</b> 표준세율로 계산했습니다.<br><br>"
          : "")+
        "재산세는 <b>매년 6월 1일</b> 소유자에게 부과됩니다. 5월 31일에 팔면 안 내고, "+
        "6월 2일에 팔면 그해 재산세를 냅니다. 잔금일을 정할 때 흔히 다투는 지점입니다.<br><br>"+
        "주택은 <b>7월과 9월에 절반씩</b> 나눠 고지됩니다(세액 20만원 이하면 7월에 일괄). "+
        "공시가격이 급등해도 전년 대비 일정 비율을 넘지 못하게 하는 <b>세부담상한</b>이 있어 "+
        "실제 고지액은 이 계산보다 적을 수 있습니다.</div>"
    };
  }
});""",
    guide=u"""
<h3>6월 1일이 기준일입니다</h3>
<p>재산세는 <strong>매년 6월 1일 현재 소유자</strong>에게 1년치가 부과됩니다.
하루 차이로 부담자가 바뀝니다.</p>
<ul>
<li>5월 31일에 잔금을 치르면 → <strong>매수인</strong>이 냅니다</li>
<li>6월 2일에 잔금을 치르면 → <strong>매도인</strong>이 냅니다</li>
</ul>
<p>매매 계약할 때 잔금일을 6월 1일 전후로 조정하는 이유가 이것입니다.</p>

<h3>시세가 아니라 공시가격 기준입니다</h3>
<p>10억에 산 집이라도 공시가격이 6억이면 6억을 기준으로 계산합니다.
공시가격은 국토교통부가 매년 발표하며 부동산공시가격 알리미에서 확인할 수 있습니다.</p>
<p>여기에 <strong>공정시장가액비율</strong>을 곱해 과세표준을 만듭니다.
주택은 통상 60%이고, 1주택자에게는 더 낮은 비율을 적용하기도 합니다.
공시 6억이면 과세표준은 3억 6천만원입니다.</p>

<h3>세율</h3>
<div class="tablewrap"><table>
<thead><tr><th>과세표준</th><th>표준세율</th><th>1주택 특례 (공시 9억 이하)</th></tr></thead>
<tbody>
<tr><td>6,000만원 이하</td><td class="n">0.1%</td><td class="n">0.05%</td></tr>
<tr><td>1억 5,000만원 이하</td><td class="n">0.15%</td><td class="n">0.1%</td></tr>
<tr><td>3억원 이하</td><td class="n">0.25%</td><td class="n">0.2%</td></tr>
<tr><td>3억원 초과</td><td class="n">0.4%</td><td class="n">0.35%</td></tr>
</tbody></table></div>
<p>1세대 1주택이고 공시가격이 9억원 이하면 특례세율로 절반 가까이 줄어듭니다.</p>

<h3>본세만 내는 게 아닙니다</h3>
<ul>
<li><strong>재산세 본세</strong> — 위 세율로 계산</li>
<li><strong>도시지역분</strong> — 과세표준의 0.14%. 도시계획구역에 부과</li>
<li><strong>지방교육세</strong> — 재산세 본세의 20%</li>
</ul>
<p>고지서에 이 셋이 합쳐져 나옵니다. 본세만 생각하면 실제 고지액보다 적게 예상하게 됩니다.</p>

<h3>7월과 9월에 나눠 냅니다</h3>
<p>주택 재산세는 절반씩 두 번 고지됩니다. 7월(7/16~7/31)과 9월(9/16~9/30)입니다.
다만 세액이 20만원 이하면 7월에 한 번에 부과됩니다.
건축물은 7월, 토지는 9월에 냅니다.</p>

<h3>세부담상한</h3>
<p>공시가격이 급등해도 전년도 세액 대비 일정 비율 이상 오르지 못하도록 상한이 있습니다.
공시가격이 크게 올랐다면 실제 고지액은 이 계산보다 적을 수 있습니다.
이 계산기는 상한을 반영하지 않습니다.</p>

<h3>종합부동산세는 별개입니다</h3>
<p>재산세를 내고도 공시가격 합계가 기준을 넘으면 12월에 종합부동산세를 추가로 냅니다.
1주택자는 공시 12억, 다주택자는 9억이 기준입니다(정책에 따라 변동).
이 계산기는 재산세만 다룹니다.</p>
""",
    faq=[
        (u"6월 1일에 집을 팔면 누가 내나요?",
         u"6월 1일 현재 소유자가 냅니다. 6월 1일에 잔금을 치러 소유권이 넘어갔다면 매수인이 부담합니다. "
         u"잔금일을 정할 때 미리 협의하는 편이 좋습니다."),
        (u"공시가격은 어디서 보나요?",
         u"국토교통부 부동산공시가격 알리미에서 조회할 수 있습니다. 시세와는 다릅니다."),
        (u"고지서 금액이 계산과 다릅니다.",
         u"세부담상한이 적용되었거나 지자체별 탄력세율, 감면이 반영됐을 수 있습니다. "
         u"위택스에서 상세 내역을 확인하세요."),
        (u"1주택 특례는 자동으로 적용되나요?",
         u"1세대 1주택이고 공시가격이 9억원 이하면 적용됩니다. 세대 기준이므로 "
         u"세대원의 주택 보유 현황에 따라 달라집니다."),
    ],
)

# ───────────────────────── 자동차세 ─────────────────────────
add(
    slug="jadongchase", name=u"자동차세 계산기", group=u"부동산·생활",
    title=u"자동차세 계산기 | 배기량·차령 기준 자동차세",
    desc=u"배기량과 차령으로 자동차세를 계산합니다. 지방교육세와 연납 할인, 차령 감면을 반영합니다.",
    kw=u"배기량·차령 기준 자동차세와 연납 할인",
    spec=u"""
Calc.mount({
  id:"jadongchase",
  formTitle:"차량 정보",
  fields:[
    {k:"kind", label:"차종", type:"select", value:"car", options:[
      {value:"car", label:"승용차 (비영업용)"},
      {value:"ev", label:"전기·수소차 (비영업용)"},
      {value:"van", label:"승합차 (비영업용)"}]},
    {k:"cc", label:"배기량", sub:"전기차는 무관", suffix:"cc", value:1998, step:1, min:0},
    {k:"age", label:"차령", sub:"최초 등록 후 경과 연수", suffix:"년", value:3, step:1, min:0},
    {k:"prepay", label:"연납 할인율", sub:"1월 일시납 시", suffix:"%", value:0, step:0.5, min:0}
  ],
  compute:function(v,F){
    var cc=v.cc||0, age=Math.max(0,Math.round(v.age||0));
    var base, note;

    if(v.kind==="ev"){ base=130000; note="전기·수소차 정액"; }
    else if(v.kind==="van"){ base=65000; note="승합차 정액(소형 기준)"; }
    else {
      var rate = cc<=1000 ? 80 : cc<=1600 ? 140 : 200;
      base = cc*rate;
      note = "배기량 "+F.num(cc)+"cc × "+rate+"원";
    }

    /* 차령 감면: 3년차부터 매년 5%, 최대 50% */
    var cut = age>=3 ? Math.min(50, (age-2)*5) : 0;
    var tax = Math.floor(base*(1-cut/100)/10)*10;
    var edu = Math.floor(tax*0.3/10)*10;
    var year = tax+edu;
    var discounted = year*(1-(v.prepay||0)/100);

    return {
      hero:{k:"연간 자동차세", v:F.kor(year), sub:F.won(year), cls:"down"},
      stats:[
        {k:"자동차세 본세", v:F.won(tax), sub: cut? "차령 감면 "+cut+"%" : note},
        {k:"지방교육세", v:F.won(edu), sub:"본세의 30%"},
        {k:"연납 시", v: v.prepay ? F.won(discounted) : "—", cls: v.prepay?"up":"",
         sub: v.prepay ? F.num(v.prepay,1)+"% 할인" : "할인율 입력 시"}
      ],
      hint:note+(cut? " · 차령 "+age+"년 감면 "+cut+"%":""),
      cols:["차령","감면율","연간 세액"],
      rows:[0,1,2,3,4,5,7,9,11,12].map(function(a){
        var c = a>=3 ? Math.min(50,(a-2)*5) : 0;
        var t = Math.floor(base*(1-c/100)/10)*10;
        return [a+"년", c+"%", F.won(t+Math.floor(t*0.3/10)*10)];
      }),
      tableHint:"차령별 세액",
      extra:"<div class='note'>자동차세는 <b>6월과 12월에 절반씩</b> 부과됩니다. "+
        "1월에 1년치를 미리 내면 <b>연납 할인</b>을 받을 수 있습니다(할인율은 해마다 조정). "+
        "3월·6월·9월에도 남은 기간에 대해 신청할 수 있지만 할인폭은 줄어듭니다.<br><br>"+
        "차령 감면은 <b>3년차부터 매년 5%씩, 최대 50%</b>까지입니다. "+
        "차를 오래 탈수록 세금이 줄어듭니다. 영업용 차량은 세율 체계가 다릅니다.</div>"
    };
  }
});""",
    guide=u"""
<h3>배기량 곱하기 세율이 전부입니다</h3>
<p>비영업용 승용차 기준입니다.</p>
<div class="tablewrap"><table>
<thead><tr><th>배기량</th><th>cc당 세액</th><th>2,000cc 예시</th></tr></thead>
<tbody>
<tr><td>1,000cc 이하</td><td class="n">80원</td><td class="n">—</td></tr>
<tr><td>1,600cc 이하</td><td class="n">140원</td><td class="n">—</td></tr>
<tr><td>1,600cc 초과</td><td class="n">200원</td><td class="n">40만원</td></tr>
</tbody></table></div>
<p>2,000cc 차량이면 본세 40만원, 지방교육세 12만원(본세의 30%)을 더해 <strong>52만원</strong>입니다.</p>

<h3>1,600cc가 경계선입니다</h3>
<p>1,600cc는 140원, 1,601cc는 200원입니다. cc당 60원 차이라 배기량이 조금만 넘어도
세금이 크게 뜁니다. 1,598cc 차량이 많은 데는 이런 배경도 있습니다.</p>

<h3>오래 탈수록 세금이 줄어듭니다</h3>
<p>차령 3년차부터 <strong>매년 5%씩 감면</strong>되며 최대 50%까지 줄어듭니다.
12년이 지나면 절반만 냅니다.</p>
<div class="tablewrap"><table>
<thead><tr><th>차령</th><th>감면율</th><th>차령</th><th>감면율</th></tr></thead>
<tbody>
<tr><td>2년 이하</td><td class="n">0%</td><td>8년</td><td class="n">30%</td></tr>
<tr><td>3년</td><td class="n">5%</td><td>10년</td><td class="n">40%</td></tr>
<tr><td>5년</td><td class="n">15%</td><td>12년 이상</td><td class="n">50%</td></tr>
</tbody></table></div>

<h3>1월에 미리 내면 할인받습니다</h3>
<p>자동차세는 원래 <strong>6월과 12월에 절반씩</strong> 냅니다.
1월에 1년치를 한 번에 내면 연납 할인을 받습니다.
할인율은 정책에 따라 조정되어 왔으니 해당 연도 고시를 확인하세요.</p>
<p>3월·6월·9월에도 신청할 수 있지만 남은 기간분만 할인되어 폭이 줄어듭니다.
연초에 신청하는 것이 가장 유리합니다.</p>

<h3>전기차는 정액입니다</h3>
<p>전기차와 수소차는 배기량이 없어 <strong>정액</strong>으로 부과됩니다.
비영업용 승용 기준 13만원에 지방교육세를 더해 약 17만원 수준입니다.
2,000cc 내연기관차의 3분의 1 수준이라 유지비 차이가 큽니다.</p>

<h3>차를 팔거나 사면</h3>
<p>자동차세는 소유 기간에 따라 <strong>일할 계산</strong>됩니다.
연납한 뒤 중도에 팔면 남은 기간분을 환급받습니다.
반대로 중고차를 사면 그 시점부터의 세금을 부담합니다.</p>

<h3>안 내면 어떻게 되나</h3>
<p>납부기한을 넘기면 가산금이 붙고, 체납이 계속되면 번호판 영치나 차량 압류로 이어집니다.
자동차 검사나 명의 이전에도 제약이 생깁니다.</p>
""",
    faq=[
        (u"내 차 배기량을 모르겠습니다.",
         u"자동차등록증에 배기량이 적혀 있습니다. 차량 제원표나 보험증권에서도 확인할 수 있습니다."),
        (u"연납 할인율이 기본값과 다릅니다.",
         u"할인율은 정책에 따라 조정되어 왔습니다. 할인율 칸에 해당 연도 기준을 넣어 계산하세요."),
        (u"중고차를 샀는데 세금은 어떻게 되나요?",
         u"소유 기간에 따라 일할 계산됩니다. 이전 소유자가 연납했다면 그쪽이 환급받고 "
         u"매수인은 취득일부터 부담합니다."),
        (u"영업용 차량도 같나요?",
         u"영업용은 세율 체계가 다르고 훨씬 낮습니다. 이 계산기는 비영업용 기준입니다."),
    ],
)

# ───────────────────────── 중도상환수수료 ─────────────────────────
add(
    slug="jungdo", name=u"중도상환수수료 계산기", group=u"대출·예금",
    title=u"중도상환수수료 계산기 | 대출 조기상환 수수료와 손익 비교",
    desc=u"중도상환수수료를 계산하고, 아끼는 이자와 비교해 지금 갚는 것이 유리한지 확인합니다.",
    kw=u"조기상환 수수료와 아끼는 이자 비교",
    spec=u"""
Calc.mount({
  id:"jungdo",
  formTitle:"대출 정보",
  fields:[
    {k:"balance", label:"남은 대출 잔액", suffix:"원", value:200000000, step:10000000, min:0},
    {k:"repay", label:"중도상환 금액", suffix:"원", value:100000000, step:10000000, min:0},
    {k:"rate", label:"수수료율", sub:"약정서 기준, 통상 0.7~1.4%", suffix:"%", value:1.2, step:0.1, min:0},
    {k:"term", label:"약정기간", suffix:"개월", value:36, step:1, min:1},
    {k:"passed", label:"경과기간", suffix:"개월", value:12, step:1, min:0},
    {k:"loanRate", label:"대출 금리", sub:"아끼는 이자 계산용", suffix:"%", value:4.5, step:0.01, min:0},
    {k:"left", label:"남은 대출기간", suffix:"개월", value:240, step:1, min:1}
  ],
  compute:function(v,F){
    var repay=Math.min(v.repay||0, v.balance||0);
    var term=Math.max(1,Math.round(v.term||1));
    var passed=Math.round(v.passed||0);
    var remain=Math.max(0, term-passed);

    /* 슬라이딩 방식: 잔여기간에 비례해 줄어든다 */
    var fee = passed>=term ? 0 : repay*(v.rate||0)/100*(remain/term);

    /* 아끼는 이자(개략): 잔여기간 동안 그 금액에 붙었을 이자 */
    var i=(v.loanRate||0)/100/12, n=Math.max(1,Math.round(v.left||1));
    var saved = i>0 ? repay*(Math.pow(1+i,n)-1) : 0;
    /* 원리금균등 상환 중이라면 실제 절감은 이보다 작다. 단순 이자 기준 상한으로 본다. */
    var simple = repay*(v.loanRate||0)/100*(n/12);

    var net = simple-fee;

    return {
      hero:{k:"중도상환수수료", v: fee>0 ? F.kor(fee) : "면제", sub: fee>0? F.won(fee):"약정기간 경과",
            cls: fee>0?"down":"up"},
      stats:[
        {k:"잔여 약정기간", v: remain+"개월", sub:"약정 "+term+"개월 중"},
        {k:"아끼는 이자", v:F.won(simple), cls:"up", sub:"남은 "+F.num(n)+"개월 단순이자"},
        {k:"순이익", v:F.won(net), cls: net>0?"up":"down", sub: net>0? "갚는 쪽이 유리":"수수료가 더 큼"}
      ],
      hint: fee>0 ? "슬라이딩 방식 · 잔여 "+remain+"/"+term+"개월" : "수수료 없음",
      cols:["경과","잔여 약정","수수료"],
      rows:[0,6,12,18,24,30,36].filter(function(m){return m<=term;}).map(function(m){
        var r2=Math.max(0,term-m);
        return [m+"개월", r2+"개월", F.won(repay*(v.rate||0)/100*(r2/term))];
      }),
      tableHint:"경과기간별 수수료",
      extra:"<div class='note'>대부분의 대출은 <b>3년(36개월)이 지나면 중도상환수수료가 면제</b>됩니다. "+
        "그 안에 갚을 때는 <b>잔여기간에 비례해</b> 수수료가 줄어드는 슬라이딩 방식이 일반적입니다.<br><br>"+
        "<b>수수료 계산 방식은 상품마다 다릅니다.</b> 정액률, 슬라이딩, 면제 한도 등이 약정서에 적혀 있으니 "+
        "반드시 확인하세요. 여기 표시되는 '아끼는 이자'는 단순이자 기준 상한이며, "+
        "원리금균등으로 상환 중이라면 실제 절감액은 이보다 작습니다.</div>"
    };
  }
});""",
    guide=u"""
<h3>3년이 넘으면 대개 면제입니다</h3>
<p>주택담보대출과 신용대출 대부분은 <strong>대출 실행일로부터 3년이 지나면
중도상환수수료가 없습니다.</strong> 갈아타기를 고민한다면 먼저 3년이 지났는지 확인하세요.</p>

<h3>3년 안이라면 잔여기간에 비례합니다</h3>
<p>대부분 <strong>슬라이딩 방식</strong>을 씁니다.</p>
<p><strong>수수료 = 중도상환금액 × 수수료율 × (잔여기간 ÷ 약정기간)</strong></p>
<p>1억원을 수수료율 1.2%, 약정 36개월 중 12개월이 지난 시점에 갚는다면
1억 × 1.2% × (24÷36) = <strong>80만원</strong>입니다.
같은 조건에서 30개월이 지났다면 20만원으로 줄어듭니다.
버틸수록 수수료가 줄어드는 구조입니다.</p>

<h3>갚는 게 이득인지 판단하는 법</h3>
<p>수수료보다 <strong>앞으로 낼 이자</strong>가 크면 갚는 쪽이 유리합니다.
1억을 4.5%로 20년 더 쓴다면 단순이자만 9,000만원입니다.
수수료 80만원과 비교가 되지 않습니다.</p>
<p>반대로 남은 기간이 얼마 없다면 수수료가 더 클 수 있습니다.
계산기의 <strong>순이익</strong> 항목이 이 비교를 해줍니다.</p>

<h3>대환(갈아타기)할 때 따져야 할 것</h3>
<p>금리가 낮은 상품으로 갈아탈 때는 수수료 외에도 비용이 붙습니다.</p>
<ul>
<li>중도상환수수료</li>
<li>근저당권 설정비·말소비</li>
<li>인지세</li>
<li>새 대출의 취급 조건 (금리, 한도, 우대조건)</li>
</ul>
<p>금리를 0.5%p 낮춰도 이 비용을 회수하는 데 시간이 걸립니다.
<a href="../loan/">대출 이자 계산기</a>로 갈아타기 전후 총이자를 비교해 보세요.</p>

<h3>일부 상환도 수수료가 붙습니다</h3>
<p>전액이 아니라 일부만 갚아도 그 금액에 대해 수수료가 발생합니다.
다만 상품에 따라 <strong>연간 일정 금액까지는 면제</strong>해 주는 경우가 있습니다.
원금의 10% 같은 식입니다. 약정서에서 면제 한도를 확인하면 수수료 없이 원금을 줄일 수 있습니다.</p>

<h3>방식은 상품마다 다릅니다</h3>
<p>이 계산기는 가장 흔한 슬라이딩 방식으로 계산합니다.
정액률을 적용하거나 계산식이 다른 상품도 있으니
<strong>약정서나 금융기관 확인이 필요합니다.</strong></p>
""",
    faq=[
        (u"3년이 지났는데도 수수료가 있나요?",
         u"대부분 면제되지만 상품에 따라 다릅니다. 경과기간을 약정기간 이상으로 넣으면 "
         u"면제로 계산됩니다. 실제 여부는 약정서를 확인하세요."),
        (u"일부만 갚아도 수수료가 붙나요?",
         u"갚은 금액에 대해 발생합니다. 다만 연간 일정 금액까지 면제해 주는 상품이 많으니 "
         u"면제 한도를 확인해 보세요."),
        (u"갈아타는 게 이득인지 어떻게 아나요?",
         u"수수료와 설정비를 합한 비용보다 금리 인하로 아끼는 이자가 크면 유리합니다. "
         u"대출 이자 계산기로 갈아타기 전후 총이자를 비교해 보세요."),
        (u"아끼는 이자가 실제와 다릅니다.",
         u"단순이자 기준 상한으로 계산합니다. 원리금균등으로 상환 중이라면 이미 갚은 원금이 있어 "
         u"실제 절감액은 이보다 작습니다."),
    ],
)

# ───────────────────────── 상속세 ─────────────────────────
add(
    slug="sangsokse", name=u"상속세 계산기", group=u"사업·세금",
    title=u"상속세 계산기 | 일괄공제·배우자공제 반영 상속세",
    desc=u"상속재산에서 채무와 상속공제를 빼고 상속세를 계산합니다. 일괄공제 5억, 배우자공제, 금융재산공제를 반영합니다.",
    kw=u"일괄공제·배우자공제 반영한 상속세",
    spec=u"""
Calc.mount({
  id:"sangsokse",
  formTitle:"상속 정보",
  sideNote:"공제 요건이 까다롭고 재산 평가가 결과를 좌우합니다. 실제 신고는 세무 전문가 확인이 필요합니다.",
  fields:[
    {k:"estate", label:"상속재산 총액", sub:"부동산·예금·주식 등", suffix:"원", value:1500000000, step:100000000, min:0},
    {k:"financial", label:"그중 금융재산", sub:"예금·주식 등 (채무 차감 후)", suffix:"원", value:300000000, step:10000000, min:0},
    {k:"debt", label:"채무·장례비", suffix:"원", value:0, step:10000000, min:0},
    {k:"spouse", label:"배우자 생존", type:"seg", options:[
      {value:"1", label:"있음"}, {value:"0", label:"없음"}]},
    {k:"spouseShare", label:"배우자 실제 상속분", sub:"배우자공제 한도 계산용", suffix:"원", value:500000000, step:100000000, min:0},
    {k:"report", label:"기한 내 신고", type:"seg", options:[
      {value:"1", label:"신고 (3% 공제)"}, {value:"0", label:"미신고"}]}
  ],
  compute:function(v,F){
    var gross=(v.estate||0)-(v.debt||0);
    if(gross<0) gross=0;

    /* 일괄공제 5억 (기초공제 2억 + 인적공제 와 비교해 큰 쪽. 보통 일괄이 유리) */
    var lump=500000000;

    /* 배우자상속공제: 최소 5억, 실제 상속분 한도, 최대 30억 */
    var spouseDed = v.spouse==1
      ? Math.min(3000000000, Math.max(500000000, Math.min(v.spouseShare||0, gross)))
      : 0;

    /* 금융재산상속공제: 순금융재산의 20%, 최대 2억. 2천만 이하는 전액 */
    var fin=Math.max(0, Math.min(v.financial||0, gross));
    var finDed = fin<=20000000 ? fin : Math.min(200000000, fin*0.2);

    var totalDed=lump+spouseDed+finDed;
    var base=Math.max(0, gross-totalDed);

    var t=[[100000000,.10,0],[500000000,.20,10000000],[1000000000,.30,60000000],
           [3000000000,.40,160000000],[Infinity,.50,460000000]];
    var tax=0, rateNote="";
    for(var i=0;i<t.length;i++) if(base<=t[i][0]){ tax=base*t[i][1]-t[i][2]; rateNote=(t[i][1]*100)+"%"; break; }
    tax=Math.max(0,tax);

    var credit = v.report==1 ? tax*0.03 : 0;
    var pay=tax-credit;

    return {
      hero:{k:"납부할 상속세", v: pay>0 ? F.kor(pay) : "없음", sub: pay>0? F.won(pay):"공제 범위 내",
            cls: pay>0?"down":"up"},
      stats:[
        {k:"상속공제 합계", v:F.kor(totalDed), sub:"일괄 5억"+(spouseDed?" + 배우자 "+F.kor(spouseDed):"")},
        {k:"과세표준", v:F.kor(base), sub: base>0? "세율 "+rateNote : "과세 없음"},
        {k:"실수령", v:F.kor(gross-pay), cls:"up"}
      ],
      hint: base<=0 ? "공제 범위 내 — 세금 없음" : "세율 "+rateNote,
      cols:["단계","금액"],
      rows:[
        ["상속재산 총액", F.won(v.estate||0)],
        ["채무·장례비", "− "+F.won(v.debt||0)],
        ["과세가액", F.won(gross)],
        ["일괄공제", "− "+F.won(lump)],
        ["배우자상속공제", "− "+F.won(spouseDed)],
        ["금융재산상속공제", "− "+F.won(finDed)],
        ["과세표준", F.won(base)],
        ["산출세액 ("+rateNote+")", F.won(tax)],
        ["신고세액공제 3%", "− "+F.won(credit)],
        ["납부세액", F.won(pay)]
      ],
      extra:"<div class='note'>"+
        (v.spouse==1
          ? "배우자가 있으면 <b>일괄공제 5억 + 배우자공제 최소 5억 = 10억</b> 까지는 상속세가 없는 것이 일반적입니다.<br><br>"
          : "배우자가 없으면 일괄공제 <b>5억</b> 이 기본입니다. 자녀만 상속받는 경우 문턱이 낮아집니다.<br><br>")+
        "신고·납부 기한은 상속개시일이 속한 달의 말일부터 <b>6개월 이내</b>입니다. "+
        "세액이 크면 <b>연부연납</b>(최대 10년 분할)이나 물납을 신청할 수 있습니다.<br><br>"+
        "<b>10년 이내 사전증여</b>는 상속재산에 합산됩니다. 미리 증여했다고 끝나는 것이 아닙니다. "+
        "동거주택상속공제, 가업상속공제, 부동산 평가 방법은 반영하지 않았습니다.</div>"
    };
  }
});""",
    guide=u"""
<h3>10억까지는 대개 세금이 없습니다</h3>
<p>배우자가 살아 있다면 <strong>일괄공제 5억 + 배우자상속공제 최소 5억</strong>으로
10억원까지는 상속세가 나오지 않는 것이 일반적입니다.
배우자가 없고 자녀만 상속받으면 일괄공제 5억이 기본이라 문턱이 낮아집니다.</p>

<h3>주요 공제</h3>
<ul>
<li><strong>일괄공제 5억원</strong> — 기초공제 2억 + 인적공제를 합한 금액과 비교해 큰 쪽을 씁니다.
대부분 일괄공제 5억이 유리합니다.</li>
<li><strong>배우자상속공제</strong> — 배우자가 실제로 상속받은 금액만큼 공제하되,
최소 5억원은 보장되고 최대 30억원까지입니다.
실제로 상속받지 않아도 5억은 공제됩니다.</li>
<li><strong>금융재산상속공제</strong> — 순금융재산의 20%, 최대 2억원.
예금과 주식이 많으면 도움이 됩니다.</li>
<li><strong>동거주택상속공제</strong> — 요건을 갖춘 1주택은 최대 6억원.
이 계산기는 반영하지 않았습니다.</li>
</ul>

<h3>세율은 증여세와 같습니다</h3>
<div class="tablewrap"><table>
<thead><tr><th>과세표준</th><th>세율</th><th>누진공제</th></tr></thead>
<tbody>
<tr><td>1억원 이하</td><td class="n">10%</td><td class="n">—</td></tr>
<tr><td>5억원 이하</td><td class="n">20%</td><td class="n">1,000만원</td></tr>
<tr><td>10억원 이하</td><td class="n">30%</td><td class="n">6,000만원</td></tr>
<tr><td>30억원 이하</td><td class="n">40%</td><td class="n">1억 6,000만원</td></tr>
<tr><td>30억원 초과</td><td class="n">50%</td><td class="n">4억 6,000만원</td></tr>
</tbody></table></div>

<h3>미리 증여해도 10년은 합산됩니다</h3>
<p>상속을 앞두고 재산을 미리 넘기는 경우가 많은데,
<strong>상속개시일로부터 10년 이내에 상속인에게 증여한 재산은 상속재산에 합산</strong>됩니다.
상속인이 아닌 사람에게 증여한 것은 5년입니다.</p>
<p>절세를 위해 사전증여를 활용하려면 <strong>10년 이상 앞서</strong> 계획해야 의미가 있습니다.
<a href="../jeungyeo/">증여세 계산기</a>와 함께 비교해 보세요.</p>

<h3>기한은 6개월입니다</h3>
<p>상속개시일(사망일)이 속한 달의 말일부터 <strong>6개월 이내</strong>에 신고·납부해야 합니다.
기한 내 신고하면 산출세액의 3%를 깎아줍니다.
놓치면 무신고가산세와 납부지연가산세가 붙습니다.</p>

<h3>돈이 없으면 나눠 낼 수 있습니다</h3>
<p>부동산이 대부분이라 현금이 없는 경우가 흔합니다.
<strong>연부연납</strong>으로 최대 10년(가업상속은 더 길게) 나눠 낼 수 있고,
요건을 갖추면 <strong>물납</strong>(부동산이나 유가증권으로 납부)도 가능합니다.
다만 연부연납에는 이자 성격의 가산금이 붙습니다.</p>

<h3>부동산 평가가 결과를 좌우합니다</h3>
<p>상속재산은 <strong>상속개시일 현재의 시가</strong>로 평가합니다.
시가가 불분명하면 기준시가를 쓰는데, 최근에는 감정평가를 통한 시가 산정이 강조되는 추세입니다.
평가액이 달라지면 세금이 크게 바뀌므로 이 부분은 반드시 전문가 상담이 필요합니다.</p>
""",
    faq=[
        (u"배우자와 자녀가 있으면 얼마까지 세금이 없나요?",
         u"일괄공제 5억과 배우자공제 최소 5억을 합쳐 10억원까지는 상속세가 없는 것이 일반적입니다. "
         u"재산 구성과 상속 방식에 따라 달라질 수 있습니다."),
        (u"미리 증여하면 상속세를 피할 수 있나요?",
         u"상속인에게 10년 이내(상속인 외 5년) 증여한 재산은 상속재산에 합산됩니다. "
         u"10년 이상 앞서 계획해야 의미가 있습니다."),
        (u"세금 낼 현금이 없으면 어떻게 하나요?",
         u"연부연납으로 최대 10년 분할 납부하거나 요건을 갖추면 물납할 수 있습니다. "
         u"연부연납에는 가산금이 붙습니다."),
        (u"부동산은 어떤 금액으로 계산하나요?",
         u"상속개시일 현재 시가가 원칙입니다. 평가 방법에 따라 세액이 크게 달라지므로 "
         u"세무 전문가 상담을 권합니다."),
    ],
)

# ───────────────────────── 시간외수당 ─────────────────────────
add(
    slug="overtime", name=u"시간외수당 계산기", group=u"급여·노무",
    title=u"연장·야간·휴일근로 수당 계산기",
    desc=u"통상시급으로 연장근로·야간근로·휴일근로 가산수당을 계산합니다. 5인 미만 사업장 여부를 반영합니다.",
    kw=u"연장 1.5배·야간 가산·휴일근로 수당",
    spec=u"""
Calc.mount({
  id:"overtime",
  formTitle:"근로 정보",
  fields:[
    {k:"mode", label:"시급 입력", type:"seg", options:[
      {value:"hour", label:"시급 직접"}, {value:"month", label:"월급에서 환산"}]},
    {k:"wage", label:"통상시급", suffix:"원", value:15000, step:100, min:0},
    {k:"monthly", label:"월 통상임금", sub:"월급에서 환산할 때", suffix:"원", value:3000000, step:100000, min:0},
    {k:"monthHours", label:"월 소정근로시간", sub:"주40시간이면 209", suffix:"시간", value:209, step:1, min:1},
    {k:"ot", label:"연장근로", sub:"주 40시간 초과", suffix:"시간", value:10, step:0.5, min:0},
    {k:"night", label:"야간근로", sub:"22시~06시", suffix:"시간", value:0, step:0.5, min:0},
    {k:"holiday", label:"휴일근로", sub:"8시간 이내", suffix:"시간", value:0, step:0.5, min:0},
    {k:"holidayOver", label:"휴일 8시간 초과분", suffix:"시간", value:0, step:0.5, min:0},
    {k:"small", label:"상시 근로자", type:"seg", options:[
      {value:"0", label:"5인 이상"}, {value:"1", label:"5인 미만"}]}
  ],
  compute:function(v,F){
    var w = v.mode==="month"
      ? (v.monthly||0)/Math.max(1,v.monthHours||1)
      : (v.wage||0);
    var small = v.small==1;

    /* 5인 미만 사업장은 가산수당 의무가 없다. 실근로시간분만 지급. */
    var otM   = small ? 1.0 : 1.5;
    var nightM= small ? 0.0 : 0.5;
    var hdM   = small ? 1.0 : 1.5;
    var hdoM  = small ? 1.0 : 2.0;

    var ot=(v.ot||0)*w*otM;
    var night=(v.night||0)*w*nightM;
    var hd=(v.holiday||0)*w*hdM;
    var hdo=(v.holidayOver||0)*w*hdoM;
    var total=ot+night+hd+hdo;
    var hours=(v.ot||0)+(v.holiday||0)+(v.holidayOver||0);

    return {
      hero:{k:"시간외수당 합계", v:F.kor(total), sub:F.won(total), cls:"up"},
      stats:[
        {k:"통상시급", v:F.won(w), sub: v.mode==="month" ? "월급 ÷ "+F.num(v.monthHours)+"시간" : "직접 입력"},
        {k:"가산 대상 시간", v:F.num(hours,1)+"시간", sub:"야간 "+F.num(v.night,1)+"시간 별도"},
        {k:"시간당 평균", v: hours>0 ? F.won(total/hours) : "—"}
      ],
      hint: small ? "5인 미만 — 가산수당 의무 없음" : "5인 이상 — 가산 적용",
      cols:["구분","시간","배율","금액"],
      rows:[
        ["연장근로", F.num(v.ot,1)+"시간", otM+"배", F.won(ot)],
        ["야간근로 가산", F.num(v.night,1)+"시간", "+"+nightM+"배", F.won(night)],
        ["휴일근로 (8h 이내)", F.num(v.holiday,1)+"시간", hdM+"배", F.won(hd)],
        ["휴일근로 (8h 초과)", F.num(v.holidayOver,1)+"시간", hdoM+"배", F.won(hdo)],
        ["합계", "", "", F.won(total)]
      ],
      extra:"<div class='note'>"+
        (small
          ? "<b>상시 근로자 5인 미만 사업장은 연장·야간·휴일근로 가산수당 의무가 없습니다.</b> "+
            "실제 일한 시간만큼의 임금(1배)만 지급하면 됩니다. 다만 최저임금과 주휴수당은 적용됩니다."
          : "야간근로 가산(0.5배)은 <b>연장근로와 중복 적용</b>됩니다. "+
            "밤 10시 이후 연장근무를 하면 연장 1.5배 + 야간 0.5배 = <b>2배</b>가 됩니다. "+
            "야간근로 칸에는 그 시간대에 일한 시간을 따로 넣으세요.")+
        "</div>"
    };
  }
});""",
    guide=u"""
<h3>가산율</h3>
<div class="tablewrap"><table>
<thead><tr><th>구분</th><th>기준</th><th>지급 배율</th></tr></thead>
<tbody>
<tr><td>연장근로</td><td>1일 8시간 · 주 40시간 초과</td><td class="n">1.5배</td></tr>
<tr><td>야간근로</td><td>밤 10시 ~ 아침 6시</td><td class="n">+0.5배 (가산)</td></tr>
<tr><td>휴일근로</td><td>8시간 이내</td><td class="n">1.5배</td></tr>
<tr><td>휴일근로</td><td>8시간 초과</td><td class="n">2배</td></tr>
</tbody></table></div>

<h3>야간근로는 중복해서 붙습니다</h3>
<p>야간근로 가산은 <strong>다른 가산과 함께 적용</strong>됩니다.</p>
<ul>
<li>밤 10시 이후 <strong>연장근무</strong> → 1.5배 + 0.5배 = <strong>2배</strong></li>
<li>밤 10시 이후 <strong>휴일근무</strong> → 1.5배 + 0.5배 = <strong>2배</strong></li>
<li>휴일 8시간 초과 + 야간 → 2배 + 0.5배 = <strong>2.5배</strong></li>
</ul>
<p>계산기에서는 야간 시간을 따로 넣으면 가산분(0.5배)만 더해집니다.</p>

<h3>5인 미만 사업장은 가산수당 의무가 없습니다</h3>
<p>상시 근로자 5인 미만 사업장에는 근로기준법의 가산수당 규정이 적용되지 않습니다.
연장·야간·휴일에 일해도 <strong>실제 일한 시간만큼의 임금(1배)</strong>만 지급하면 됩니다.</p>
<p>다만 <strong>최저임금과 주휴수당은 적용</strong>됩니다.
5인 미만이라고 모든 규정에서 자유로운 것은 아닙니다.</p>

<h3>통상시급을 정확히 잡아야 합니다</h3>
<p>가산수당의 기준은 <strong>통상임금</strong>입니다. 월급제라면 이렇게 환산합니다.</p>
<p><strong>통상시급 = 월 통상임금 ÷ 월 소정근로시간</strong></p>
<p>주 40시간 근로자의 월 소정근로시간은 보통 <strong>209시간</strong>입니다.
(40시간 + 주휴 8시간) × 4.345주 ≒ 209시간이기 때문입니다.</p>
<p>통상임금에는 기본급과 정기적·일률적으로 지급되는 수당이 들어갑니다.
성과급처럼 실적에 따라 달라지는 것은 제외되는 것이 원칙이나
판례가 계속 나오는 영역이라 다툼이 잦습니다.</p>

<h3>주 52시간</h3>
<p>법정근로시간은 주 40시간이고, 연장근로는 <strong>주 12시간까지</strong> 허용됩니다.
합쳐서 주 52시간이 상한입니다. 이를 넘기는 것은 당사자가 합의해도 위법입니다.</p>

<h3>포괄임금제라면</h3>
<p>연장·야간수당을 미리 급여에 포함해 지급하는 방식입니다.
다만 <strong>실제 근로시간에 따른 법정 수당보다 적으면 차액을 청구할 수 있습니다.</strong>
계산기로 실제 근로시간 기준 수당을 계산해 급여명세서와 비교해 보세요.</p>
""",
    faq=[
        (u"밤 11시까지 야근하면 얼마를 받나요?",
         u"8시간을 넘긴 시간은 연장근로 1.5배이고, 밤 10시 이후 시간에는 야간 가산 0.5배가 "
         u"더해져 2배가 됩니다. 야간 칸에 10시 이후 시간을 넣으면 계산됩니다."),
        (u"5인 미만인데 야근수당을 못 받나요?",
         u"5인 미만 사업장은 가산수당 의무가 없어 실제 일한 시간만큼의 임금만 받습니다. "
         u"다만 최저임금과 주휴수당은 적용됩니다."),
        (u"월 소정근로시간 209는 어디서 나온 숫자인가요?",
         u"주 40시간에 주휴 8시간을 더한 48시간에 월 평균 주수 4.345를 곱한 값입니다."),
        (u"포괄임금제인데 따로 청구할 수 있나요?",
         u"실제 근로시간 기준 법정 수당이 지급액보다 많으면 차액을 청구할 수 있습니다. "
         u"근로시간 기록을 남겨두시는 것이 중요합니다."),
    ],
)

# ───────────────────────── 육아휴직 급여 ─────────────────────────
add(
    slug="yuka", name=u"육아휴직 급여 계산기", group=u"급여·노무",
    title=u"육아휴직 급여 계산기 | 기간별 지급액과 총액",
    desc=u"통상임금과 휴직 기간으로 육아휴직 급여를 계산합니다. 기간별 상한액과 하한액을 반영합니다.",
    kw=u"통상임금 기준 육아휴직 급여 월별·총액",
    spec=u"""
Calc.mount({
  id:"yuka",
  formTitle:"휴직 정보",
  sideNote:"지급률과 상한액은 제도 개편으로 자주 바뀝니다. 고용보험 홈페이지에서 당해 연도 기준을 확인해 값을 고쳐 쓰세요.",
  fields:[
    {k:"wage", label:"월 통상임금", suffix:"원", value:3500000, step:100000, min:0},
    {k:"months", label:"휴직 기간", suffix:"개월", value:12, step:1, min:1},
    {k:"cap1", label:"1~3개월 상한", suffix:"원", value:2500000, step:100000, min:0},
    {k:"cap2", label:"4~6개월 상한", suffix:"원", value:2000000, step:100000, min:0},
    {k:"cap3", label:"7개월~ 상한", suffix:"원", value:1600000, step:100000, min:0},
    {k:"rate3", label:"7개월~ 지급률", sub:"1~6개월은 100%", suffix:"%", value:80, step:5, min:0},
    {k:"floor", label:"하한액", suffix:"원", value:700000, step:50000, min:0}
  ],
  compute:function(v,F){
    var w=v.wage||0, n=Math.max(1,Math.round(v.months||1));
    var floor=v.floor||0;
    var rows=[], total=0;

    for(var m=1;m<=n;m++){
      var cap, rate;
      if(m<=3){ cap=v.cap1||0; rate=1.0; }
      else if(m<=6){ cap=v.cap2||0; rate=1.0; }
      else { cap=v.cap3||0; rate=(v.rate3||0)/100; }
      var raw=w*rate;
      var pay=Math.max(floor, Math.min(cap, raw));
      total+=pay;
      var note = raw>cap ? "상한" : (raw<floor ? "하한" : "통상임금 "+(rate*100)+"%");
      if(rows.length<24) rows.push([m+"개월차", F.won(pay), note]);
    }

    var first=rows.length? rows[0][1] : "—";
    return {
      hero:{k:"총 수령액", v:F.kor(total), sub:F.won(total), cls:"up"},
      stats:[
        {k:"1개월차", v:first},
        {k:"월 평균", v:F.won(total/n)},
        {k:"휴직 기간", v:F.num(n)+"개월"}
      ],
      hint:"통상임금 "+F.kor(w),
      cols:["회차","지급액","적용"],
      rows:rows,
      tableHint: n>24 ? "앞 24개월만" : F.num(n)+"개월",
      extra:"<div class='note'>육아휴직 급여는 <b>고용보험</b>에서 지급합니다. "+
        "회사가 주는 것이 아니라 고용센터에 신청해 받습니다. "+
        "휴직 시작 후 1개월이 지난 시점부터 매월 신청할 수 있고, "+
        "휴직 종료 후 <b>12개월 이내</b>에 신청해야 합니다.<br><br>"+
        "지급 대상은 <b>고용보험 피보험 단위기간 180일 이상</b>이고 "+
        "만 8세 이하 또는 초등학교 2학년 이하 자녀를 양육하는 근로자입니다.<br><br>"+
        "<b>지급률과 상한액은 제도 개편으로 자주 바뀝니다.</b> 부모가 함께 쓰거나 "+
        "한부모인 경우 더 유리한 특례가 적용될 수 있으니 고용보험 홈페이지에서 확인하세요.</div>"
    };
  }
});""",
    guide=u"""
<h3>회사가 아니라 고용보험에서 나옵니다</h3>
<p>육아휴직 급여는 <strong>고용보험에서 지급</strong>합니다.
회사는 휴직을 허용할 의무가 있지만 급여를 줄 의무는 없습니다.
근로자가 고용센터에 직접 신청해서 받습니다.</p>

<h3>기간에 따라 금액이 달라집니다</h3>
<p>초반에 많이 주고 뒤로 갈수록 줄어드는 구조입니다.
통상임금에 지급률을 곱하되 <strong>상한액</strong>을 넘지 못하고,
<strong>하한액</strong> 아래로도 내려가지 않습니다.</p>
<p>통상임금이 상한보다 높으면 상한액을 받습니다.
월 통상임금 350만원이고 1~3개월 상한이 250만원이면 250만원을 받습니다.</p>

<h3>지급률과 상한은 자주 바뀝니다</h3>
<p>육아휴직 급여는 저출산 대책의 핵심이라 <strong>제도 개편이 잦습니다.</strong>
지급률, 상한액, 사후지급금 유무가 해마다 달라져 왔습니다.</p>
<p>그래서 이 계산기는 <strong>모든 금액을 입력 항목으로 열어두었습니다.</strong>
고용보험 홈페이지에서 당해 연도 기준을 확인해 넣으시면 정확한 금액이 나옵니다.
기본값은 참고용입니다.</p>

<h3>신청 조건</h3>
<ul>
<li>고용보험 <strong>피보험 단위기간 180일 이상</strong></li>
<li>만 8세 이하 또는 초등학교 2학년 이하 자녀 양육</li>
<li>육아휴직을 <strong>30일 이상</strong> 사용</li>
</ul>

<h3>신청 시기를 놓치지 마세요</h3>
<p>휴직 시작 후 <strong>1개월이 지난 시점부터</strong> 매월 신청합니다.
휴직이 끝난 뒤에는 <strong>12개월 이내</strong>에 신청해야 하며,
이 기간이 지나면 받을 수 없습니다.</p>

<h3>부부가 함께 쓰면 유리한 특례가 있습니다</h3>
<p>같은 자녀에 대해 부모가 순차적으로 또는 동시에 휴직하면
더 높은 지급률을 적용하는 특례가 운영되어 왔습니다.
한부모 근로자에게도 별도 기준이 있습니다.
해당한다면 고용센터에 문의해 보세요.</p>

<h3>휴직 중에도 고용보험료는</h3>
<p>육아휴직 기간에도 건강보험료는 경감된 금액으로 부과되고,
국민연금은 납부예외 신청이 가능합니다.
회사와 공단에 각각 확인하셔야 합니다.</p>

<h3>복직 후 불이익은 위법입니다</h3>
<p>육아휴직을 이유로 해고하거나 불리하게 처우하는 것은 금지되어 있습니다.
휴직 전과 같은 업무 또는 같은 수준의 임금을 지급하는 직무로 복귀시켜야 합니다.</p>
""",
    faq=[
        (u"상한액과 지급률이 기본값과 다릅니다.",
         u"제도 개편이 잦아 해마다 바뀝니다. 모든 금액을 입력 항목으로 열어두었으니 "
         u"고용보험 홈페이지에서 당해 연도 기준을 확인해 넣으세요."),
        (u"회사가 급여를 안 준다고 합니다.",
         u"육아휴직 급여는 고용보험에서 지급합니다. 회사가 주는 것이 아니라 "
         u"근로자가 고용센터에 직접 신청합니다."),
        (u"통상임금이 상한보다 높으면요?",
         u"상한액까지만 받습니다. 통상임금 350만원인데 상한이 250만원이면 250만원입니다."),
        (u"휴직이 끝났는데 신청을 안 했습니다.",
         u"휴직 종료 후 12개월 이내에 신청해야 합니다. 서둘러 고용센터에 문의하세요."),
        (u"부부가 같이 쓰면 더 받나요?",
         u"같은 자녀에 대해 부모가 함께 사용하는 경우 지급률을 높여주는 특례가 운영되어 왔습니다. "
         u"적용 요건은 고용센터에서 확인하세요."),
    ],
)

# ───────────────────────── 전기요금 ─────────────────────────
add(
    slug="jeongi", name=u"전기요금 계산기", group=u"부동산·생활",
    title=u"전기요금 계산기 | 주택용 누진제 단계별 요금 계산",
    desc=u"사용량(kWh)으로 주택용 전기요금을 계산합니다. 누진 3단계, 기후환경요금, 부가세, 전력기반기금을 모두 반영합니다.",
    kw=u"누진 3단계·기후환경요금·부가세 포함 실제 청구액",
    spec=u"""
Calc.mount({
  id:"jeongi",
  formTitle:"사용 정보",
  sideNote:"단가는 한국전력 요금표가 개정되면 바뀝니다. 고지서와 다르면 아래 단가 항목을 고쳐 쓰세요.",
  fields:[
    {k:"kwh", label:"사용량", suffix:"kWh", value:350, step:10, min:0},
    {k:"type", label:"주택용", type:"seg", options:[
      {value:"low", label:"저압"}, {value:"high", label:"고압"}]},
    {k:"season", label:"계절", type:"seg", options:[
      {value:"normal", label:"평상시"}, {value:"summer", label:"여름 (7~8월)"}]},
    {k:"climate", label:"기후환경요금", suffix:"원/kWh", value:9.0, step:0.1, min:0},
    {k:"fuel", label:"연료비조정액", sub:"분기마다 바뀜, 음수 가능", suffix:"원/kWh", value:5.0, step:0.1},
    {k:"family", label:"복지 할인", sub:"대가족·출산 등, 없으면 0", suffix:"원", value:0, step:1000, min:0}
  ],
  compute:function(v,F){
    var kwh=Math.max(0, v.kwh||0);
    var low = v.type!=="high";
    var summer = v.season==="summer";

    /* 누진 구간. 여름(7~8월)은 1·2단계 상한이 늘어난다. */
    var T1 = summer ? 300 : 200;
    var T2 = summer ? 450 : 400;

    /* 기본요금 (구간별 정액) */
    var baseTable = low ? [910, 1600, 7300] : [730, 1260, 6060];
    var tier = kwh<=T1 ? 0 : kwh<=T2 ? 1 : 2;
    var base = baseTable[tier];

    /* 전력량요금 단가 */
    var rate = low ? [120.0, 214.6, 307.3] : [105.0, 174.0, 242.3];

    var seg=[
      Math.min(kwh, T1),
      Math.max(0, Math.min(kwh, T2) - T1),
      Math.max(0, kwh - T2)
    ];
    var energy = seg[0]*rate[0] + seg[1]*rate[1] + seg[2]*rate[2];

    var climate = kwh*(v.climate||0);
    var fuel = kwh*(v.fuel||0);
    var discount = Math.min(v.family||0, base+energy+climate+fuel);

    var supply = base + energy + climate + fuel - discount;   /* 공급가액 */
    var vat = Math.round(supply*0.1);
    var fund = Math.floor(supply*0.037/10)*10;                /* 전력산업기반기금 */
    var total = Math.floor((supply + vat + fund)/10)*10;      /* 10원 미만 절사 */

    var avg = kwh>0 ? total/kwh : 0;

    return {
      hero:{k:"청구 예상액", v:F.kor(total), sub:F.won(total), cls:"down"},
      stats:[
        {k:"전력량요금", v:F.won(energy), sub: tier===2 ? "3단계 적용" : (tier===1 ? "2단계 적용" : "1단계")},
        {k:"기본요금", v:F.won(base)},
        {k:"kWh당 평균", v:F.won(avg), sub:"누진 반영 실단가"}
      ],
      hint:(low?"저압":"고압")+" · "+(summer?"여름 누진완화":"평상시")+" · "+F.num(kwh)+"kWh",
      cols:["단계","사용량","단가","금액"],
      rows:[
        ["1단계 (~"+T1+"kWh)", F.num(seg[0])+"kWh", F.num(rate[0],1)+"원", F.won(seg[0]*rate[0])],
        ["2단계 ("+(T1+1)+"~"+T2+")", F.num(seg[1])+"kWh", F.num(rate[1],1)+"원", F.won(seg[1]*rate[1])],
        ["3단계 ("+T2+" 초과)", F.num(seg[2])+"kWh", F.num(rate[2],1)+"원", F.won(seg[2]*rate[2])],
        ["기본요금", "—", "—", F.won(base)],
        ["기후환경요금", F.num(kwh)+"kWh", F.num(v.climate,1)+"원", F.won(climate)],
        ["연료비조정액", F.num(kwh)+"kWh", F.num(v.fuel,1)+"원", F.won(fuel)],
        ["복지 할인", "—", "—", discount? "− "+F.won(discount) : "—"],
        ["공급가액", "—", "—", F.won(supply)],
        ["부가가치세 10%", "—", "—", F.won(vat)],
        ["전력기반기금 3.7%", "—", "—", F.won(fund)],
        ["합계", "—", "—", F.won(total)]
      ],
      tableHint:"10원 미만 절사",
      extra:"<div class='note'>"+
        (tier===2
          ? "<b>3단계 구간에 들어갔습니다.</b> "+F.num(seg[2])+"kWh 가 최고 단가 "+F.num(rate[2],1)+"원으로 계산됩니다. "+
            "1단계의 <b>"+ (rate[2]/rate[0]).toFixed(1) +"배</b>입니다. "+F.num(T2)+"kWh 아래로 줄이면 부담이 크게 줄어듭니다."
          : tier===1
            ? "2단계 구간입니다. "+F.num(T2)+"kWh 를 넘기면 단가가 "+F.num(rate[2],1)+"원으로 뜁니다. "+
              "남은 여유는 <b>"+F.num(T2-kwh)+"kWh</b> 입니다."
            : "1단계 구간이라 가장 낮은 단가가 적용됩니다.")+
        (summer ? "<br><br>여름철(7~8월)에는 누진 구간이 <b>300/450kWh</b> 로 완화됩니다." : "")+
        "</div>"
    };
  }
});""",
    guide=u"""
<h3>전기요금은 곱셈이 아닙니다</h3>
<p>350kWh를 썼다고 <em>350 × 단가</em>로 계산하면 틀립니다.
주택용 전기는 <strong>누진제</strong>라 사용량 구간마다 단가가 다릅니다.
많이 쓸수록 뒤쪽 사용량에 더 비싼 단가가 붙습니다.</p>

<h3>누진 3단계</h3>
<div class="tablewrap"><table>
<thead><tr><th>단계</th><th>평상시</th><th>여름 (7~8월)</th><th>저압 단가</th></tr></thead>
<tbody>
<tr><td>1단계</td><td>~200kWh</td><td>~300kWh</td><td class="n">120.0원</td></tr>
<tr><td>2단계</td><td>201~400kWh</td><td>301~450kWh</td><td class="n">214.6원</td></tr>
<tr><td>3단계</td><td>400kWh 초과</td><td>450kWh 초과</td><td class="n">307.3원</td></tr>
</tbody></table></div>
<p>3단계 단가는 1단계의 <strong>2.6배</strong>입니다.
400kWh에서 401kWh로 1kWh만 넘어가도 그 1kWh는 307원이 됩니다.</p>

<h3>여름에는 구간이 늘어납니다</h3>
<p>에어컨 사용이 몰리는 <strong>7~8월</strong>에는 1단계가 300kWh, 2단계가 450kWh로 완화됩니다.
같은 400kWh라도 여름이면 2단계 안에 들어가 요금이 줄어듭니다.
계절 항목을 바꿔가며 비교해 보세요.</p>

<h3>고지서에 붙는 것들</h3>
<p>전력량요금만 내는 게 아닙니다.</p>
<ul>
<li><strong>기본요금</strong> — 사용 구간에 따른 정액. 400kWh를 넘으면 7,300원으로 크게 뜁니다.</li>
<li><strong>기후환경요금</strong> — kWh당 부과. 신재생에너지 의무이행 비용 등에 쓰입니다.</li>
<li><strong>연료비조정액</strong> — 분기마다 조정됩니다. 마이너스일 때도 있습니다.</li>
<li><strong>부가가치세</strong> — 공급가액의 10%</li>
<li><strong>전력산업기반기금</strong> — 공급가액의 3.7%</li>
</ul>
<p>부가세와 기금까지 더하면 공급가액보다 <strong>13.7%</strong> 더 나옵니다.</p>

<h3>저압과 고압</h3>
<p>단독주택과 소규모 건물은 대체로 <strong>저압</strong>, 아파트처럼 고압으로 받아
단지에서 나눠 쓰는 곳은 <strong>고압</strong>입니다. 고압이 단가가 더 쌉니다.
고지서나 관리비 명세서에서 확인할 수 있습니다.</p>

<h3>사용량을 줄이면 얼마나 아끼나</h3>
<p>누진제 때문에 <strong>줄이는 효과가 구간마다 다릅니다.</strong>
3단계에 있는 사람이 10kWh를 줄이면 약 3,000원이 줄지만,
1단계에 있는 사람이 같은 10kWh를 줄이면 1,200원입니다.
많이 쓰는 집일수록 절약 효과가 큽니다.</p>
<p>계산기에서 사용량을 바꿔가며 구간 경계 근처의 차이를 확인해 보세요.</p>

<h3>단가는 바뀝니다</h3>
<p>전기요금 단가는 한국전력 요금표 개정으로 바뀝니다.
기후환경요금과 연료비조정액은 특히 자주 조정됩니다.
계산기의 해당 항목을 <strong>입력값으로 열어두었으니</strong> 고지서와 다르면 직접 고쳐 쓰세요.</p>
""",
    faq=[
        (u"고지서 금액과 조금 다릅니다.",
         u"단가 개정, 복지 할인, 검침일 기준 일할 계산, 미납·연체료 등이 반영되면 달라집니다. "
         u"기후환경요금과 연료비조정액을 고지서 값으로 맞추면 가까워집니다."),
        (u"저압인지 고압인지 어떻게 아나요?",
         u"고지서나 관리비 명세서에 표시됩니다. 아파트는 대체로 고압, 단독주택은 저압인 경우가 많습니다."),
        (u"여름 누진 완화는 언제 적용되나요?",
         u"7월과 8월 사용분에 적용됩니다. 검침일 기준이라 고지서 대상 기간을 확인하세요."),
        (u"400kWh를 조금 넘겼는데 요금이 많이 올랐습니다.",
         u"3단계 단가가 1단계의 2.6배이고, 기본요금도 7,300원으로 뜁니다. "
         u"구간 경계에서 요금이 계단처럼 오르는 구조입니다."),
        (u"전기요금 누진제는 왜 있나요?",
         u"과다 사용을 억제하고 저소비 가구의 부담을 낮추기 위한 구조입니다. "
         u"이 계산기는 제도의 타당성이 아니라 현행 요금표에 따른 금액만 계산합니다."),
    ],
)
