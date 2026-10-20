"""Единый набор данных исследования «Экономика быстрого платежа».

Каждая запись несёт источник и статус достоверности:
  primary   — первичный источник (Банк России, НСПК, тексты решений)
  secondary — вторичный источник (СМИ, сервисы, агрегаторы)
  disputed  — источники расходятся
  author    — расчёт или оценка автора

Данные проверены на 20.10.2026. Запуск `python analysis/build_data.py`
пересобирает CSV в data/ и JSON для сайта в docs/data/.
"""

CHECKED = "2026-10-20"

SOURCES = {
    "cbr_nps_q2_2026": ("Банк России. Развитие НПС, II кв. 2026", "https://cbr.ru/Collection/Collection/File/62351/development_nps_2026-q2.pdf", "primary"),
    "cbr_sbp_2023": ("Банк России. Показатели СБП в 2023 году удвоились, 02.02.2024", "https://www.cbr.ru/press/event/?id=18391", "primary"),
    "cbr_sbp_2024": ("Банк России. Итоги СБП 2024", "https://www.cbr.ru/press/event/?id=23333", "primary"),
    "cbr_sbp_q4_2025": ("Банк России. СБП: основные показатели, IV кв. 2025", "https://www.cbr.ru/analytics/nps/sbp/4_2025/", "primary"),
    "cbr_sbp_tariff_2026": ("Банк России. Решение о тарифах в СБП от 27.03.2026", "https://cbr.ru/rbr/dir_decisions/rsd_2026-03-27_45_01/", "primary"),
    "cbr_dr_tariff_2026": ("Банк России. Решение о тарифах платформы цифрового рубля от 28.08.2026 (Гарант)", "https://www.garant.ru/products/ipo/prime/doc/414732671/", "primary"),
    "cbr_dr_rollout": ("Банк России. Массовое внедрение цифрового рубля, 15.07.2025", "https://www.cbr.ru/press/event/?id=25772", "primary"),
    "cbr_fraud_2025": ("Банк России. Обзор операций без согласия клиентов, 2025", "https://www.cbr.ru/analytics/ib/operations_survey/2025/", "primary"),
    "cbr_fraud_q2_2026": ("Банк России. Обзор операций без согласия клиентов, II кв. 2026", "https://cbr.ru/statistics/ib/review_2q_2026/", "primary"),
    "kommersant_2025": ("Коммерсантъ, 06.02.2026 — итоги СБП 2025", "https://www.kommersant.ru/doc/8418300", "secondary"),
    "izvestia_dr": ("«Известия», 02.09.2026 — старт цифрового рубля", "https://iz.ru/2159280/2026-09-02/zapusk-tcifrovogo-rublia-v-krupneishikh-bankakh-startoval-s-pereboiami", "secondary"),
    "dr_month": ("РБ.ру, ТКС.ру, Коммерсантъ — первый месяц цифрового рубля (октябрь 2026)", "https://rb.ru/news/zapusk-cifrovogo-rublya-prevzoshyol-ozhidaniya-cb-s-1-sentyabrya-rossiyane-otkryli-bolee-220-tys-schetov/", "secondary"),
    "kontur_sbp": ("Контур. Что нужно знать бизнесу о СБП в 2026 году (26.05.2026)", "https://kontur.ru/articles/6279", "secondary"),
    "nspk_blog": ("НСПК. СБП или эквайринг в 2026 году", "https://sbp.nspk.ru/blog/sbp-ili-ekvairing-cto-vygodnee-dlia-malogo-biznesa", "secondary"),
    "vat_425": ("Материалы банков о законе № 425-ФЗ (НДС на эквайринг)", "https://pay.yandex.ru/blog/articles/ekvajring-2026", "secondary"),
    "pix": ("clearingpost.com — Pix, август 2026", "https://clearingpost.com/insights/pix-passed-8-billion-transactions-in-a-month-for-the-first-time-in-august-2026/", "secondary"),
    "upi": ("Business Standard, Medianama — UPI, август 2026", "https://www.medianama.com/2026/09/223-upi-transactions-august-2026/", "secondary"),
    "cashback": ("Т—Ж, Ведомости — кэшбэк банков 2024–2025", "https://t-j.ru/news/cashback-392mlgd-2024g/", "secondary"),
    "biometrics": ("Финанс Mail, ComNews — биометрические платежи 2025", "https://www.comnews.ru/content/243113/2026-01-12/2026-w03/1008/biometriya-zashagala-strane", "secondary"),
    "keyrate": ("Банк России — ключевая ставка 14% с 24.07.2026 (через Сбер CIB)", "https://sbercib.ru/publication/reshenie-banka-rossii-po-klyuchevoi-stavke-ot-24-iyulya-2026-goda", "secondary"),
}

