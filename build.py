import hashlib as _h, json, pathlib
R = pathlib.Path(__file__).parent
V=_h.md5(b''.join(open(R/f,'rb').read() for f in ['assets/style.css','assets/logo.svg','assets/logo-light.svg','favicon.svg'])).hexdigest()[:8]
NAV = [("Rates","rates.html"),("Calculator","calculator.html"),("Lenders","lenders/index.html"),("Newsletter","newsletter/index.html"),("Advertise","advertise.html")]
SIGNUP = '''<div class="bh-form"><script async src="https://subscribe-forms.beehiiv.com/v3/loader.js" data-beehiiv-form="dce3dc61-62a8-45aa-924b-3f5930aff887"></script></div>'''

BASE="https://wefliphousesllc.com/"
PAGES=[]
CALC_SCHEMA={"@type":"WebApplication","name":"Flip profit calculator","url":BASE+"calculator.html","applicationCategory":"FinanceApplication","operatingSystem":"Any (web browser)","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"},"description":"Free fix-and-flip profit calculator: purchase, rehab, ARV, loan, holding and selling costs to profit, ROI and 70% rule max offer."}
DESC={
"index.html":"Published fix-and-flip and hard money loan rates checked daily against lenders' own pages, a free flip profit calculator, and a weekly newsletter for house flippers.",
"rates.html":"Today's published fix-and-flip and hard money loan rates from lenders' own pages, with source links, last-checked dates, and stale-page flags.",
"calculator.html":"Free flip profit calculator. Enter purchase, rehab, ARV, loan terms, holding and selling costs to see profit, cash needed, ROI, and your 70% rule max offer.",
"lenders/index.html":"Directory of fix-and-flip and hard money lenders with published rates, products, and links to each lender's own source page.",
"methodology.html":"How We Flip Houses tracks hard money rates: lender-published figures only, daily checks, stale-source flags, and no guessed numbers.",
"advertise.html":"Reach active house flippers with a featured lender listing, newsletter sponsorship, or calculator sponsorship. Flat fees, clearly labeled.",
"newsletter/index.html":"The Friday Flip: a free weekly email with hard money rate moves, one lender spotlight, and one flip deal broken down line by line.",
}
def page(path, title, body, desc="Fix-and-flip loan rates, flip calculators, and a weekly newsletter for house flippers.", schema=None):
    desc = DESC.get(path, desc)
    if path.startswith("lenders/") and path!="lenders/index.html": desc = f"{title.replace(' fix-and-flip rates','')}: published fix-and-flip rate, product notes, source link, and last-checked date, tracked by We Flip Houses."
    url = BASE + ("" if path=="index.html" else path.replace("index.html",""))
    PAGES.append(url)
    full = "We Flip Houses | "+title if path=="index.html" else f"{title} | We Flip Houses"
    sd = [{"@context":"https://schema.org","@type":"WebSite","name":"We Flip Houses","url":BASE}] if path=="index.html" else []
    if schema: sd.append(dict({"@context":"https://schema.org"}, **schema))
    ld = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in sd)
    seo = f'<link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:site_name" content="We Flip Houses"><meta property="og:title" content="{full}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}assets/og.png"><meta name="twitter:card" content="summary_large_image">{ld}'
    depth = path.count("/"); pre = "../"*depth
    nav = "".join(f'<a href="{pre}{h}">{n}</a>' for n,h in NAV)
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{full}</title><meta name="description" content="{desc}">{seo}<link rel="icon" type="image/svg+xml" href="{pre}favicon.svg?v={V}"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;800;900&display=swap"><link rel="stylesheet" href="{pre}assets/style.css?v={V}"></head><body>
<header><div class="wrap"><a class="logo" href="{pre}index.html"><img src="{pre}assets/logo.svg?v={V}" alt="We Flip Houses" width="248" height="48"></a><nav>{nav}</nav></div></header>
{body.replace("{pre}",pre).replace("{SIGNUP}",SIGNUP)}
<footer><div class="wrap"><img class="flogo" src="{pre}assets/logo-light.svg?v={V}" alt="We Flip Houses" width="206" height="40"><br>© 2026 We Flip Houses LLC · <a href="{pre}methodology.html">Methodology</a> · <a href="{pre}advertise.html">Advertise</a><br>Guides: <a href="{pre}hard-money-loan-rates-today.html">Hard money loan rates today</a> · <a href="{pre}fix-and-flip-calculator.html">Fix and flip calculator</a> · <a href="{pre}70-percent-rule-calculator.html">70% rule calculator</a><br>Rates are lenders' published figures, not quotes or offers. We are not a lender or broker. Verify every term with the lender.</div></footer><script type="text/javascript" async src="https://subscribe-forms.beehiiv.com/attribution.js"></script></body></html>'''
    p = R/path; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(html)
