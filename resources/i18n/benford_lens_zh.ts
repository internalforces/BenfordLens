<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="zh">
<context>
    <name>MainWindow</name>
    <message><source>Benford Lens</source><translation>Benford Lens</translation></message>
    <message><source>Column</source><translation>列</translation></message>
    <message><source>Type</source><translation>类型</translation></message>
    <message><source>Open File…</source><translation>打开文件…</translation></message>
    <message><source>Analyze</source><translation>分析</translation></message>
    <message><source>Export Report…</source><translation>导出报告…</translation></message>
    <message><source>Open a CSV or Excel file to begin.</source><translation>打开一个 CSV 或 Excel 文件以开始。</translation></message>
    <message><source>Open data file</source><translation>打开数据文件</translation></message>
    <message><source>Select sheet</source><translation>选择工作表</translation></message>
    <message><source>Sheet:</source><translation>工作表:</translation></message>
    <message><source>Could not open file</source><translation>无法打开文件</translation></message>
    <message><source>Select a column, then click Analyze.</source><translation>选择一列,然后点击"分析"。</translation></message>
    <message><source>Cannot select column</source><translation>无法选择列</translation></message>
    <message><source>Cannot analyze</source><translation>无法分析</translation></message>
    <message><source>Cannot show rows</source><translation>无法显示行</translation></message>
    <message><source>Export report</source><translation>导出报告</translation></message>
    <message><source>Could not export report</source><translation>无法导出报告</translation></message>
    <message><source>No valid numeric values were found in the selected column.</source><translation>在所选列中未找到有效的数值。</translation></message>
    <message><source>Only {sample_size} valid numeric value(s) were found, which is too few for a meaningful comparison to the expected Benford distribution. Try a column with more data.</source><translation>仅找到 {sample_size} 个有效数值，不足以与预期的本福特分布进行有意义的比较。请尝试数据更多的列。</translation></message>
    <message><source>The overall distribution is close to the expected Benford distribution. This result alone cannot be used to judge data errors or manipulation.</source><translation>整体分布接近预期的本福特分布。仅凭此结果无法判断数据是否存在错误或被人为改动。</translation></message>
    <message><source>The overall distribution differs somewhat from the expected Benford distribution. This result alone cannot be used to judge data errors or manipulation; further review may be warranted.</source><translation>整体分布与预期的本福特分布存在一定差异。仅凭此结果无法判断数据是否存在错误或被人为改动；可能需要进一步审查。</translation></message>
</context>
<context>
    <name>PreprocessingPanel</name>
    <message><source>Negative values</source><translation>负值</translation></message>
    <message><source>Zero values</source><translation>零值</translation></message>
    <message><source>Decimal values</source><translation>小数值</translation></message>
    <message><source>Blank values</source><translation>空值</translation></message>
    <message><source>Duplicate values</source><translation>重复值</translation></message>
    <message><source>Text-to-number</source><translation>文本转数字</translation></message>
    <message><source>Keep</source><translation>保留</translation></message>
    <message><source>Convert to absolute value</source><translation>转换为绝对值</translation></message>
    <message><source>Exclude</source><translation>排除</translation></message>
    <message><source>Use as-is</source><translation>按原样使用</translation></message>
    <message><source>Round</source><translation>四舍五入</translation></message>
    <message><source>Truncate</source><translation>截断</translation></message>
    <message><source>Auto-convert</source><translation>自动转换</translation></message>
    <message><source>Do not convert</source><translation>不转换</translation></message>
    <message><source>Preview</source><translation>预览</translation></message>
    <message><source>Before</source><translation>之前</translation></message>
    <message><source>After</source><translation>之后</translation></message>
    <message><source>values (excluded: {blank} blank, {non_numeric} non-numeric, {negative} negative, {zero} zero)</source><translation>个值(已排除:空值 {blank} 个、非数字 {non_numeric} 个、负值 {negative} 个、零值 {zero} 个)</translation></message>
</context>
<context>
    <name>SuitabilityPanel</name>
    <message><source>🟢 Good</source><translation>🟢 良好</translation></message>
    <message><source>🟡 Caution</source><translation>🟡 注意</translation></message>
    <message><source>🔴 Difficult to determine</source><translation>🔴 难以判断</translation></message>
    <message><source>No caveats found.</source><translation>未发现需要注意的问题。</translation></message>
    <message><source>These are data characteristics, not a determination of whether Benford's Law applies — that judgment is yours to make.</source><translation>这些只是数据特征,并非对本福特定律是否适用的判定——该判断由您自行做出。</translation></message>
    <message><source>Sample count</source><translation>样本数量</translation></message>
    <message><source>Minimum value</source><translation>最小值</translation></message>
    <message><source>Maximum value</source><translation>最大值</translation></message>
    <message><source>Magnitude range</source><translation>数量级范围</translation></message>
    <message><source>Distinct values</source><translation>不同值数量</translation></message>
    <message><source>Duplicate rate</source><translation>重复率</translation></message>
    <message><source>Zero rate</source><translation>零值比例</translation></message>
    <message><source>Negative rate</source><translation>负值比例</translation></message>
    <message><source>Missing rate</source><translation>缺失比例</translation></message>
    <message><source>Only {sample_count} valid value(s) — below the {minimum}-value floor for a meaningful comparison.</source><translation>仅有 {sample_count} 个有效值，低于进行有意义比较所需的 {minimum} 个下限。</translation></message>
    <message><source>{sample_count} valid values is a workable but modest sample size.</source><translation>{sample_count} 个有效值可以使用，但样本量偏小。</translation></message>
    <message><source>Values span only a single order of magnitude.</source><translation>数值仅分布在单一数量级内。</translation></message>
    <message><source>Values span {digit_range} orders of magnitude.</source><translation>数值分布在 {digit_range} 个数量级内。</translation></message>
    <message><source>Very few distinct values relative to the sample size.</source><translation>相对于样本量，不同数值的数量非常少。</translation></message>
    <message><source>Values repeat somewhat more than expected for this sample size.</source><translation>相对于样本量，数值重复得略多。</translation></message>
    <message><source>{zero_rate:.0%} of the source values were zero.</source><translation>源数据中有 {zero_rate:.0%} 的值为零。</translation></message>
    <message><source>{negative_rate:.0%} of the source values were negative — check whether the negative-value preprocessing option fits this data.</source><translation>源数据中有 {negative_rate:.0%} 的值为负数——请确认负值预处理选项是否适合此数据。</translation></message>
    <message><source>{missing_rate:.0%} of the source values were blank.</source><translation>源数据中有 {missing_rate:.0%} 的值为空。</translation></message>
</context>
<context>
    <name>DrillDownPanel</name>
    <message><source>Search…</source><translation>搜索…</translation></message>
    <message><source>Export CSV…</source><translation>导出 CSV…</translation></message>
    <message><source>Export rows</source><translation>导出行</translation></message>
    <message><source>Could not export</source><translation>无法导出</translation></message>
</context>
</TS>
