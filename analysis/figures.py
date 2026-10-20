"""Графики для отчёта (research/figures/*.png). Запуск: python analysis/figures.py"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import dataset as ds
from payment_cost import cost, methods

OUT = Path(__file__).resolve().parent.parent / "research" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

NAVY, PETROL, CYAN, BRIGHT, SKY, RED, AMBER, GREY = "#083542", "#016A80", "#0098AE", "#19C3D6", "#5B9BD5", "#D70E16", "#F4A62A", "#9AA7AD"
plt.rcParams.update({"font.family": "Segoe UI", "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#C9D6DB", "axes.titleweight": "bold", "axes.titlesize": 13, "figure.dpi": 150})


def save(fig, name, source):
    fig.text(0.01, 0.01, "Источник: " + source, fontsize=8, color="#6B7C85")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)


def labels(ax, bars, fmt="{:.1f}"):
    for b in bars:
        ax.annotate(fmt.format(b.get_height()).replace(".", ","), (b.get_x() + b.get_width() / 2, b.get_height()),
                    ha="center", va="bottom", fontsize=10, fontweight="bold", xytext=(0, 3), textcoords="offset points")


# 1. Рост СБП
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.8))
years = [str(r[0]) for r in ds.SBP_ANNUAL]
labels(a1, a1.bar(years, [r[1] for r in ds.SBP_ANNUAL], color=CYAN))
a1.set_title("Операций СБП в год, млрд")
labels(a2, a2.bar(years, [r[2] for r in ds.SBP_ANNUAL], color=PETROL))
a2.set_title("Объём СБП в год, трлн ₽")
for a in (a1, a2):
    a.set_yticks([])
save(fig, "01_sbp_growth.png", "Банк России, итоги 2023–2025 гг.")

# 2. Способы оплаты
fig, ax = plt.subplots(figsize=(7, 4))
names = [m[0] for m in ds.PAYMENT_METHODS_Q2_2026]
vals = [m[1] for m in ds.PAYMENT_METHODS_Q2_2026]
ax.pie(vals, labels=[f"{n}\n{v}%" for n, v in zip(names, vals)], colors=[NAVY, CYAN, SKY, RED, GREY], startangle=90,
       wedgeprops={"width": 0.42, "edgecolor": "white"}, textprops={"fontsize": 9.5})
ax.set_title("Доля способов в количестве оплат, II кв. 2026")
save(fig, "02_payment_methods.png", "Банк России, «Развитие НПС», II кв. 2026; «Прочее» — остаток, расчёт автора")

# 3. Чек 1 700 ₽
fig, ax = plt.subplots(figsize=(9, 3.6))
items = [("ЦР 2027 (0,3%)", cost(1700, methods(year=2027)["dr"]), 0), ("СБП (0,7%)", cost(1700, methods()["sbp"]), 0),
         ("Карта 1,5%", 25.5, 5.61), ("Карта 2,5%", 42.5, 9.35)]
y = range(len(items))[::-1]
ax.barh(list(y), [i[1] if i[2] == 0 else i[1] for i in items], color=[CYAN, CYAN, CYAN, CYAN])
ax.barh(list(y), [i[2] for i in items], left=[i[1] for i in items], color=RED, label="НДС 22%")
for yy, it in zip(y, items):
    tot = it[1] + it[2]
    ax.text(tot + 0.6, yy, f"{tot:.2f} ₽".replace(".", ","), va="center", fontweight="bold")
ax.set_yticks(list(y), [i[0] for i in items])
ax.set_xticks([])
ax.legend(frameon=False, loc="upper right")
ax.set_title("Сколько продавец платит с чека 1 700 ₽")
save(fig, "03_check_1700.png", "расчёт автора (analysis/payment_cost.py)")

# 4. Чувствительность
fig, ax = plt.subplots(figsize=(8, 3.8))
rates = [r / 10 for r in range(5, 31)]
ax.plot(rates, [1700 * r / 100 * 1.22 for r in rates], color=RED, lw=2.5, label="Карта с НДС (УСН)")
ax.plot(rates, [1700 * r / 100 for r in rates], color=AMBER, lw=2, ls="--", label="Карта без НДС (ОСН)")
ax.axhline(11.9, color=CYAN, lw=2.5, label="СБП 0,7%")
ax.axhline(5.1, color=NAVY, lw=2.5, label="ЦР 2027, 0,3%")
ax.axvspan(1.5, 2.5, color="#EAF6F8", zorder=0)
ax.text(2.0, 56, "рыночный диапазон\n1,5–2,5%", ha="center", fontsize=9, color="#33444C")
ax.axvline(0.574, color=GREY, lw=1, ls=":")
ax.annotate("0,57% — точка\nравенства с СБП", xy=(0.574, 11.9), xytext=(0.75, 24), fontsize=9, color="#33444C", arrowprops={"arrowstyle": "->", "color": "#6B7C85"})
ax.set_xlabel("Ставка эквайринга, %")
ax.set_ylabel("₽ с чека 1 700 ₽")
ax.legend(frameon=False, fontsize=9, loc="upper left", bbox_to_anchor=(0.0, 1.0))
ax.set_title("Чувствительность цены платежа к ставке эквайринга")
save(fig, "04_sensitivity.png", "расчёт автора")

# 5. На душу населения
fig, ax = plt.subplots(figsize=(7, 3.6))
pc = [(f"{s} · {c}", o * 1000 / p) for s, c, o, p, *_ in ds.INTERNATIONAL]
labels(ax, ax.bar([x[0] for x in pc], [x[1] for x in pc], color=[RED, SKY, PETROL]))
ax.set_yticks([])
ax.set_title("Операций на человека в месяц")
save(fig, "05_per_capita.png", "расчёт автора: Банк России, NPCI, Pix; население округлено")

# 6. Цифровой рубль
fig, ax = plt.subplots(figsize=(7, 3.6))
dd = [(d[0], d[1]) for d in ds.DIGITAL_RUBLE] + [("Ожидание ЦБ\nна конец 2026", ds.DR_CBR_EXPECTATION_YEAR_END_K)]
labels(ax, ax.bar([x[0] for x in dd], [x[1] for x in dd], color=[SKY, CYAN, GREY]), fmt="{:.0f}")
ax.set_yticks([])
ax.set_title("Кошельков цифрового рубля, тыс.")
save(fig, "06_digital_ruble.png", "СМИ со ссылкой на Банк России (вторичные), октябрь 2026")

# 7. Регионы
fig, ax = plt.subplots(figsize=(8, 4))
rg = ds.REGIONS_CARD_PAYMENTS_Q2_2026[::-1]
ax.barh([r[0] for r in rg], [r[1] for r in rg], color=[RED if r[0] == "СКФО" else NAVY if r[0] == "Россия" else PETROL for r in rg])
for i, r in enumerate(rg):
    ax.text(r[1] + 1, i, f"{r[1]:.0f}", va="center", fontsize=9.5)
ax.set_xticks([])
ax.set_title("Оплат картами на жителя за квартал, II кв. 2026")
save(fig, "07_regions.png", "Банк России, «Развитие НПС», II кв. 2026")

print("figures:", len(list(OUT.glob("*.png"))))