data = json.loads((R/"data/rates.json").read_text())
def rate_txt(l):
    if l["floor"] is None: return "Rate not yet verified"
    return f'{l["floor"]:.2f}%' + (f' – {l["max"]:.2f}%' if l["max"] else "+ (starting)")
def status(l):
    if l["status"]=="verified" and l["stale"]: return '<span class="tag warn">Stale source</span>'
    if l["status"]=="verified": return '<span class="tag ok">Verified</span>'
    if l["status"]=="scrape_failed": return '<span class="tag bad">Last check failed</span>'
    return '<span class="tag no">Not yet verified</span>'

page("index.html","Fix-and-flip loan rates & flip tools",f'''
<div class="hero"><div class="wrap"><h1>Know your money before you make the offer.</h1>
<p>Fix-and-flip and hard money rates checked against lenders' own pages every day, a flip profit calculator, and one email every Friday on who's lending and what deals pencil.</p>
<p><a class="btn" href="rates.html">See today's rates</a> &nbsp; <a class="btn alt" href="calculator.html">Run a flip</a></p></div></div>
<section><div class="wrap grid">
<div class="card"><h3>📈 Rate tracker</h3><p class="muted">Published fix-and-flip rates with source links and last-checked dates. Old pages get flagged, and we never fill in guesses.</p><a href="rates.html">Open the tracker →</a></div>
<div class="card"><h3>🧮 Flip profit calculator</h3><p class="muted">Purchase, rehab, ARV, holding, loan and selling costs → profit, ROI and your 70% rule max offer.</p><a href="calculator.html">Run the numbers →</a></div>
<div class="card"><h3>🏦 Lender directory</h3><p class="muted">Short profiles of hard money and fix-and-flip lenders: products, published terms, and where the numbers come from.</p><a href="lenders/index.html">Browse lenders →</a></div>
</div></section>
<section style="background:#fff;border-top:1px solid var(--line);border-bottom:1px solid var(--line)"><div class="wrap"><h2>The Friday Flip email</h2>
<p class="muted">Rate moves, one lender spotlight, and one real deal broken down line by line. Free, and you can unsubscribe anytime.</p>{{SIGNUP}}</div></section>''', schema={"@type":"Organization","name":"We Flip Houses LLC","url":BASE,"logo":BASE+"assets/logo.svg"})

rows = "".join(f'<tr><td><a href="lenders/{l["id"]}.html"><b>{l["name"]}</b></a></td><td>{l["product"]}</td><td><b>{rate_txt(l)}</b></td><td>{status(l)}{"<br><small class=muted>page dated "+l["page_date"]+"</small>" if l["page_date"] else ""}</td><td>{(l["last_checked"] or "—")[:10]}</td><td>{f'<a href="{l["url"]}" rel="nofollow noopener" target="_blank">Source</a>' if l["url"] else "—"}</td></tr>' for l in sorted(data["lenders"], key=lambda x:(x["floor"] is None, x["floor"] or 0)))
page("rates.html","Fix-and-flip & hard money rates today",f'''<section><div class="wrap"><h1>Fix-and-flip & hard money rates</h1>
<p class="muted">Data updated {data["generated"][:10]} (UTC). Starting rates are what lenders advertise for their best borrowers, and most files price higher. A source is flagged <span class="tag warn">Stale source</span> if the page's own date is more than {data["stale_days"]} days old. <a href="methodology.html">How we track rates</a>.</p>
<div class="tbl"><table><thead><tr><th>Lender</th><th>Product</th><th>Published rate</th><th>Status</th><th>Last checked</th><th>Source</th></tr></thead><tbody>{rows}</tbody></table></div>
<div class="card" style="margin-top:22px"><h3>Get rate moves every Friday</h3>{{SIGNUP}}</div></div></section>''')

