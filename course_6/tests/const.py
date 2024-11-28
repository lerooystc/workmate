from numpy import nan
import pandas as pd


MOCK_EXCEL_DICT = {
    "Unnamed: 0": {
        0: nan,
        1: nan,
        2: nan,
        3: nan,
        4: nan,
        5: nan,
        6: nan,
        7: nan,
        8: nan,
        9: nan,
        10: nan,
        11: nan,
        12: nan,
        13: nan,
        14: nan,
        15: nan,
        16: nan,
        531: nan,
        532: nan,
    },
    "Форма СЭТ-БТ": {
        0: "Бюллетень",
        1: "по итогам торгов",
        2: "Дата торгов: 21.11.2024",
        3: "Секция Биржи: «Нефтепродукты» АО «СПбМТСБ»",
        4: "Единица измерения: Метрическая тонна",
        5: "Код\nИнструмента",
        6: nan,
        7: "A001KRU060F",
        8: "A100ANK060F",
        9: "A100NVY060F",
        10: "A100SCI005A",
        11: "A100STI060F",
        12: "A100UFM060F",
        13: "A10KZLY060W",
        14: "A592ABS005A",
        15: "A592ACH005A",
        16: "A592AKR060F",
        531: "Итого:",
        532: "Итого по секции:",
    },
    "Unnamed: 2": {
        0: nan,
        1: nan,
        2: nan,
        3: nan,
        4: nan,
        5: "Наименование\nИнструмента",
        6: nan,
        7: "Бензин (АИ-100-К5), ст. Круглое Поле (ст. отправления)",
        8: "Бензин (АИ-100-К5), Ангарск-группа станций (ст. отправления)",
        9: "Бензин (АИ-100-К5), ст. Новоярославская (ст. отправления)",
        10: "Бензин (АИ-100-К5), НБ Адлерская (самовывоз автотранспортом)",
        11: "Бензин (АИ-100-К5), ст. Стенькино II (ст. отправления)",
        12: "Бензин (АИ-100-К5), Уфа-группа станций (ст. отправления)",
        13: "Бензин (АИ-100-К5)-Евро, ст. Злынка-Экспорт (промежуточная станция)",
        14: "Бензин (АИ-92-К5) по ГОСТ, НБ Абаканская (самовывоз автотранспортом)",
        15: "Бензин (АИ-92-К5) по ГОСТ, Ачинский НПЗ (самовывоз автотранспортом)",
        16: "Бензин (АИ-92-К5) по ГОСТ, ст. Аксарайская II (ст. отправления)",
        531: nan,
        532: nan,
    },
    "Unnamed: 3": {
        0: nan,
        1: nan,
        2: nan,
        3: nan,
        4: nan,
        5: "Базис\nпоставки",
        6: nan,
        7: "ст. Круглое Поле",
        8: "Ангарск-группа станций",
        9: "ст. Новоярославская",
        10: "НБ Адлерская",
        11: "ст. Стенькино II",
        12: "Уфа-группа станций",
        13: "ст. Злынка-Экспорт",
        14: "НБ Абаканская",
        15: "Ачинский НПЗ",
        16: "ст. Аксарайская II",
        531: nan,
        532: nan,
    },
    "Unnamed: 4": {
        0: nan,
        1: nan,
        2: nan,
        3: nan,
        4: nan,
        5: "Объем\nДоговоров\nв единицах\nизмерения",
        6: nan,
        7: "-",
        8: "60",
        9: "60",
        10: "-",
        11: "60",
        12: "60",
        13: "60",
        14: "50",
        15: "125",
        16: "720",
        531: "142474",
        532: nan,
    },
    "Unnamed: 5": {
        0: nan,
        1: nan,
        2: nan,
        3: nan,
        4: nan,
        5: "Обьем\nДоговоров,\nруб.",
        6: nan,
        7: "-",
        8: "6246000",
        9: "5753640",
        10: "-",
        11: "5748000",
        12: "5970000",
        13: "5280000",
        14: "3285000",
        15: "7850000",
        16: "45026340",
        531: "8782799771",
        532: "8782799771",
    },
    "Unnamed: 6": {
        0: nan,
        1: nan,
        2: nan,
        3: nan,
        4: nan,
        5: "Изменение рыночной\nцены к цене\nпредыдуего дня",
        6: "Руб.",
        7: "-",
        8: "-",
        9: "477",
        10: "-",
        11: "-",
        12: "-",
        13: "-",
        14: "700",
        15: "-1700",
        16: "409",
        531: nan,
        532: nan,
    },
    "Unnamed: 7": {
        0: nan,
        1: nan,
        2: nan,
        3: nan,
        4: nan,
        5: nan,
        6: "%",
        7: "-",
        8: "-",
        9: "0.5",
        10: "-",
        11: "-",
        12: "-",
        13: "-",
        14: "1.07",
        15: "-2.71",
        16: "0.65",
        531: nan,
        532: nan,
    },
    "Unnamed: 8": {
        0: nan,
        1: nan,
        2: nan,
        3: nan,
        4: nan,
        5: "Цена (за единицу измерения), руб.",
        6: "Минимальная",
        7: "-",
        8: "104100",
        9: "95894",
        10: "-",
        11: "95800",
        12: "99500",
        13: "88000",
        14: "65700",
        15: "62500",
        16: "62439",
        531: nan,
        532: nan,
    },
    "Unnamed: 9": {
        0: nan,
        1: nan,
        2: nan,
        3: nan,
        4: nan,
        5: nan,
        6: "Средневзвешенная",
        7: "-",
        8: "104100",
        9: "95894",
        10: "-",
        11: "95800",
        12: "99500",
        13: "88000",
        14: "65700",
        15: "62800",
        16: "62537",
        531: nan,
        532: nan,
    },
    "Unnamed: 10": {
        0: nan,
        1: nan,
        2: nan,
        3: nan,
        4: nan,
        5: nan,
        6: "Максимальная",
        7: "-",
        8: "104100",
        9: "95894",
        10: "-",
        11: "95800",
        12: "99500",
        13: "88000",
        14: "65700",
        15: "63500",
        16: "62600",
        531: nan,
        532: nan,
    },
    "Unnamed: 11": {
        0: nan,
        1: nan,
        2: nan,
        3: nan,
        4: nan,
        5: nan,
        6: "Рыночная",
        7: "91500",
        8: "104100",
        9: "95894",
        10: "-",
        11: "95800",
        12: "99500",
        13: "88000",
        14: "65700",
        15: "62800",
        16: "62537",
        531: nan,
        532: nan,
    },
    "Unnamed: 12": {
        0: nan,
        1: nan,
        2: nan,
        3: nan,
        4: nan,
        5: "Цена в Заявках (за единицу\nизмерения)",
        6: "Лучшее\nпредложение",
        7: "92000",
        8: "104100",
        9: "95894",
        10: "111000",
        11: "95800",
        12: "95000",
        13: "88000",
        14: "65700",
        15: "62500",
        16: "62439",
        531: nan,
        532: nan,
    },
    "Unnamed: 13": {
        0: nan,
        1: nan,
        2: nan,
        3: nan,
        4: nan,
        5: nan,
        6: "Лучший\nспрос",
        7: "-",
        8: "104100",
        9: "96373",
        10: "-",
        11: "96279",
        12: "99998",
        13: "88000",
        14: "65700",
        15: "63500",
        16: "62600",
        531: nan,
        532: nan,
    },
    "Unnamed: 14": {
        0: nan,
        1: nan,
        2: nan,
        3: nan,
        4: nan,
        5: "Количество\nДоговоров,\nшт.",
        6: nan,
        7: "-",
        8: "1",
        9: "1",
        10: "-",
        11: "1",
        12: "1",
        13: "1",
        14: "2",
        15: "5",
        16: "9",
        531: "1737",
        532: "1737",
    },
}

EXCEL_DF = pd.DataFrame.from_dict(MOCK_EXCEL_DICT)