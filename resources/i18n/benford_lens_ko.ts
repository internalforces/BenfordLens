<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="ko">
<context>
    <name>MainWindow</name>
    <message><source>Benford Lens</source><translation>Benford Lens</translation></message>
    <message><source>Column</source><translation>열</translation></message>
    <message><source>Type</source><translation>유형</translation></message>
    <message><source>Open File…</source><translation>파일 열기…</translation></message>
    <message><source>Analyze</source><translation>분석</translation></message>
    <message><source>Export Report…</source><translation>보고서 내보내기…</translation></message>
    <message><source>Third-party notices</source><translation>타사 소프트웨어 고지</translation></message>
    <message><source>The third-party notices file is unavailable.</source><translation>타사 소프트웨어 고지 파일을 사용할 수 없습니다.</translation></message>
    <message><source>Open a CSV or Excel file to begin.</source><translation>시작하려면 CSV 또는 Excel 파일을 여세요.</translation></message>
    <message><source>Open data file</source><translation>데이터 파일 열기</translation></message>
    <message><source>Select sheet</source><translation>시트 선택</translation></message>
    <message><source>Sheet:</source><translation>시트:</translation></message>
    <message><source>Could not open file</source><translation>파일을 열 수 없습니다</translation></message>
    <message><source>Select a column, then click Analyze.</source><translation>열을 선택한 다음 분석을 클릭하세요.</translation></message>
    <message><source>Cannot select column</source><translation>열을 선택할 수 없습니다</translation></message>
    <message><source>Cannot analyze</source><translation>분석할 수 없습니다</translation></message>
    <message><source>Cannot show rows</source><translation>행을 표시할 수 없습니다</translation></message>
    <message><source>Export report</source><translation>보고서 내보내기</translation></message>
    <message><source>Could not export report</source><translation>보고서를 내보낼 수 없습니다</translation></message>
    <message><source>No valid numeric values were found in the selected column.</source><translation>선택한 열에서 유효한 숫자 값을 찾지 못했습니다.</translation></message>
    <message><source>Only {sample_size} valid numeric value(s) were found, which is too few for a meaningful comparison to the expected Benford distribution. Try a column with more data.</source><translation>유효한 숫자 값이 {sample_size}개뿐이어서 기대되는 벤포드 분포와 의미 있게 비교하기에는 너무 적습니다. 데이터가 더 많은 열을 사용해 보세요.</translation></message>
    <message><source>The overall distribution is close to the expected Benford distribution. Interpret this comparison together with the characteristics of the data.</source><translation>전체 분포가 기대되는 벤포드 분포에 가깝습니다. 이 비교 결과를 데이터의 특성과 함께 해석하세요.</translation></message>
    <message><source>The overall distribution differs somewhat from the expected Benford distribution. Further review of the data characteristics may be warranted.</source><translation>전체 분포가 기대되는 벤포드 분포와 다소 차이가 있습니다. 데이터 특성에 대한 추가 검토가 필요할 수 있습니다.</translation></message>
    <message><source>First digit</source><translation>첫째 자리</translation></message>
    <message><source>Second digit</source><translation>둘째 자리</translation></message>
    <message><source>First + second</source><translation>첫째 + 둘째 자리</translation></message>
    <message><source>Observed</source><translation>관측값</translation></message>
    <message><source>Expected (Benford)</source><translation>기대값 (벤포드)</translation></message>
    <message><source>Proportion (%)</source><translation>비율 (%)</translation></message>
    <message><source>{position} analysis</source><translation>{position} 분석</translation></message>
</context>
<context>
    <name>PreprocessingPanel</name>
    <message><source>Negative values</source><translation>음수 값</translation></message>
    <message><source>Zero values</source><translation>0 값</translation></message>
    <message><source>Decimal values</source><translation>소수 값</translation></message>
    <message><source>Blank values</source><translation>빈 값</translation></message>
    <message><source>Duplicate values</source><translation>중복 값</translation></message>
    <message><source>Text-to-number</source><translation>문자열→숫자 변환</translation></message>
    <message><source>Keep</source><translation>유지</translation></message>
    <message><source>Convert to absolute value</source><translation>절대값으로 변환</translation></message>
    <message><source>Exclude</source><translation>제외</translation></message>
    <message><source>Use as-is</source><translation>그대로 사용</translation></message>
    <message><source>Round</source><translation>반올림</translation></message>
    <message><source>Truncate</source><translation>자르기</translation></message>
    <message><source>Auto-convert</source><translation>자동 변환</translation></message>
    <message><source>Do not convert</source><translation>변환 안 함</translation></message>
    <message><source>Preview</source><translation>미리보기</translation></message>
    <message><source>Before</source><translation>이전</translation></message>
    <message><source>After</source><translation>이후</translation></message>
    <message><source>values (excluded: {blank} blank, {non_numeric} non-numeric, {negative} negative, {zero} zero)</source><translation>개의 값 (제외됨: 빈값 {blank}개, 비숫자 {non_numeric}개, 음수 {negative}개, 0 {zero}개)</translation></message>
