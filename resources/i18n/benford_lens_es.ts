<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="es">
<context>
    <name>MainWindow</name>
    <message><source>Benford Lens</source><translation>Benford Lens</translation></message>
    <message><source>Column</source><translation>Columna</translation></message>
    <message><source>Type</source><translation>Tipo</translation></message>
    <message><source>Open File…</source><translation>Abrir archivo…</translation></message>
    <message><source>Analyze</source><translation>Analizar</translation></message>
    <message><source>Export Report…</source><translation>Exportar informe…</translation></message>
    <message><source>Open a CSV or Excel file to begin.</source><translation>Abra un archivo CSV o Excel para comenzar.</translation></message>
    <message><source>Open data file</source><translation>Abrir archivo de datos</translation></message>
    <message><source>Select sheet</source><translation>Seleccionar hoja</translation></message>
    <message><source>Sheet:</source><translation>Hoja:</translation></message>
    <message><source>Could not open file</source><translation>No se pudo abrir el archivo</translation></message>
    <message><source>Select a column, then click Analyze.</source><translation>Seleccione una columna y haga clic en Analizar.</translation></message>
    <message><source>Cannot select column</source><translation>No se puede seleccionar la columna</translation></message>
    <message><source>Cannot analyze</source><translation>No se puede analizar</translation></message>
    <message><source>Cannot show rows</source><translation>No se pueden mostrar las filas</translation></message>
    <message><source>Export report</source><translation>Exportar informe</translation></message>
    <message><source>Could not export report</source><translation>No se pudo exportar el informe</translation></message>
    <message><source>No valid numeric values were found in the selected column.</source><translation>No se encontraron valores numéricos válidos en la columna seleccionada.</translation></message>
    <message><source>Only {sample_size} valid numeric value(s) were found, which is too few for a meaningful comparison to the expected Benford distribution. Try a column with more data.</source><translation>Solo se encontraron {sample_size} valores numéricos válidos, una cantidad insuficiente para realizar una comparación significativa con la distribución de Benford esperada. Pruebe con una columna que contenga más datos.</translation></message>
    <message><source>The overall distribution is close to the expected Benford distribution. Interpret this comparison together with the characteristics of the data.</source><translation>La distribución general se aproxima a la distribución de Benford esperada. Interprete esta comparación junto con las características de los datos.</translation></message>
    <message><source>The overall distribution differs somewhat from the expected Benford distribution. Further review of the data characteristics may be warranted.</source><translation>La distribución general difiere en cierta medida de la distribución de Benford esperada. Puede ser conveniente revisar más a fondo las características de los datos.</translation></message>
    <message><source>First digit</source><translation>Primer dígito</translation></message>
    <message><source>Second digit</source><translation>Segundo dígito</translation></message>
    <message><source>First + second</source><translation>Primer + segundo dígito</translation></message>
    <message><source>Observed</source><translation>Observado</translation></message>
    <message><source>Expected (Benford)</source><translation>Esperado (Benford)</translation></message>
    <message><source>Proportion (%)</source><translation>Proporción (%)</translation></message>
    <message><source>{position} analysis</source><translation>Análisis: {position}</translation></message>
</context>
<context>
    <name>PreprocessingPanel</name>
    <message><source>Negative values</source><translation>Valores negativos</translation></message>
    <message><source>Zero values</source><translation>Valores cero</translation></message>
    <message><source>Decimal values</source><translation>Valores decimales</translation></message>
    <message><source>Blank values</source><translation>Valores en blanco</translation></message>
    <message><source>Duplicate values</source><translation>Valores duplicados</translation></message>
    <message><source>Text-to-number</source><translation>Texto a número</translation></message>
    <message><source>Keep</source><translation>Conservar</translation></message>
    <message><source>Convert to absolute value</source><translation>Convertir a valor absoluto</translation></message>
    <message><source>Exclude</source><translation>Excluir</translation></message>
    <message><source>Use as-is</source><translation>Usar sin cambios</translation></message>
    <message><source>Round</source><translation>Redondear</translation></message>
    <message><source>Truncate</source><translation>Truncar</translation></message>
    <message><source>Auto-convert</source><translation>Conversión automática</translation></message>
    <message><source>Do not convert</source><translation>No convertir</translation></message>
    <message><source>Preview</source><translation>Vista previa</translation></message>
    <message><source>Before</source><translation>Antes</translation></message>
    <message><source>After</source><translation>Después</translation></message>
    <message><source>values (excluded: {blank} blank, {non_numeric} non-numeric, {negative} negative, {zero} zero)</source><translation>valores (excluidos: {blank} en blanco, {non_numeric} no numéricos, {negative} negativos, {zero} cero)</translation></message>
