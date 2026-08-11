<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="ja">
<context>
    <name>MainWindow</name>
    <message><source>Benford Lens</source><translation>Benford Lens</translation></message>
    <message><source>Column</source><translation>列</translation></message>
    <message><source>Type</source><translation>種類</translation></message>
    <message><source>Open File…</source><translation>ファイルを開く…</translation></message>
    <message><source>Analyze</source><translation>分析</translation></message>
    <message><source>Export Report…</source><translation>レポートを書き出す…</translation></message>
    <message><source>Third-party notices</source><translation>サードパーティ通知</translation></message>
    <message><source>The third-party notices file is unavailable.</source><translation>サードパーティ通知ファイルを利用できません。</translation></message>
    <message><source>Open a CSV or Excel file to begin.</source><translation>開始するには CSV または Excel ファイルを開いてください。</translation></message>
    <message><source>Open data file</source><translation>データファイルを開く</translation></message>
    <message><source>Select sheet</source><translation>シートを選択</translation></message>
    <message><source>Sheet:</source><translation>シート:</translation></message>
    <message><source>Could not open file</source><translation>ファイルを開けませんでした</translation></message>
    <message><source>Select a column, then click Analyze.</source><translation>列を選択してから「分析」をクリックしてください。</translation></message>
    <message><source>Cannot select column</source><translation>列を選択できません</translation></message>
    <message><source>Cannot analyze</source><translation>分析できません</translation></message>
    <message><source>Cannot show rows</source><translation>行を表示できません</translation></message>
    <message><source>Export report</source><translation>レポートを書き出す</translation></message>
    <message><source>Could not export report</source><translation>レポートを書き出せませんでした</translation></message>
    <message><source>No valid numeric values were found in the selected column.</source><translation>選択した列に有効な数値が見つかりませんでした。</translation></message>
    <message><source>Only {sample_size} valid numeric value(s) were found, which is too few for a meaningful comparison to the expected Benford distribution. Try a column with more data.</source><translation>有効な数値が {sample_size} 件しか見つからず、期待されるベンフォード分布と有意義に比較するには少なすぎます。データがより多い列をお試しください。</translation></message>
    <message><source>The overall distribution is close to the expected Benford distribution. Interpret this comparison together with the characteristics of the data.</source><translation>全体の分布は期待されるベンフォード分布に近い形です。この比較結果はデータの特性と合わせて解釈してください。</translation></message>
    <message><source>The overall distribution differs somewhat from the expected Benford distribution. Further review of the data characteristics may be warranted.</source><translation>全体の分布は期待されるベンフォード分布とやや異なります。データの特性をさらに確認することが望ましい場合があります。</translation></message>
    <message><source>First digit</source><translation>第1桁</translation></message>
    <message><source>Second digit</source><translation>第2桁</translation></message>
    <message><source>First + second</source><translation>第1桁 + 第2桁</translation></message>
    <message><source>Observed</source><translation>観測値</translation></message>
    <message><source>Expected (Benford)</source><translation>期待値（ベンフォード）</translation></message>
    <message><source>Proportion (%)</source><translation>割合（%）</translation></message>
    <message><source>{position} analysis</source><translation>{position}の分析</translation></message>
</context>
<context>
    <name>PreprocessingPanel</name>
    <message><source>Negative values</source><translation>負の値</translation></message>
    <message><source>Zero values</source><translation>ゼロの値</translation></message>
    <message><source>Decimal values</source><translation>小数の値</translation></message>
    <message><source>Blank values</source><translation>空欄の値</translation></message>
    <message><source>Duplicate values</source><translation>重複する値</translation></message>
    <message><source>Text-to-number</source><translation>文字列から数値への変換</translation></message>
    <message><source>Keep</source><translation>保持</translation></message>
    <message><source>Convert to absolute value</source><translation>絶対値に変換</translation></message>
    <message><source>Exclude</source><translation>除外</translation></message>
    <message><source>Use as-is</source><translation>そのまま使用</translation></message>
    <message><source>Round</source><translation>四捨五入</translation></message>
    <message><source>Truncate</source><translation>切り捨て</translation></message>
    <message><source>Auto-convert</source><translation>自動変換</translation></message>
    <message><source>Do not convert</source><translation>変換しない</translation></message>
    <message><source>Preview</source><translation>プレビュー</translation></message>
    <message><source>Before</source><translation>変更前</translation></message>
    <message><source>After</source><translation>変更後</translation></message>
    <message><source>values (excluded: {blank} blank, {non_numeric} non-numeric, {negative} negative, {zero} zero)</source><translation>件の値(除外:空欄 {blank} 件、非数値 {non_numeric} 件、負の値 {negative} 件、ゼロ {zero} 件)</translation></message>