page("calculator.html","Flip profit calculator",'''<section><div class="wrap"><h1>Flip profit calculator</h1><p class="muted">Everything runs in your browser, and nothing you type is saved or sent.</p>
<div class="calc"><div id="f">
<fieldset><legend>Deal</legend><label>Purchase price ($)<input id="pp" type="number" value="180000"></label><label>Rehab budget ($)<input id="rehab" type="number" value="45000"></label><label>After-repair value, ARV ($)<input id="arv" type="number" value="300000"></label><label>Buying closing costs (%)<input id="bcc" type="number" step="0.1" value="2"></label></fieldset>
<fieldset><legend>Loan</legend><label>Loan covers % of purchase<input id="ltp" type="number" value="90"></label><label>Loan covers % of rehab<input id="ltr" type="number" value="100"></label><label>Interest rate (%/yr, interest-only)<input id="rate" type="number" step="0.01" value="9.99"></label><label>Points (%)<input id="pts" type="number" step="0.1" value="2"></label><label>Lender fees ($)<input id="lfee" type="number" value="1500"></label></fieldset>
<fieldset><legend>Holding</legend><label>Months held<input id="mo" type="number" value="6"></label><label>Taxes + insurance ($/mo)<input id="ti" type="number" value="400"></label><label>Utilities + other ($/mo)<input id="ut" type="number" value="250"></label></fieldset>
<fieldset><legend>Selling</legend><label>Agent commission (%)<input id="comm" type="number" step="0.1" value="5"></label><label>Seller closing costs (%)<input id="scc" type="number" step="0.1" value="1.5"></label></fieldset>
</div><div><div class="card result"><div class="muted">Estimated profit</div><div class="big" id="profit">—</div>
<div class="row"><span>Cash you put in</span><b id="cash"></b></div><div class="row"><span>ROI on cash</span><b id="roi"></b></div><div class="row"><span>Annualized ROI</span><b id="aroi"></b></div><div class="row"><span>Return on total cost</span><b id="roc"></b></div>
<div class="row"><span>Interest paid</span><span id="int"></span></div><div class="row"><span>Points + lender fees</span><span id="fees"></span></div><div class="row"><span>Holding costs</span><span id="hold"></span></div><div class="row"><span>Selling costs</span><span id="sell"></span></div><div class="row"><span>Total project cost</span><span id="tot"></span></div>
<h3 style="margin-bottom:4px">70% rule max offer</h3><div class="big" id="mao" style="font-size:1.6rem"></div><p class="muted" id="maonote" style="margin-top:4px"></p>
<p class="muted" style="font-size:.85rem">Estimate only. It assumes rehab money is drawn at the start and charged interest the whole time. <a href="rates.html">Compare current rates →</a></p></div></div></div></div></section>
<script>
const $=id=>+document.getElementById(id).value||0, set=(id,v)=>document.getElementById(id).textContent=v, usd=v=>(v<0?"-$":"$")+Math.abs(Math.round(v)).toLocaleString(), pct=v=>isFinite(v)?(v*100).toFixed(1)+"%":"—";
function calc(){const pp=$("pp"),rh=$("rehab"),arv=$("arv"),mo=$("mo");
const loan=pp*$("ltp")/100+rh*$("ltr")/100, interest=loan*$("rate")/100/12*mo, fees=loan*$("pts")/100+$("lfee"), buy=pp*$("bcc")/100, hold=($("ti")+$("ut"))*mo, sell=arv*($("comm")+$("scc"))/100;
const total=pp+rh+buy+interest+fees+hold+sell, profit=arv-total, cash=total-sell-loan;
set("profit",usd(profit));document.getElementById("profit").className="big "+(profit>=0?"pos":"neg");
set("cash",usd(cash));set("roi",pct(profit/cash));set("aroi",mo>0?pct(profit/cash*12/mo):"—");set("roc",pct(profit/total));set("int",usd(interest));set("fees",usd(fees));set("hold",usd(hold));set("sell",usd(sell));set("tot",usd(total));
const mao=arv*0.7-rh;set("mao",usd(mao));set("maonote",`ARV × 70% − rehab. Your price is ${pp<=mao?usd(mao-pp)+" under":usd(pp-mao)+" over"} that.`);}
document.querySelectorAll("#f input").forEach(i=>i.addEventListener("input",calc));calc();
</script>''', schema=CALC_SCHEMA)

