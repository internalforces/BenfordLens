# Benford Lens — Portfolio Case Study

[한국어](#한국어) · [English](#english)

## 한국어

### 한 줄 요약

Benford Lens는 민감할 수 있는 CSV/XLSX 데이터를 외부로 보내지 않고, 비전문가가 숫자 분포와
데이터 특성을 단계적으로 탐색하도록 만든 로컬 우선 데스크톱 애플리케이션입니다.

![Benford Lens 한국어 결합 분석](assets/benford-lens-overview-ko.png)

### 문제

벤포드 법칙 계산 자체는 작지만 실제 제품에는 더 큰 문제가 있습니다.

- 사용자가 어떤 열과 전처리 규칙을 선택했는지 결과와 함께 추적해야 합니다.
- 첫째 자리와 둘째 자리 결과가 서로 다른 데이터 상태에서 계산되어서는 안 됩니다.
- 통계 결과를 자동 결론처럼 표현하지 않고 데이터 특성과 함께 해석하도록 도와야 합니다.
- 원본 파일을 수정하거나 데이터를 외부 서비스로 보내지 않아야 합니다.
- 다국어 데스크톱 UI가 작은 화면과 운영체제별 글꼴에서도 사용할 수 있어야 합니다.

따라서 목표는 계산기 하나가 아니라, 입력부터 검토와 보고서까지 일관된 분석 경험을 만드는
것이었습니다.

### 역할과 범위

프로젝트 범위에는 제품 원칙 정리, 계층형 아키텍처 설계, 분석 엔진과 PySide6 UI 구현,
통계·UI 회귀 테스트, 다국어, 성능 개선, macOS/Windows 패키징 검증이 포함됩니다.

의도적으로 제외한 범위는 계정, 클라우드 저장, 온라인 업로드, 텔레메트리, 서버 분석, 자동
적용 판정, 직접 PDF 생성입니다.

### 핵심 판단 1 — 결합 분석을 하나의 스냅샷으로 만들기

첫째 자리와 둘째 자리 기능을 각각 복제하면 전처리 옵션이나 선택 열이 바뀌었을 때 두 결과가
서로 다른 상태를 설명할 위험이 있었습니다. 이를 피하기 위해 한 번의 명시적 분석 동작이 다음을
모두 담는 불변 `AnalysisSnapshot`을 만들도록 설계했습니다.

- 실제 사용된 전처리 옵션과 미리보기
- 데이터 특성 평가
- 첫째·둘째 자리 결과
- 자릿수별 MAD/카이제곱과 공유 KS 결과
- 원본 행과 자릿수의 위치별 매핑

UI, 드릴다운, HTML 보고서는 모두 이 스냅샷을 읽습니다. 그 결과 화면과 보고서가 동일한 사용자
선택을 설명하며, 입력이 바뀌면 관련 결과를 함께 무효화할 수 있습니다.

### 핵심 판단 2 — 측정된 병목 제거

10만 개의 결정론적 합성 값으로 컨트롤러 경로를 측정했을 때, 계산식보다 분석과 드릴다운에서
자릿수를 반복 추출하는 Python 작업이 병목이었습니다. 분석 엔진이 정렬된 첫째·둘째 자리 쌍을
한 번 반환하고 모든 모드가 이를 재사용하도록 바꿨습니다.

| 모드 | 변경 전 중앙값 | 변경 후 중앙값 | 개선 |
|------|---------------:|---------------:|-----:|
| 첫째 자리 | 0.284455초 | 0.195216초 | 31.4% |
| 둘째 자리 | 0.277398초 | 0.194066초 | 30.0% |
| 첫째 + 둘째 | 0.281804초 | 0.192316초 | 31.8% |

측정은 파일 입출력과 차트 렌더링을 제외한 동일 개발 환경의 비교이며, 모든 사용자 환경에 대한
성능 보장은 아닙니다. 자세한 조건은 [검증 문서](verification.md)에 정리되어 있습니다.

### 핵심 판단 3 — 번역을 넘어선 다국어 UI 안정성

영어와 6개 번역 언어를 지원하면서 단순 문자열 번역보다 실제 레이아웃 문제가 더 크게
드러났습니다.

- Windows에서 한국어·중국어·일본어 차트와 UI가 설치된 시스템 글꼴을 선택하도록 했습니다.
- 긴 러시아어 툴바가 900×700 창을 강제로 넓히던 문제를 두 줄 툴바로 해결했습니다.
- 결합 차트는 좁은 화면에서 세로, 넓은 화면에서 가로로 배치하고 최소 높이를 유지합니다.
- 차트 위 휠 입력을 상위 스크롤 영역으로 전달하면서 차트 클릭 드릴다운은 유지했습니다.
- 번역 카탈로그 키, 빈 번역, 플레이스홀더, 컴파일 리소스, 실제 언어 전환을 테스트합니다.

### 결과

- CSV/XLSX 입력부터 전처리, 분석, 드릴다운, HTML 보고서까지 한 제품 흐름으로 완성했습니다.
- 첫째·둘째·결합 분석을 동일한 상태 모델과 재사용 가능한 UI로 구현했습니다.
- 현재 기준선에서 Ruff·형식 검사·mypy와 259개 테스트가 통과합니다.
- macOS arm64 앱 후보와 Windows x64 ZIP/MSI 후보를 빌드하고 실행·설치·제거를 검증했습니다.
- 모든 데이터 처리는 로컬에 남으며 원본 입력 파일은 수정하지 않습니다.

### 회고와 남은 경계

가장 큰 교훈은 통계 기능보다 상태 일관성, 표현 방식, 운영체제별 UI, 배포 신뢰가 제품 완성도를
좌우한다는 점입니다. 공개 문서는 현재 결과, 재현 방법과 핵심 판단에 집중합니다.

v1.0.1 소스와 macOS/Windows 패키지는 공개되어 있습니다. 남은 필수 마일스톤은 macOS
Developer ID 서명·공증과 Windows의 승인된 서명 경로를 적용한 뒤 각 플랫폼의 클린 머신에서
검증하는 것입니다. Linux 패키지는 현재 제공하지 않습니다.

---

## English

### One-line summary

Benford Lens is a local-first desktop application that helps non-experts explore numeric
distributions and data characteristics in CSV/XLSX files without sending potentially sensitive
data to a remote service.

![Benford Lens combined analysis](assets/benford-lens-overview-en.png)

### Problem

The Benford formula is small; the product problem is not.

- Results must remain traceable to the user's column and preprocessing choices.
- First- and second-digit results must not describe different data states.
- Statistical output should support exploration without becoming an automatic conclusion.
- The application must not modify source files or transmit their contents.
- A multilingual desktop UI must remain usable across small windows and platform fonts.

The goal was therefore a coherent workflow from local input through review and reporting, not a
standalone calculation demo.

### Role and scope

The project scope covers product constraints, layered architecture, the analysis engine and
PySide6 UI, statistical and UI regression tests, internationalization, performance work, and
macOS/Windows packaging verification.

Accounts, cloud storage, online upload, telemetry, server-side analysis, automatic applicability
decisions, and direct PDF generation are intentionally excluded.

### Decision 1 — one snapshot for combined analysis

Duplicating the first- and second-digit pipelines would allow their preprocessing or selection
state to drift. One explicit analysis action therefore creates an immutable `AnalysisSnapshot`
containing the exact preprocessing choice and preview, suitability context, digit results,
statistics, and position-aware original-row mappings.

The UI, drill-down, and HTML report all read this snapshot. A changed input invalidates the
related output as one unit, and every visible/exported result describes the same user choice.

### Decision 2 — remove the measured bottleneck

A deterministic 100,000-value controller benchmark showed that repeated Python-level digit
extraction, not the distribution formula, dominated the path. The engine was changed to return
aligned first/second digit pairs once for reuse by analysis and drill-down.

| Mode | Before median | After median | Improvement |
|------|--------------:|-------------:|------------:|
| First digit | 0.284455 s | 0.195216 s | 31.4% |
| Second digit | 0.277398 s | 0.194066 s | 30.0% |
| First + second | 0.281804 s | 0.192316 s | 31.8% |

These are controlled comparative development measurements, not a universal performance promise.
The full method is summarized in the [verification guide](verification.md).

### Decision 3 — multilingual desktop resilience beyond translation

Supporting built-in English plus six complete translation catalogs exposed real layout and font
problems:

- installed Windows CJK fonts are selected for charts and UI;
- a two-row toolbar prevents long Russian controls from widening a 900×700 window;
- combined charts stack at compact widths and sit side by side when wide, with readable minimums;
- wheel input over charts reaches the enclosing workflow scroll area while click drill-down works;
- catalog keys, empty strings, placeholders, compiled resources, and live switching are tested.

### Outcome

- A complete CSV/XLSX → preprocessing → analysis → drill-down → HTML report workflow.
- First, second, and combined modes share one state model and reusable result UI.
- Ruff, formatting, mypy, and all 259 tests pass on the current baseline.
- macOS arm64 and Windows x64 ZIP/MSI candidates were built and smoke-tested.
- Processing remains local, and the original input file is never modified.

### Retrospective and remaining boundaries

The strongest lesson is that state consistency, careful presentation, platform UI behavior, and
distribution trust matter as much as the statistical feature itself. Public documentation now
focuses on current outcomes, reproducible checks, and durable design reasoning.

The v1.0.1 source and macOS/Windows packages are public. The remaining required milestone is to
apply Developer ID signing/notarization on macOS and an approved signed Windows distribution path,
then verify both on clean supported machines. A Linux package is not currently offered.
