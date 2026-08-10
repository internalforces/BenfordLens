<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="ru">
<context>
    <name>MainWindow</name>
    <message><source>Benford Lens</source><translation>Benford Lens</translation></message>
    <message><source>Column</source><translation>Столбец</translation></message>
    <message><source>Type</source><translation>Тип</translation></message>
    <message><source>Open File…</source><translation>Открыть файл…</translation></message>
    <message><source>Analyze</source><translation>Анализировать</translation></message>
    <message><source>Export Report…</source><translation>Экспортировать отчёт…</translation></message>
    <message><source>Third-party notices</source><translation>Уведомления о стороннем ПО</translation></message>
    <message><source>The third-party notices file is unavailable.</source><translation>Файл уведомлений о стороннем ПО недоступен.</translation></message>
    <message><source>Open a CSV or Excel file to begin.</source><translation>Откройте файл CSV или Excel, чтобы начать.</translation></message>
    <message><source>Open data file</source><translation>Открыть файл данных</translation></message>
    <message><source>Select sheet</source><translation>Выберите лист</translation></message>
    <message><source>Sheet:</source><translation>Лист:</translation></message>
    <message><source>Could not open file</source><translation>Не удалось открыть файл</translation></message>
    <message><source>Select a column, then click Analyze.</source><translation>Выберите столбец, затем нажмите «Анализировать».</translation></message>
    <message><source>Cannot select column</source><translation>Невозможно выбрать столбец</translation></message>
    <message><source>Cannot analyze</source><translation>Невозможно выполнить анализ</translation></message>
    <message><source>Cannot show rows</source><translation>Невозможно показать строки</translation></message>
    <message><source>Export report</source><translation>Экспорт отчёта</translation></message>
    <message><source>Could not export report</source><translation>Не удалось экспортировать отчёт</translation></message>
    <message><source>No valid numeric values were found in the selected column.</source><translation>В выбранном столбце не найдено допустимых числовых значений.</translation></message>
    <message><source>Only {sample_size} valid numeric value(s) were found, which is too few for a meaningful comparison to the expected Benford distribution. Try a column with more data.</source><translation>Найдено только {sample_size} допустимых числовых значений, чего недостаточно для содержательного сравнения с ожидаемым распределением Бенфорда. Попробуйте выбрать столбец с большим объёмом данных.</translation></message>
    <message><source>The overall distribution is close to the expected Benford distribution. Interpret this comparison together with the characteristics of the data.</source><translation>Общее распределение близко к ожидаемому распределению Бенфорда. Интерпретируйте это сравнение с учётом характеристик данных.</translation></message>
    <message><source>The overall distribution differs somewhat from the expected Benford distribution. Further review of the data characteristics may be warranted.</source><translation>Общее распределение несколько отличается от ожидаемого распределения Бенфорда. Может потребоваться дополнительное изучение характеристик данных.</translation></message>
    <message><source>First digit</source><translation>Первая цифра</translation></message>
    <message><source>Second digit</source><translation>Вторая цифра</translation></message>
    <message><source>First + second</source><translation>Первая + вторая</translation></message>
    <message><source>Observed</source><translation>Наблюдаемое</translation></message>
    <message><source>Expected (Benford)</source><translation>Ожидаемое (Бенфорд)</translation></message>
    <message><source>Proportion (%)</source><translation>Доля (%)</translation></message>
    <message><source>{position} analysis</source><translation>Анализ: {position}</translation></message>
</context>
<context>
    <name>PreprocessingPanel</name>
    <message><source>Negative values</source><translation>Отрицательные значения</translation></message>
    <message><source>Zero values</source><translation>Нулевые значения</translation></message>
    <message><source>Decimal values</source><translation>Дробные значения</translation></message>
    <message><source>Blank values</source><translation>Пустые значения</translation></message>
    <message><source>Duplicate values</source><translation>Повторяющиеся значения</translation></message>
    <message><source>Text-to-number</source><translation>Преобразование текста в число</translation></message>
    <message><source>Keep</source><translation>Оставить</translation></message>
    <message><source>Convert to absolute value</source><translation>Преобразовать в абсолютное значение</translation></message>
    <message><source>Exclude</source><translation>Исключить</translation></message>
    <message><source>Use as-is</source><translation>Использовать без изменений</translation></message>
    <message><source>Round</source><translation>Округлить</translation></message>
    <message><source>Truncate</source><translation>Отбросить дробную часть</translation></message>
    <message><source>Auto-convert</source><translation>Преобразовывать автоматически</translation></message>
    <message><source>Do not convert</source><translation>Не преобразовывать</translation></message>
    <message><source>Preview</source><translation>Предпросмотр</translation></message>
    <message><source>Before</source><translation>До</translation></message>
    <message><source>After</source><translation>После</translation></message>
    <message><source>values (excluded: {blank} blank, {non_numeric} non-numeric, {negative} negative, {zero} zero)</source><translation>значений (исключено: пустых — {blank}, нечисловых — {non_numeric}, отрицательных — {negative}, нулевых — {zero})</translation></message>