</context>
<context>
    <name>SuitabilityPanel</name>
    <message><source>🟢 Good</source><translation>🟢 Bien</translation></message>
    <message><source>🟡 Caution</source><translation>🟡 Precaución</translation></message>
    <message><source>🔴 Difficult to determine</source><translation>🔴 Difícil de determinar</translation></message>
    <message><source>No caveats found.</source><translation>No se detectaron observaciones.</translation></message>
    <message><source>These are data characteristics, not a determination of whether Benford's Law applies — that judgment is yours to make.</source><translation>Estas son características de los datos, no una determinación de si se aplica la ley de Benford; esa valoración le corresponde a usted.</translation></message>
    <message><source>Sample count</source><translation>Recuento de muestras</translation></message>
    <message><source>Minimum value</source><translation>Valor mínimo</translation></message>
    <message><source>Maximum value</source><translation>Valor máximo</translation></message>
    <message><source>Magnitude range</source><translation>Rango de magnitudes</translation></message>
    <message><source>Distinct values</source><translation>Valores distintos</translation></message>
    <message><source>Duplicate rate</source><translation>Tasa de duplicados</translation></message>
    <message><source>Zero rate</source><translation>Tasa de ceros</translation></message>
    <message><source>Negative rate</source><translation>Tasa de negativos</translation></message>
    <message><source>Missing rate</source><translation>Tasa de ausentes</translation></message>
    <message><source>Only {sample_count} valid value(s) — below the {minimum}-value floor for a meaningful comparison.</source><translation>Solo hay {sample_count} valores válidos, por debajo del mínimo de {minimum} valores necesario para una comparación significativa.</translation></message>
    <message><source>{sample_count} valid values is a workable but modest sample size.</source><translation>{sample_count} valores válidos forman una muestra utilizable, aunque moderada.</translation></message>
    <message><source>Values span only a single order of magnitude.</source><translation>Los valores abarcan solo un orden de magnitud.</translation></message>
    <message><source>Values span {digit_range} orders of magnitude.</source><translation>Los valores abarcan {digit_range} órdenes de magnitud.</translation></message>
    <message><source>Very few distinct values relative to the sample size.</source><translation>Hay muy pocos valores distintos en relación con el tamaño de la muestra.</translation></message>
    <message><source>Values repeat somewhat more than expected for this sample size.</source><translation>Los valores se repiten algo más de lo esperado para este tamaño de muestra.</translation></message>
    <message><source>{zero_rate:.0%} of the source values were zero.</source><translation>El {zero_rate:.0%} de los valores de origen eran cero.</translation></message>
    <message><source>{negative_rate:.0%} of the source values were negative — check whether the negative-value preprocessing option fits this data.</source><translation>El {negative_rate:.0%} de los valores de origen eran negativos; compruebe si la opción de preprocesamiento de valores negativos se ajusta a estos datos.</translation></message>
    <message><source>{missing_rate:.0%} of the source values were blank.</source><translation>El {missing_rate:.0%} de los valores de origen estaban en blanco.</translation></message>
</context>
<context>
    <name>ExpertStatisticsPanel</name>
    <message><source>Show Details</source><translation>Mostrar detalles</translation></message>
    <message><source>Hide Details</source><translation>Ocultar detalles</translation></message>
    <message><source>Sample size</source><translation>Tamaño de la muestra</translation></message>
    <message><source>Mean absolute deviation (MAD)</source><translation>Desviación absoluta media (MAD)</translation></message>
    <message><source>Chi-square statistic</source><translation>Estadístico chi-cuadrado</translation></message>
    <message><source>Chi-square p-value</source><translation>Valor p de chi-cuadrado</translation></message>
    <message><source>KS statistic</source><translation>Estadístico KS</translation></message>
    <message><source>KS p-value</source><translation>Valor p de KS</translation></message>
    <message><source>Reference statistics only. Interpret them in light of the data and sample characteristics. KS compares base-10 log mantissas with a uniform distribution.</source><translation>Estadísticas de referencia únicamente. Interprételas teniendo en cuenta los datos y las características de la muestra. KS compara las mantisas de los logaritmos en base 10 con una distribución uniforme.</translation></message>
    <message><source>First-digit sample size</source><translation>Tamaño de la muestra del primer dígito</translation></message>
    <message><source>First-digit mean absolute deviation (MAD)</source><translation>Desviación absoluta media del primer dígito (MAD)</translation></message>
    <message><source>First-digit Chi-square statistic</source><translation>Estadístico chi-cuadrado del primer dígito</translation></message>
    <message><source>First-digit Chi-square p-value</source><translation>Valor p de chi-cuadrado del primer dígito</translation></message>
    <message><source>Second-digit sample size</source><translation>Tamaño de la muestra del segundo dígito</translation></message>
    <message><source>Second-digit mean absolute deviation (MAD)</source><translation>Desviación absoluta media del segundo dígito (MAD)</translation></message>
    <message><source>Second-digit Chi-square statistic</source><translation>Estadístico chi-cuadrado del segundo dígito</translation></message>
    <message><source>Second-digit Chi-square p-value</source><translation>Valor p de chi-cuadrado del segundo dígito</translation></message>
    <message><source>Shared KS sample size</source><translation>Tamaño de la muestra KS común</translation></message>
    <message><source>Shared KS statistic</source><translation>Estadístico KS común</translation></message>
    <message><source>Shared KS p-value</source><translation>Valor p de KS común</translation></message>
</context>
<context>
    <name>DrillDownPanel</name>
    <message><source>Search…</source><translation>Buscar…</translation></message>
    <message><source>Export CSV…</source><translation>Exportar CSV…</translation></message>
    <message><source>Export rows</source><translation>Exportar filas</translation></message>
    <message><source>Could not export</source><translation>No se pudo exportar</translation></message>
</context>
</TS>
