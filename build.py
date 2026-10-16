import json, pathlib
R = pathlib.Path(__file__).parent
NAV = [("Rates","rates.html"),("Calculator","calculator.html"),("Lenders","lenders/index.html"),("Newsletter","newsletter/index.html"),("Advertise","advertise.html")]
SIGNUP = '''<form class="signup" onsubmit="event.preventDefault();this.innerHTML='<p><b>Thanks!</b> Signup goes live at launch (newsletter tool not connected yet).</p>'">
<input type="email" required placeholder="you@email.com" aria-label="Email"><button class="btn">Get the Friday email</button></form>'''
def page(path, title, body, desc="Fix-and-flip loan rates, flip calculators, and a weekly newsletter for house flippers."):
    depth = path.count("/"); pre = "../"*depth
    nav = "".join(f'<a href="{pre}{h}">{n}</a>' for n,h in NAV)
    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | We Flip Houses</title><meta name="description" content="{desc}"><link rel="icon" type="image/svg+xml" href="{pre}favicon.svg"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;800;900&display=swap"><link rel="stylesheet" href="{pre}assets/style.css"></head><body>
<header><div class="wrap"><a class="logo" href="{pre}index.html"><img src="{pre}assets/logo.svg" alt="We Flip Houses" width="248" height="48"></a><nav>{nav}</nav></div></header>
{body.replace("{pre}",pre).replace("{SIGNUP}",SIGNUP)}
<footer><div class="wrap">© 2026 We Flip Houses LLC · <a href="{pre}methodology.html">Methodology</a> · <a href="{pre}advertise.html">Advertise</a><br>Rates are lenders' published figures, not quotes or offers. We are not a lender or broker. Verify every term with the lender.</div></footer></body></html>'''
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
<p class="muted">Rate moves, one lender spotlight, and one real deal broken down line by line. Free, and you can unsubscribe anytime.</p>{{SIGNUP}}</div></section>''')

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
</script>''')

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
<div class="card" style="margin-top:20px"><h3>Get the media kit</h3><p>Pricing and audience numbers available at launch. Contact: <i>(email coming soon)</i></p></div></div></section>''')

page("newsletter/index.html","The Friday Flip newsletter archive",'''<section><div class="wrap" style="max-width:760px"><h1>The Friday Flip: archive</h1><p class="muted">Every issue covers rate moves, one lender spotlight, and one deal broken down.</p>
<div class="card"><h3>Issue #1: coming soon</h3><p class="muted">The first issue goes out after launch. Sign up so you don't miss it.</p>{SIGNUP}</div></div></section>''')
print("built")