cards=""
for l in data["lenders"]:
    cards+=f'<div class="card"><h3><a href="{l["id"]}.html">{l["name"]}</a></h3><p>{l["product"]}<br><b>{rate_txt(l)}</b> {status(l)}</p></div>'
    page(f'lenders/{l["id"]}.html',f'{l["name"]} fix-and-flip rates',f'''<section><div class="wrap"><p><a href="index.html">← All lenders</a></p><h1>{l["name"]}</h1>
<div class="grid"><div class="card"><h3>Published rate</h3><div class="big" style="font-size:1.8rem">{rate_txt(l)}</div><p>{status(l)}</p>
<p class="muted">Product: {l["product"]}<br>Last checked: {(l["last_checked"] or "not tracked yet")[:10]}{"<br>Page's own date: "+l["page_date"] if l["page_date"] else ""}</p>
{f'<p><a href="{l["url"]}" rel="nofollow noopener" target="_blank">Lender source page →</a></p>' if l["url"] else ""}</div>
<div class="card"><h3>Notes</h3><p>{l["notes"] or ""}</p>{f'<p class="muted"><small>Source text: “…{l.get("snippet","")}…”</small></p>' if l.get("snippet") else ""}<p class="muted">Rate history chart coming once we've collected a few weeks of checks.</p></div></div>
<p class="muted">Are you {l["name"]}? <a href="../advertise.html">Claim or feature this profile</a>.</p></div></section>''')
page("lenders/index.html","Fix-and-flip lender directory",f'<section><div class="wrap"><h1>Lender directory</h1><p class="muted">Fix-and-flip and hard money lenders we track. Inclusion isn\'t an endorsement.</p><div class="grid">{cards}</div></div></section>')

page("methodology.html","Methodology",f'''<section><div class="wrap" style="max-width:760px"><h1>How we track rates</h1>
<ol><li><b>Only what lenders publish.</b> Every rate comes from the lender's own public page. We link the source and show the exact text we read.</li>
<li><b>Checked daily.</b> A script visits each source once a day and records when it last checked.</li>
<li><b>No guesses, ever.</b> If we can't read a rate, the lender shows "Rate not yet verified." If a check fails, we keep the last value we read and mark it "Last check failed."</li>
<li><b>Stale flags.</b> If a lender's page carries its own date that is more than {data["stale_days"]} days old, we flag it <span class="tag warn">Stale source</span>.</li>
<li><b>Teaser vs. real.</b> "Starting at" rates usually require experience, strong credit, and low leverage. Expect your quote to be higher.</li>
<li><b>Third-party numbers aren't used.</b> Figures from roundups or other lenders' blogs don't count until we confirm them on the lender's own site. Pages labeled illustrative are excluded.</li>
<li><b>Sponsors can't buy rates.</b> Featured placement is labeled and never changes a published number or its order.</li></ol></div></section>''')

