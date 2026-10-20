"""Собирает CSV (data/) и JSON для сайта (docs/data/sbp.json) из dataset.py."""
import csv
import json
from pathlib import Path

import dataset as ds
from payment_cost import table

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
WEB = ROOT / "docs" / "data"
DATA.mkdir(exist_ok=True)
WEB.mkdir(parents=True, exist_ok=True)


def write(name, header, rows):
    with open(DATA / name, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


write("sbp_annual.csv", ["year", "operations_bn", "volume_trn_rub", "merchants_mln", "source", "status"], ds.SBP_ANNUAL)
write("sbp_daily_operations.csv", ["period", "operations_mln_per_day", "source"], ds.SBP_DAILY)
write("sbp_structure_q2_2026.csv", ["type", "share_count_pct", "share_volume_pct", "operations_bn", "volume_trn_rub"], ds.SBP_STRUCTURE_Q2_2026)
write("merchants_quarterly.csv", ["quarter", "merchants_mln", "sme_mln"], ds.MERCHANTS_QUARTERLY)
write("payment_methods_q2_2026.csv", ["method", "share_count_pct"], ds.PAYMENT_METHODS_Q2_2026)
write("transfers_q2_2026.csv", ["channel", "share_count_pct"], ds.TRANSFERS_Q2_2026)
write("avg_check_q2_2026.csv", ["method", "avg_check_rub"], ds.AVG_CHECK_Q2_2026)
write("regions_card_payments_q2_2026.csv", ["district", "card_payments_per_capita_quarter"], ds.REGIONS_CARD_PAYMENTS_Q2_2026)
write("cbr_sbp_bank_tariff_2026.csv", ["amount_upper_rub", "fee_rub"], ds.CBR_SBP_BANK_TARIFF_2026)
write("international.csv", ["system", "country", "operations_bn_month", "population_mln", "period", "source"], ds.INTERNATIONAL)
write("digital_ruble.csv", ["date", "wallets_k", "operations_k", "source"], ds.DIGITAL_RUBLE)
write("unit_economics.csv", ["check_rub", "digital_ruble_2027", "sbp_0_7", "card_1_5_vat", "card_2_5_vat"],
      [(r["check"], r["dr_2027"], r["sbp"], r["card_1_5"], r["card_2_5"]) for r in table()])
write("sources.csv", ["id", "title", "url", "status"], [(k, *v) for k, v in ds.SOURCES.items()])

web = {
    "checked": ds.CHECKED,
    "tariffs": ds.TARIFFS,
    "cbrTariff": ds.CBR_SBP_BANK_TARIFF_2026,
    "annual": [{"year": y, "ops": o, "vol": v, "merchants": m} for y, o, v, m, *_ in ds.SBP_ANNUAL],
    "daily": [{"period": p, "value": v} for p, v, _ in ds.SBP_DAILY],
    "methods": [{"name": n, "share": s} for n, s in ds.PAYMENT_METHODS_Q2_2026],
    "transfers": [{"name": n, "share": s} for n, s in ds.TRANSFERS_Q2_2026],
    "avgCheck": [{"name": n, "value": v} for n, v in ds.AVG_CHECK_Q2_2026],
    "merchants": [{"q": q, "all": a, "sme": s} for q, a, s in ds.MERCHANTS_QUARTERLY],
    "regions": [{"name": n, "value": v} for n, v in ds.REGIONS_CARD_PAYMENTS_Q2_2026],
    "international": [{"system": s, "country": c, "perCapita": round(o * 1000 / p, 1), "period": per}
                      for s, c, o, p, per, _ in ds.INTERNATIONAL],
    "digitalRuble": [{"date": d, "wallets": w, "ops": o} for d, w, o, _ in ds.DIGITAL_RUBLE],
    "drExpectation": ds.DR_CBR_EXPECTATION_YEAR_END_K,
    "fraud": ds.FRAUD,
    "sources": [{"id": k, "title": t, "url": u, "status": s} for k, (t, u, s) in ds.SOURCES.items()],
}
(WEB / "sbp.json").write_text(json.dumps(web, ensure_ascii=False, indent=1), encoding="utf-8")
print("CSV:", len(list(DATA.glob("*.csv"))), "| JSON: docs/data/sbp.json")