</context>
<context>
    <name>SuitabilityPanel</name>
    <message><source>🟢 Good</source><translation>🟢 Хорошо</translation></message>
    <message><source>🟡 Caution</source><translation>🟡 Внимание</translation></message>
    <message><source>🔴 Difficult to determine</source><translation>🔴 Трудно определить</translation></message>
    <message><source>No caveats found.</source><translation>Особенности, требующие внимания, не обнаружены.</translation></message>
    <message><source>These are data characteristics, not a determination of whether Benford's Law applies — that judgment is yours to make.</source><translation>Это характеристики данных, а не заключение о применимости закона Бенфорда — решение остаётся за вами.</translation></message>
    <message><source>Sample count</source><translation>Размер выборки</translation></message>
    <message><source>Minimum value</source><translation>Минимальное значение</translation></message>
    <message><source>Maximum value</source><translation>Максимальное значение</translation></message>
    <message><source>Magnitude range</source><translation>Диапазон порядков величины</translation></message>
    <message><source>Distinct values</source><translation>Уникальные значения</translation></message>
    <message><source>Duplicate rate</source><translation>Доля повторов</translation></message>
    <message><source>Zero rate</source><translation>Доля нулевых значений</translation></message>
    <message><source>Negative rate</source><translation>Доля отрицательных значений</translation></message>
    <message><source>Missing rate</source><translation>Доля пропущенных значений</translation></message>
    <message><source>Only {sample_count} valid value(s) — below the {minimum}-value floor for a meaningful comparison.</source><translation>Найдено только {sample_count} допустимых значений — меньше минимального уровня в {minimum} значений для содержательного сравнения.</translation></message>
    <message><source>{sample_count} valid values is a workable but modest sample size.</source><translation>{sample_count} допустимых значений образуют пригодную, но небольшую выборку.</translation></message>
    <message><source>Values span only a single order of magnitude.</source><translation>Значения охватывают только один порядок величины.</translation></message>
    <message><source>Values span {digit_range} orders of magnitude.</source><translation>Значения охватывают {digit_range} порядков величины.</translation></message>
    <message><source>Very few distinct values relative to the sample size.</source><translation>Уникальных значений очень мало относительно размера выборки.</translation></message>
    <message><source>Values repeat somewhat more than expected for this sample size.</source><translation>Значения повторяются несколько чаще, чем ожидается при таком размере выборки.</translation></message>
    <message><source>{zero_rate:.0%} of the source values were zero.</source><translation>{zero_rate:.0%} исходных значений были нулевыми.</translation></message>
    <message><source>{negative_rate:.0%} of the source values were negative — check whether the negative-value preprocessing option fits this data.</source><translation>{negative_rate:.0%} исходных значений были отрицательными — проверьте, подходит ли этим данным выбранный способ обработки отрицательных значений.</translation></message>
    <message><source>{missing_rate:.0%} of the source values were blank.</source><translation>{missing_rate:.0%} исходных значений были пустыми.</translation></message>
</context>
<context>
    <name>ExpertStatisticsPanel</name>
    <message><source>Show Details</source><translation>Показать подробности</translation></message>
    <message><source>Hide Details</source><translation>Скрыть подробности</translation></message>
    <message><source>Sample size</source><translation>Размер выборки</translation></message>
    <message><source>Mean absolute deviation (MAD)</source><translation>Среднее абсолютное отклонение (MAD)</translation></message>
    <message><source>Chi-square statistic</source><translation>Статистика хи-квадрат</translation></message>
    <message><source>Chi-square p-value</source><translation>p-значение хи-квадрат</translation></message>
    <message><source>KS statistic</source><translation>Статистика KS</translation></message>
    <message><source>KS p-value</source><translation>p-значение KS</translation></message>
    <message><source>Reference statistics only. Interpret them in light of the data and sample characteristics. KS compares base-10 log mantissas with a uniform distribution.</source><translation>Статистические показатели приведены только для справки. Интерпретируйте их с учётом данных и характеристик выборки. KS сравнивает мантиссы десятичных логарифмов с равномерным распределением.</translation></message>
    <message><source>First-digit sample size</source><translation>Размер выборки для первой цифры</translation></message>
    <message><source>First-digit mean absolute deviation (MAD)</source><translation>Среднее абсолютное отклонение для первой цифры (MAD)</translation></message>
    <message><source>First-digit Chi-square statistic</source><translation>Статистика хи-квадрат для первой цифры</translation></message>
    <message><source>First-digit Chi-square p-value</source><translation>p-значение хи-квадрат для первой цифры</translation></message>
    <message><source>Second-digit sample size</source><translation>Размер выборки для второй цифры</translation></message>
    <message><source>Second-digit mean absolute deviation (MAD)</source><translation>Среднее абсолютное отклонение для второй цифры (MAD)</translation></message>
    <message><source>Second-digit Chi-square statistic</source><translation>Статистика хи-квадрат для второй цифры</translation></message>
    <message><source>Second-digit Chi-square p-value</source><translation>p-значение хи-квадрат для второй цифры</translation></message>
    <message><source>Shared KS sample size</source><translation>Размер общей выборки KS</translation></message>
    <message><source>Shared KS statistic</source><translation>Общая статистика KS</translation></message>
    <message><source>Shared KS p-value</source><translation>Общее p-значение KS</translation></message>
</context>
<context>
    <name>DrillDownPanel</name>
    <message><source>Search…</source><translation>Поиск…</translation></message>
    <message><source>Export CSV…</source><translation>Экспорт CSV…</translation></message>
    <message><source>Export rows</source><translation>Экспорт строк</translation></message>
    <message><source>Could not export</source><translation>Не удалось экспортировать</translation></message>
</context>
</TS>