# ── СБП по годам
SBP_ANNUAL = [
    # год, операций млрд, объём трлн ₽, продавцов млн, источник, статус
    (2023, 7.0, 31.0, 1.5, "cbr_sbp_2023", "primary"),   # «свыше 7 млрд»
    (2024, 13.4, 69.5, 2.2, "cbr_sbp_2024", "primary"),
    (2025, 18.3, 103.0, 3.0, "kommersant_2025", "primary"),
]

SBP_DAILY = [  # млн операций в сутки
    ("IV кв. 2023", 26, "cbr_sbp_2024"), ("IV кв. 2024", 45, "cbr_sbp_2024"),
    ("2025 (среднее)", 50, "kommersant_2025"), ("II кв. 2026", 56, "cbr_nps_q2_2026"),
]

SBP_STRUCTURE_Q2_2026 = [  # тип, доля по количеству %, доля по объёму %, операций млрд, объём трлн
    ("C2C — переводы между людьми", 68, 88, 3.5, 26.5),
    ("C2B — покупки", 30, 9, 1.5, 2.7),
    ("Прочее (остаток, расчёт автора)", 2, 3, None, None),
]

MERCHANTS_QUARTERLY = [  # квартал, все ТСП млн, из них МСП млн
    ("II кв. 2025", 2.55, 2.08), ("III кв. 2025", 2.75, 2.15), ("IV кв. 2025", 2.97, 2.30),
    ("I кв. 2026", 3.14, 2.43), ("II кв. 2026", 3.34, 2.55),
]

PAYMENT_METHODS_Q2_2026 = [  # способ, доля в количестве оплат %
    ("Карты", 60), ("Мобильный и онлайн-банкинг", 13), ("Электронные кошельки", 11),
    ("QR-коды", 5), ("Прочее (остаток, расчёт автора)", 11),
]

TRANSFERS_Q2_2026 = [("СБП", 55), ("Карты", 21), ("Счета без СБП", 22), ("Иное", 2)]

AVG_CHECK_Q2_2026 = [  # способ, средний чек ₽
    ("Смартфон (приложения)", 716), ("Биометрия", 730), ("Карта", 838),
    ("Электронный кошелёк", 1178), ("QR-код", 1432), ("Онлайн-банкинг", 2438),
]

REGIONS_CARD_PAYMENTS_Q2_2026 = [  # округ, оплат картами на жителя за квартал
    ("СЗФО", 112.5), ("СФО", 103.8), ("ЦФО", 103.3), ("УФО", 100.8), ("ДФО", 97.5),
    ("ПФО", 95.4), ("Россия", 92.0), ("ЮФО", 84.0), ("СКФО", 31.9),
]

# ── тарифы (комиссия продавца), % от чека
TARIFFS = {
    "card_min": 1.5, "card_max": 2.5, "card_default": 2.0,      # secondary
    "sbp_general": 0.7, "sbp_social": 0.4, "sbp_utilities": 0.2,  # secondary
    "sbp_cap_rub": 1500,                                          # secondary
    "dr_2026": 0.0, "dr_2027": 0.3, "dr_cap_rub": 1500,           # primary; потолок — disputed
    "vat_acquiring": 22.0,                                        # secondary
}

CBR_SBP_BANK_TARIFF_2026 = [  # верхняя граница суммы, ₽ за операцию с участием бизнеса
    (125, 0.05), (250, 0.12), (1000, 0.30), (3000, 0.80), (6000, 2.00), (1_000_000, 3.00),
]

INTERNATIONAL = [  # система, страна, операций в месяц млрд, население млн, период, источник
    ("СБП", "Россия", 1.70, 146, "II кв. 2026 (5,1 млрд / 3)", "cbr_nps_q2_2026"),
    ("UPI", "Индия", 24.51, 1450, "август 2026", "upi"),
    ("Pix", "Бразилия", 8.11, 213, "август 2026", "pix"),
]

DIGITAL_RUBLE = [  # дата, кошельков тыс., операций тыс., источник
    ("10.09.2026", 87, 50, "izvestia_dr"),
    ("12.10.2026", 220, 150, "dr_month"),
]
DR_CBR_EXPECTATION_YEAR_END_K = 60  # ожидание ЦБ к концу 2026 г., тыс. кошельков (слова Э. Набиуллиной в пересказе СМИ)

FRAUD = {
    "2025_total_bn": 29.3, "2025_returned_pct": 5.9, "2024_returned_pct": 9.9, "2025_share_pct": 0.00071,
    "q2_2026_total_ops_k": 458.7, "q2_2026_total_bn": 7.35,
    "q2_2026_sbp_ops": 129055, "q2_2026_sbp_bn": 2.74,
}

EXTRA = {
    "cashback_2024_bn": 392, "cashback_2025_bn": "450–500",
    "biometrics_ebs_users_mln_2025": 10, "biometrics_tx_2025_mln": 195.2, "biometrics_volume_2025_bn": 150.9,
    "key_rate_pct": 14.0, "sbp_free_limit_others_rub": 100_000, "sbp_free_limit_me2me_rub": 30_000_000,
    "sbp_cross_border_countries": 9,
}