page("advertise.html","Advertise with us",'''<section><div class="wrap"><h1>Reach active house flippers</h1><p class="muted" style="max-width:700px">Our readers are investors comparing fix-and-flip and hard money financing right now. Sponsorships are flat-fee and clearly labeled.</p>
<div class="grid"><div class="card"><h3>Featured lender listing</h3><p>Top-of-directory placement, a highlighted row on the rate tracker (labeled "Featured"), and an expanded profile.</p></div>
<div class="card"><h3>Newsletter sponsor</h3><p>One sponsor slot in the Friday Flip email: a logo, 60 words, and a link.</p></div>
<div class="card"><h3>Calculator sponsor</h3><p>A "Get a quote" card beside the flip profit calculator.</p></div></div>
<div class="card" style="margin-top:20px"><h3>Get the media kit</h3><p>Pricing and audience numbers available on request. Contact: <a href="mailto:Michael573davis@gmail.com">Michael573davis@gmail.com</a></p></div></div></section>''')

page("newsletter/index.html","The Friday Flip newsletter archive",'''<section><div class="wrap" style="max-width:760px"><h1>The Friday Flip: archive</h1><p class="muted">Every issue covers rate moves, one lender spotlight, and one deal broken down.</p>
<div class="card"><h3><a href="issue-1.html">The Friday Flip #1: who's lending, and a deal that breaks the 70% rule</a></h3><p class="muted">Oct 16, 2026 · This week's published hard money rates, an example flip run line by line, and a tip on rehab draw interest.</p></div><div class="card" style="margin-top:18px"><h3>Get the next issue</h3>{SIGNUP}</div></div></section>''')

DESC["newsletter/issue-1.html"]="The Friday Flip #1: published hard money rates for Oct 16, 2026, an example fix-and-flip deal broken down line by line, and a tip on rehab draw interest."
page("newsletter/issue-1.html","The Friday Flip #1: who's lending, and a deal that breaks the 70% rule",'<section><div class="wrap" style="max-width:780px"><p><a href="index.html">← Newsletter archive</a></p><h1>The Friday Flip #1</h1><p class="muted">Oct 16, 2026</p>'+(R/"newsletter/issues/issue-1.html.part").read_text()+'<div class="card" style="margin-top:24px"><h3>Get the Friday Flip every week</h3>{SIGNUP}</div></div></section>', schema={"@type":"Article","headline":"The Friday Flip #1: who's lending, and a deal that breaks the 70% rule","datePublished":"2026-10-16","author":{"@type":"Organization","name":"We Flip Houses"},"publisher":{"@type":"Organization","name":"We Flip Houses LLC"}})
# ---- SEO landing pages ----
ver = [l for l in data["lenders"] if l["status"]=="verified" and l["floor"] is not None]
lrows = "".join(f'<tr><td><a href="lenders/{l["id"]}.html">{l["name"]}</a></td><td><b>{rate_txt(l)}</b></td><td>{status(l)}</td><td>{(l["last_checked"] or "")[:10]}</td><td><a href="{l["url"]}" rel="nofollow noopener" target="_blank">Source</a></td></tr>' for l in sorted(ver,key=lambda x:x["floor"]))
lo = min([l["floor"] for l in ver], default=None)
FAQ_RATES=[("What are hard money loan rates today?", f"Among the lenders we could verify on {data['generated'][:10]}, the lowest published starting rate was {lo:.2f}%. Starting rates go to the strongest borrowers; most quotes come in higher." if lo else "We haven't verified any published rates yet today."),
("Why is my quote higher than the advertised rate?","Advertised 'starting at' rates usually assume several completed flips, strong credit, and low leverage. Less experience, higher loan-to-cost, or a weaker property usually means a higher rate or more points."),
("Do points matter as much as the rate?","Often more on a short loan. On a 6-month loan, 1 point costs about as much as 2% of annual interest. Compare total cost, not just the rate.")]
def faq_html(f): return "".join(f"<h3>{q}</h3><p>{a}</p>" for q,a in f)
def faq_schema(f): return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in f]}
DESC["hard-money-loan-rates-today.html"]="Hard money loan rates today, from lenders' own published pages, with source links and dates. Plus what drives your quote: points, leverage, experience, and term."
page("hard-money-loan-rates-today.html","Hard money loan rates today",f'''<section><div class="wrap" style="max-width:860px"><h1>Hard money loan rates today</h1>
<p class="muted">Published rates we verified on lenders' own pages. Data updated {data["generated"][:10]} (UTC). These are advertised figures, not quotes.</p>
<div class="tbl"><table><thead><tr><th>Lender</th><th>Published rate</th><th>Status</th><th>Checked</th><th>Source</th></tr></thead><tbody>{lrows or '<tr><td colspan=5>No verified rates yet.</td></tr>'}</tbody></table></div>
<p><a href="rates.html">See the full tracker, including lenders we haven't verified yet →</a></p>
<h2>What actually sets your rate</h2><ul><li><b>Experience:</b> number of completed flips in the last 2–3 years is usually the biggest lever.</li><li><b>Leverage:</b> loan-to-cost and loan-to-ARV. Borrowing 90% of purchase usually costs more than 80%.</li><li><b>Credit and liquidity:</b> many lenders tier by credit score and cash reserves.</li><li><b>Points and fees:</b> a lower rate with 3 points can cost more than a higher rate with 1 point on a short hold.</li><li><b>Term and draws:</b> ask whether interest is charged on the full rehab budget or only on funds drawn.</li></ul>
<h2>Common questions</h2>{faq_html(FAQ_RATES)}
<p>Plug any of these rates into the <a href="calculator.html">flip profit calculator</a> to see what they do to your profit.</p></div></section>''', schema=faq_schema(FAQ_RATES))

