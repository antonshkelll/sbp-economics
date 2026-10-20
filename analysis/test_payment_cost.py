"""Проверка, что расчёты в презентации и отчёте воспроизводятся кодом.
Запуск: python analysis/test_payment_cost.py
"""
from payment_cost import table, annual_saving, cbr_bank_tariff

EXPECTED = {
    300: (0.90, 2.10, 5.49, 9.15),
    1700: (5.10, 11.90, 31.11, 51.85),
    5000: (15.00, 35.00, 91.50, 152.50),
}

for row in table():
    got = (row["dr_2027"], row["sbp"], row["card_1_5"], row["card_2_5"])
    assert got == EXPECTED[row["check"]], (row["check"], got)

assert annual_saving(1_000_000, 30, "sbp") == 62_640
assert annual_saving(1_000_000, 30, "dr") == 77_040
assert annual_saving(3_000_000, 30, "sbp") == 187_920
assert annual_saving(10_000_000, 30, "dr") == 770_400
assert cbr_bank_tariff(1700) == 0.80
assert cbr_bank_tariff(100) == 0.05

print("OK: все расчёты совпадают с отчётом и презентацией")
