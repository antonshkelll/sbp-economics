"""Юнит-экономика платежа: сколько продавец платит за приём одного чека.

Формула:  стоимость = min(чек × ставка, потолок) × (1 + НДС, если он не вычитается)

Пример:
    python analysis/payment_cost.py --check 1700
    python analysis/payment_cost.py --turnover 1000000 --shift 30
"""
import argparse
from dataclasses import dataclass

from dataset import TARIFFS, CBR_SBP_BANK_TARIFF_2026


@dataclass
class Method:
    name: str
    rate_pct: float          # комиссия продавца, % от чека
    vat_pct: float = 0.0     # НДС на комиссию, %
    cap_rub: float | None = None


def methods(card_rate=TARIFFS["card_default"], sbp_rate=TARIFFS["sbp_general"], year=2027, vat_deductible=False):
    vat = 0.0 if vat_deductible else TARIFFS["vat_acquiring"]
    dr_rate = TARIFFS["dr_2026"] if year <= 2026 else TARIFFS["dr_2027"]
    return {
        "card": Method("Карта (эквайринг)", card_rate, vat),
        "sbp": Method("СБП", sbp_rate, 0.0, TARIFFS["sbp_cap_rub"]),   # допущение: без НДС
        "dr": Method(f"Цифровой рубль ({year})", dr_rate, 0.0, TARIFFS["dr_cap_rub"]),
    }


def cost(check: float, m: Method) -> float:
    fee = check * m.rate_pct / 100
    if m.cap_rub is not None:
        fee = min(fee, m.cap_rub)
    return round(fee * (1 + m.vat_pct / 100), 2)


def cbr_bank_tariff(check: float) -> float:
    """Тариф Банка России для банка за операцию C2B в СБП (с 01.05.2026)."""
    for upper, fee in CBR_SBP_BANK_TARIFF_2026:
        if check <= upper:
            return fee
    return CBR_SBP_BANK_TARIFF_2026[-1][1]


def annual_saving(turnover_month: float, shift_pct: float, to: str = "sbp", **kw) -> float:
    """Экономия за год, если shift_pct% оплат перевести с карты на СБП или ЦР."""
    ms = methods(**kw)
    moved = turnover_month * shift_pct / 100
    card_eff = ms["card"].rate_pct * (1 + ms["card"].vat_pct / 100)
    target_eff = ms[to].rate_pct
    return round(moved * (card_eff - target_eff) / 100 * 12, 2)


def table(checks=(300, 1700, 5000)):
    rows = []
    for c in checks:
        rows.append({
            "check": c,
            "dr_2027": cost(c, methods(year=2027)["dr"]),
            "sbp": cost(c, methods()["sbp"]),
            "card_1_5": cost(c, methods(card_rate=1.5)["card"]),
            "card_2_5": cost(c, methods(card_rate=2.5)["card"]),
        })
    return rows


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Стоимость платежа для продавца")
    ap.add_argument("--check", type=float, default=1700)
    ap.add_argument("--turnover", type=float, default=1_000_000)
    ap.add_argument("--shift", type=float, default=30)
    a = ap.parse_args()
    for key, m in methods().items():
        print(f"{m.name:<28} {cost(a.check, m):>8.2f} ₽")
    print(f"{'Тариф ЦБ для банка в СБП':<28} {cbr_bank_tariff(a.check):>8.2f} ₽")
    print(f"\nЭкономия в год при переводе {a.shift:.0f}% оплат: "
          f"в СБП — {annual_saving(a.turnover, a.shift, 'sbp'):,.0f} ₽; "
          f"в ЦР — {annual_saving(a.turnover, a.shift, 'dr'):,.0f} ₽".replace(",", " "))