DESC["fix-and-flip-calculator.html"]="How to use a fix-and-flip calculator: every input explained (ARV, rehab, points, holding, selling costs), the formulas behind profit and ROI, and a free calculator."
page("fix-and-flip-calculator.html","Fix and flip calculator: how to run a flip",'''<section><div class="wrap" style="max-width:820px"><h1>Fix and flip calculator</h1>
<p>Our <a href="calculator.html"><b>free flip profit calculator</b></a> runs in your browser. Here's what each input means and how the math works, so you can trust (or challenge) the result.</p>
<p><a class="btn" href="calculator.html">Open the calculator</a></p>
<h2>The inputs</h2><ul><li><b>Purchase price</b> and <b>buying closing costs</b> (title, escrow, recording; often 1–3% of price).</li><li><b>Rehab budget:</b> include a contingency. Overruns are the most common way flips lose money.</li><li><b>ARV (after-repair value):</b> base it on recent comparable sales of renovated homes, not list prices.</li><li><b>Loan:</b> the % of purchase and % of rehab your lender funds, the interest rate, points, and flat fees.</li><li><b>Holding:</b> months from purchase to sale closing, plus monthly taxes, insurance, and utilities.</li><li><b>Selling:</b> agent commission and seller closing costs as a % of sale price.</li></ul>
<h2>The formulas</h2><ul><li>Loan = purchase × loan % of purchase + rehab × loan % of rehab</li><li>Interest = loan × rate ÷ 12 × months (interest-only, full rehab charged from day one, the conservative case)</li><li>Total cost = purchase + rehab + buying costs + interest + points and fees + holding + selling costs</li><li>Profit = ARV − total cost</li><li>Cash in = total cost − selling costs − loan (selling costs come out of the sale proceeds)</li><li>ROI on cash = profit ÷ cash in; annualized = ROI × 12 ÷ months</li></ul>
<h2>Sanity checks before you offer</h2><ul><li>Run it again with ARV 5–10% lower and rehab 15% higher. If profit disappears, the deal is thin.</li><li>Add a month or two to the hold. Permits and slow sales happen.</li><li>Compare with the <a href="70-percent-rule-calculator.html">70% rule</a> as a quick screen.</li></ul>
<p>Need a rate to plug in? See <a href="hard-money-loan-rates-today.html">hard money loan rates today</a>.</p></div></section>''', schema=CALC_SCHEMA)