</context>
<context>
    <name>SuitabilityPanel</name>
    <message><source>🟢 Good</source><translation>🟢 양호</translation></message>
    <message><source>🟡 Caution</source><translation>🟡 주의</translation></message>
    <message><source>🔴 Difficult to determine</source><translation>🔴 판단 어려움</translation></message>
    <message><source>No caveats found.</source><translation>특이사항 없음.</translation></message>
    <message><source>These are data characteristics, not a determination of whether Benford's Law applies — that judgment is yours to make.</source><translation>이는 데이터의 특성일 뿐이며 벤포드 법칙의 적용 여부를 판단한 것이 아닙니다. 그 판단은 사용자의 몫입니다.</translation></message>
    <message><source>Sample count</source><translation>표본 개수</translation></message>
    <message><source>Minimum value</source><translation>최솟값</translation></message>
    <message><source>Maximum value</source><translation>최댓값</translation></message>
    <message><source>Magnitude range</source><translation>자릿수 범위</translation></message>
    <message><source>Distinct values</source><translation>고유 값 수</translation></message>
    <message><source>Duplicate rate</source><translation>중복 비율</translation></message>
    <message><source>Zero rate</source><translation>0 비율</translation></message>
    <message><source>Negative rate</source><translation>음수 비율</translation></message>
    <message><source>Missing rate</source><translation>결측 비율</translation></message>
    <message><source>Only {sample_count} valid value(s) — below the {minimum}-value floor for a meaningful comparison.</source><translation>유효한 값이 {sample_count}개뿐이며, 의미 있는 비교를 위한 최소 기준 {minimum}개에 미치지 못합니다.</translation></message>
    <message><source>{sample_count} valid values is a workable but modest sample size.</source><translation>유효한 값 {sample_count}개는 분석에 사용할 수 있지만 다소 적은 표본 크기입니다.</translation></message>
    <message><source>Values span only a single order of magnitude.</source><translation>값이 하나의 자릿수 범위에만 분포합니다.</translation></message>
    <message><source>Values span {digit_range} orders of magnitude.</source><translation>값이 {digit_range}개의 자릿수 범위에 분포합니다.</translation></message>
    <message><source>Very few distinct values relative to the sample size.</source><translation>표본 크기에 비해 서로 다른 값의 수가 매우 적습니다.</translation></message>
    <message><source>Values repeat somewhat more than expected for this sample size.</source><translation>표본 크기에 비해 값의 반복이 다소 많습니다.</translation></message>
    <message><source>{zero_rate:.0%} of the source values were zero.</source><translation>원본 값의 {zero_rate:.0%}가 0이었습니다.</translation></message>
    <message><source>{negative_rate:.0%} of the source values were negative — check whether the negative-value preprocessing option fits this data.</source><translation>원본 값의 {negative_rate:.0%}가 음수였습니다. 음수 값 전처리 옵션이 이 데이터에 적합한지 확인하세요.</translation></message>
    <message><source>{missing_rate:.0%} of the source values were blank.</source><translation>원본 값의 {missing_rate:.0%}가 비어 있었습니다.</translation></message>
</context>
<context>
    <name>ExpertStatisticsPanel</name>
    <message><source>Show Details</source><translation>상세 통계 보기</translation></message>
    <message><source>Hide Details</source><translation>상세 통계 숨기기</translation></message>
    <message><source>Sample size</source><translation>표본 크기</translation></message>
    <message><source>Mean absolute deviation (MAD)</source><translation>평균 절대 편차 (MAD)</translation></message>
    <message><source>Chi-square statistic</source><translation>카이제곱 통계량</translation></message>
    <message><source>Chi-square p-value</source><translation>카이제곱 p-값</translation></message>
    <message><source>KS statistic</source><translation>KS 통계량</translation></message>
    <message><source>KS p-value</source><translation>KS p-값</translation></message>
    <message><source>Reference statistics only. Interpret them in light of the data and sample characteristics. KS compares base-10 log mantissas with a uniform distribution.</source><translation>참고용 통계입니다. 데이터와 표본의 특성을 함께 고려해 해석하세요. KS는 밑이 10인 로그의 소수 부분을 균등분포와 비교합니다.</translation></message>
    <message><source>First-digit sample size</source><translation>첫째 자리 표본 크기</translation></message>
    <message><source>First-digit mean absolute deviation (MAD)</source><translation>첫째 자리 평균 절대 편차 (MAD)</translation></message>
    <message><source>First-digit Chi-square statistic</source><translation>첫째 자리 카이제곱 통계량</translation></message>
    <message><source>First-digit Chi-square p-value</source><translation>첫째 자리 카이제곱 p-값</translation></message>
    <message><source>Second-digit sample size</source><translation>둘째 자리 표본 크기</translation></message>
    <message><source>Second-digit mean absolute deviation (MAD)</source><translation>둘째 자리 평균 절대 편차 (MAD)</translation></message>
    <message><source>Second-digit Chi-square statistic</source><translation>둘째 자리 카이제곱 통계량</translation></message>
    <message><source>Second-digit Chi-square p-value</source><translation>둘째 자리 카이제곱 p-값</translation></message>
    <message><source>Shared KS sample size</source><translation>공통 KS 표본 크기</translation></message>
    <message><source>Shared KS statistic</source><translation>공통 KS 통계량</translation></message>
    <message><source>Shared KS p-value</source><translation>공통 KS p-값</translation></message>
</context>
<context>
    <name>DrillDownPanel</name>
    <message><source>Search…</source><translation>검색…</translation></message>
    <message><source>Export CSV…</source><translation>CSV 내보내기…</translation></message>
    <message><source>Export rows</source><translation>행 내보내기</translation></message>
    <message><source>Could not export</source><translation>내보낼 수 없습니다</translation></message>
</context>
</TS>
