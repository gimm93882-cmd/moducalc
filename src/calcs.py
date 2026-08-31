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
