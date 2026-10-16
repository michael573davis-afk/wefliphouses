"""Daily rate scraper. Never invents numbers: on failure keeps last value, marks it unverified."""
import json, re, datetime, pathlib, requests
from bs4 import BeautifulSoup
ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG, OUT = ROOT/"data/lenders.json", ROOT/"data/rates.json"
STALE_DAYS = 30
def parse_date(s):
    for f in ("%B %Y","%b %Y","%B %d, %Y","%b %d, %Y","%b %d %Y","%B %d %Y","%b. %d, %Y"):
        try: return datetime.datetime.strptime(s.strip(), f).date()
        except ValueError: pass
def main():
    now = datetime.datetime.now(datetime.timezone.utc)
    old = {r["id"]: r for r in json.loads(OUT.read_text())["lenders"]} if OUT.exists() else {}
    out = []
    for l in json.loads(CFG.read_text()):
        r = {k: l.get(k) for k in ("id","name","product","url","notes")}
        r.update(status="not_verified", floor=None, max=None, last_checked=None, last_success=None, page_date=None, stale=False, error=None)
        if l.get("url"):
            r["last_checked"] = now.isoformat(timespec="seconds")
            try:
                h = requests.get(l["url"], timeout=25, headers={"User-Agent":"Mozilla/5.0 (WeFlipHousesRateBot)"}); h.raise_for_status()
                t = re.sub(r"\s+"," ",BeautifulSoup(h.text,"html.parser").get_text(" "))
                m = re.search(l["pattern"], t)
                if not m: raise ValueError("rate pattern not found on page")
                g = [float(x) for x in m.groups() if x]
                r["floor"], r["max"] = g[0], (g[-1] if len(g) > 1 else None)
                r["snippet"] = t[max(0,m.start()-60):m.end()+40]
                r["status"], r["last_success"] = "verified", r["last_checked"]
                if l.get("date_pattern") and (d := re.search(l["date_pattern"], t)):
                    pd = parse_date(d.group(1))
                    if pd:
                        r["page_date"] = pd.isoformat()
                        r["stale"] = (now.date() - pd).days > STALE_DAYS
            except Exception as e:
                r["error"] = str(e)[:200]
                p = old.get(l["id"])
                if p and p.get("floor") is not None:   # keep last known value, flagged
                    for k in ("floor","max","last_success","page_date","snippet"): r[k] = p.get(k)
                    r["status"] = "scrape_failed"
                if r["last_success"]:
                    r["stale"] = r["stale"] or (now - datetime.datetime.fromisoformat(r["last_success"])).days > STALE_DAYS
        out.append(r)
    data = {"generated": now.isoformat(timespec="seconds"), "stale_days": STALE_DAYS, "lenders": out}
    OUT.write_text(json.dumps(data, indent=1))
    (ROOT/"data/rates.js").write_text("window.RATES=" + json.dumps(data) + ";")
    for r in out: print(f'{r["name"]:22} {r["status"]:13} {r["floor"]} {r["max"]} stale={r["stale"]} {r["error"] or ""}')
if __name__ == "__main__": main()