</context>
<context>
    <name>SuitabilityPanel</name>
    <message><source>🟢 Good</source><translation>🟢 良好</translation></message>
    <message><source>🟡 Caution</source><translation>🟡 注意</translation></message>
    <message><source>🔴 Difficult to determine</source><translation>🔴 判断が難しい</translation></message>
    <message><source>No caveats found.</source><translation>特に注意点はありません。</translation></message>
    <message><source>These are data characteristics, not a determination of whether Benford's Law applies — that judgment is yours to make.</source><translation>これらはデータの特性を示すものであり、ベンフォードの法則が当てはまるかどうかを判断するものではありません。その判断はご自身で行ってください。</translation></message>
    <message><source>Sample count</source><translation>サンプル数</translation></message>
    <message><source>Minimum value</source><translation>最小値</translation></message>
    <message><source>Maximum value</source><translation>最大値</translation></message>
    <message><source>Magnitude range</source><translation>桁数の範囲</translation></message>
    <message><source>Distinct values</source><translation>異なる値の数</translation></message>
    <message><source>Duplicate rate</source><translation>重複率</translation></message>
    <message><source>Zero rate</source><translation>ゼロの割合</translation></message>
    <message><source>Negative rate</source><translation>負の数の割合</translation></message>
    <message><source>Missing rate</source><translation>欠損の割合</translation></message>
    <message><source>Only {sample_count} valid value(s) — below the {minimum}-value floor for a meaningful comparison.</source><translation>有効な値が {sample_count} 件しかなく、意味のある比較に必要な {minimum} 件の下限を下回っています。</translation></message>
    <message><source>{sample_count} valid values is a workable but modest sample size.</source><translation>有効な値 {sample_count} 件は分析に使えますが、サンプルサイズはやや小さめです。</translation></message>
    <message><source>Values span only a single order of magnitude.</source><translation>値が単一の桁数範囲にしか分布していません。</translation></message>
    <message><source>Values span {digit_range} orders of magnitude.</source><translation>値は {digit_range} 桁分の範囲に分布しています。</translation></message>
    <message><source>Very few distinct values relative to the sample size.</source><translation>サンプルサイズに対して、異なる値の数が非常に少なくなっています。</translation></message>
    <message><source>Values repeat somewhat more than expected for this sample size.</source><translation>サンプルサイズに対して、値の重複がやや多くなっています。</translation></message>
    <message><source>{zero_rate:.0%} of the source values were zero.</source><translation>元データの値のうち {zero_rate:.0%} がゼロでした。</translation></message>
    <message><source>{negative_rate:.0%} of the source values were negative — check whether the negative-value preprocessing option fits this data.</source><translation>元データの値のうち {negative_rate:.0%} が負の数でした。負の値の前処理オプションがこのデータに適しているか確認してください。</translation></message>
    <message><source>{missing_rate:.0%} of the source values were blank.</source><translation>元データの値のうち {missing_rate:.0%} が空欄でした。</translation></message>
</context>
<context>
    <name>ExpertStatisticsPanel</name>
    <message><source>Show Details</source><translation>詳細を表示</translation></message>
    <message><source>Hide Details</source><translation>詳細を隠す</translation></message>
    <message><source>Sample size</source><translation>サンプルサイズ</translation></message>
    <message><source>Mean absolute deviation (MAD)</source><translation>平均絶対偏差 (MAD)</translation></message>
    <message><source>Chi-square statistic</source><translation>カイ二乗統計量</translation></message>
    <message><source>Chi-square p-value</source><translation>カイ二乗 p 値</translation></message>
    <message><source>KS statistic</source><translation>KS 統計量</translation></message>
    <message><source>KS p-value</source><translation>KS p 値</translation></message>
    <message><source>Reference statistics only. Interpret them in light of the data and sample characteristics. KS compares base-10 log mantissas with a uniform distribution.</source><translation>これらは参考用の統計量です。データとサンプルの特性を踏まえて解釈してください。KS は常用対数の小数部分を一様分布と比較します。</translation></message>
    <message><source>First-digit sample size</source><translation>第1桁のサンプルサイズ</translation></message>
    <message><source>First-digit mean absolute deviation (MAD)</source><translation>第1桁の平均絶対偏差 (MAD)</translation></message>
    <message><source>First-digit Chi-square statistic</source><translation>第1桁のカイ二乗統計量</translation></message>
    <message><source>First-digit Chi-square p-value</source><translation>第1桁のカイ二乗 p 値</translation></message>
    <message><source>Second-digit sample size</source><translation>第2桁のサンプルサイズ</translation></message>
    <message><source>Second-digit mean absolute deviation (MAD)</source><translation>第2桁の平均絶対偏差 (MAD)</translation></message>
    <message><source>Second-digit Chi-square statistic</source><translation>第2桁のカイ二乗統計量</translation></message>
    <message><source>Second-digit Chi-square p-value</source><translation>第2桁のカイ二乗 p 値</translation></message>
    <message><source>Shared KS sample size</source><translation>共通 KS のサンプルサイズ</translation></message>
    <message><source>Shared KS statistic</source><translation>共通 KS 統計量</translation></message>
    <message><source>Shared KS p-value</source><translation>共通 KS p 値</translation></message>
</context>
<context>
    <name>DrillDownPanel</name>
    <message><source>Search…</source><translation>検索…</translation></message>
    <message><source>Export CSV…</source><translation>CSVを書き出す…</translation></message>
    <message><source>Export rows</source><translation>行を書き出す</translation></message>
    <message><source>Could not export</source><translation>書き出せませんでした</translation></message>
</context>
</TS>