FAQ70=[("What is the 70% rule in house flipping?","It's a quick screen: your maximum purchase price should be about 70% of the after-repair value (ARV), minus the rehab cost. The 30% left is meant to cover financing, holding, selling costs, and profit."),
("Is the 70% rule still realistic?","It's a rule of thumb. In expensive or competitive markets, investors often go above 70% on cheaper rehabs; in slow markets or on heavy rehabs, many stay below it. Always run a full cost breakdown."),
("Does the 70% rule include closing and holding costs?","Not explicitly. They're assumed to fit inside the remaining 30%, along with profit. That's why a full calculator is the better final check.")]
DESC["70-percent-rule-calculator.html"]="Free 70% rule calculator for house flippers: maximum allowable offer = ARV × 70% − rehab. Adjust the percentage, see the formula, and learn when the rule breaks."
page("70-percent-rule-calculator.html","70% rule calculator (max allowable offer)",f'''<section><div class="wrap" style="max-width:820px"><h1>70% rule calculator</h1>
<p class="muted">Maximum allowable offer (MAO) = ARV × 70% − rehab cost. Runs in your browser; nothing is saved.</p>
<div class="card" id="r70"><label>After-repair value, ARV ($)<input id="a" type="number" value="250000"></label><label>Rehab cost ($)<input id="r" type="number" value="40000"></label><label>Rule percentage (%)<input id="k" type="number" value="70"></label><label>Your asking / offer price ($, optional)<input id="o" type="number" value=""></label>
<div class="muted" style="margin-top:10px">Maximum allowable offer</div><div class="big" id="m">—</div><p id="n" class="muted"></p></div>
<script>const g=i=>+document.getElementById(i).value||0;function f(){{const m=g("a")*g("k")/100-g("r");document.getElementById("m").textContent="$"+Math.round(m).toLocaleString();const o=g("o");document.getElementById("n").textContent=o?(o<=m?"$"+Math.round(m-o).toLocaleString()+" under the max. Now check the full numbers.":"$"+Math.round(o-m).toLocaleString()+" over the max. Make sure the full numbers still work."):"";}}document.querySelectorAll("#r70 input").forEach(i=>i.addEventListener("input",f));f();</script>
<h2>How it works</h2><p>Example: ARV of $250,000 × 70% = $175,000, minus $40,000 rehab = a $135,000 maximum offer. The remaining 30% of ARV ($75,000) has to cover buying and selling costs, loan interest and points, holding costs, and your profit.</p>
<h2>Where the rule breaks</h2><ul><li><b>High-priced markets:</b> 30% of a $700,000 ARV is far more cushion than a typical flip needs, so investors often go higher.</li><li><b>Low-priced homes:</b> fixed costs eat a bigger share, so 65% or lower can be safer.</li><li><b>Expensive financing:</b> high points and long holds use up the 30% faster.</li></ul>
<p>Once a deal passes the screen, run the full <a href="calculator.html">flip profit calculator</a> with real loan terms from <a href="hard-money-loan-rates-today.html">today's published rates</a>.</p>
<h2>Common questions</h2>{faq_html(FAQ70)}</div></section>''', schema={"@graph":[dict(CALC_SCHEMA,name="70% rule calculator",url=BASE+"70-percent-rule-calculator.html",description=DESC["70-percent-rule-calculator.html"]),faq_schema(FAQ70)]})

today = data["generated"][:10]
(R/"sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+"".join(f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in PAGES)+"</urlset>\n")
(R/"robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")

print("built")
