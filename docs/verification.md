# Benford Lens — Verification

[한국어](#한국어) · [English](#english)

## 한국어

### 현재 품질 기준선

2026-08-09 `origin/main` PR #13 병합 커밋을 기준으로 다음을 다시 실행했습니다.

| 검사 | 결과 |
|------|------|
| Ruff lint | 통과 |
| Ruff format | 46개 기존 코드 파일 통과; 포트폴리오 자산 생성 스크립트도 통과 |
| mypy | 22개 소스 파일, 오류 없음 |
| pytest | 241 passed |
| GitHub Actions | 동일 병합 커밋에서 성공 |

### 테스트 범위

| 영역 | 대표 검증 |
|------|-----------|
| 자릿수 분석 | 첫째·둘째 자리 경계, 기대 비율, 결합 결과, 기존 첫째 자리 API 호환성 |
| 전처리 | 음수·0·소수·빈 값·중복·문자형 숫자, 무한대, 미리보기 카운트 |
| 데이터 특성 | 표본 크기, 자릿수 범위, 다양성, 중복/0/음수/결측 비율, 중립적 안내 |
| 참고 통계 | MAD, 카이제곱, 로그 가수 KS, 작은 표본과 상수 표본 경계 |
| 컨트롤러 | 명시적 선택, 단일 전처리, 불변 스냅샷, 정확한 무효화, 위치별 행 매핑 |
| UI | 파일/시트/열 선택, 세 분석 모드, 반응형 레이아웃, 휠 스크롤, 드릴다운 |
| 보고서 | 첫째·둘째·결합 HTML, 스냅샷과 UI 문구 일치, HTML 이스케이프 |
| 국제화 | 6개 카탈로그 동등성, 빈 번역, 플레이스홀더, `.qm`, 실제 언어 전환과 CJK 글꼴 |

Qt UI 테스트는 `QT_QPA_PLATFORM=offscreen`으로 실행해 창 표시가 없는 CI에서도 동작합니다.

### 재현 명령

```bash
uv sync --locked --group dev
uv run ruff check .
uv run ruff format --check src/ tests/ scripts/
uv run mypy src/
QT_QPA_PLATFORM=offscreen uv run pytest
```

macOS에서 가상환경 변경 뒤 네이티브 라이브러리 로딩 문제가 발생하면
`memory/known-issues.md`의 ENV-001 우회 절차를 확인합니다.

### 성능 검증

10만 개의 결정론적 합성 숫자를 사용해 파일 I/O, 차트, 보고서를 제외한 컨트롤러 분석 경로를
측정했습니다. 모드별 워밍업 후 5회 실행 중앙값을 비교했습니다.

| 모드 | 변경 전 | 변경 후 | 개선 |
|------|--------:|--------:|-----:|
| 첫째 자리 | 0.284455초 | 0.195216초 | 31.4% |
| 둘째 자리 | 0.277398초 | 0.194066초 | 30.0% |
| 첫째 + 둘째 | 0.281804초 | 0.192316초 | 31.8% |

개선 내용은 분석·드릴다운이 반복하던 Python 수준 자릿수 추출을 한 번으로 합친 것입니다.
전체 조건은 [성능 보고서](../reports/performance-2026-08-06-m3.md)에 있습니다.

### 커버리지 경계

표준 라이브러리 `trace`로 측정한 M3 시점 기록은 1,661개 실행 가능 소스 줄 중 1,578개 실행,
95.00%였습니다. 이후 테스트가 229개에서 241개로 늘었지만 같은 방식의 현재 측정을 다시
기록하지 않았고 CI도 커버리지를 강제하지 않습니다. 따라서 95.00%는 현재 수치가 아니라
[M3 이력](../reports/test-coverage-2026-08-06-m3.md)으로만 제시합니다.

### 패키징 검증

- **macOS arm64:** 번들 버전, 아키텍처, 6개 번역 카탈로그, ad-hoc 서명 무결성, 헤드리스
  실행, ZIP 재추출을 확인했습니다. 공개 배포에는 Developer ID 서명·공증이 남았습니다.
- **Windows x64 ZIP:** PE 아키텍처, 아이콘, 번역, 폴더/재추출 ZIP 실행, 해시 일치를
  확인했습니다. 실행 파일은 아직 Authenticode 서명되지 않았습니다.
- **Windows x64 MSI:** 1,194개 파일, 사용자 범위 비승격 설치, 시작 메뉴 바로가기,
  8초 실행, 완전 제거를 확인했습니다. MSI도 아직 서명되지 않았습니다.
- **Linux:** 설정 파일만 존재하며 대상 환경 검증은 아직입니다.

체크섬과 상세 절차는 `reports/release-2026-08-07-macos.md`,
`reports/release-2026-08-08-windows.md`, `reports/release-2026-08-08-windows-msi.md`에
보존합니다.

### 문서 시각 자료 검증

`scripts/generate_portfolio_assets.py`는 결정론적 합성 거래 데이터를 임시 디렉터리에 만들고
실제 PySide6 앱을 offscreen으로 구동합니다. 생성 결과는 영어·한국어 PNG 3개와 5프레임
960×640 GIF이며 실제 사용자 데이터를 읽지 않습니다.

```bash
QT_QPA_PLATFORM=offscreen uv run python scripts/generate_portfolio_assets.py
```

---

## English

### Current quality baseline

The following checks were rerun on 2026-08-09 against the `origin/main` PR #13 merge baseline.

| Check | Result |
|-------|--------|
| Ruff lint | Passed |
| Ruff format | 46 existing code files passed; the portfolio asset generator also passed |
| mypy | 22 source files, no issues |
| pytest | 241 passed |
| GitHub Actions | Successful on the same merge commit |

### Test matrix

| Area | Representative coverage |
|------|-------------------------|
| Digit analysis | First/second boundaries, expected proportions, combined results, first-digit API compatibility |
| Preprocessing | Negative, zero, decimal, blank, duplicate, text numbers, infinity, preview counts |
| Data context | Sample, magnitude range, diversity, duplicate/zero/negative/missing rates, neutral guidance |
| Statistics | MAD, Chi-square, log-mantissa KS, small and constant sample boundaries |
| Controller | Explicit selection, one preprocessing pass, frozen snapshot, invalidation, position mappings |
| UI | File/sheet/column selection, all modes, responsive layout, wheel scrolling, drill-down |
| Report | First/second/combined HTML, snapshot/UI copy parity, escaping |
| i18n | Six-catalog parity, empty text, placeholders, `.qm`, live switching, CJK fonts |

Qt UI tests use `QT_QPA_PLATFORM=offscreen` so they can run without a display in CI.

### Reproduce

```bash
uv sync --locked --group dev
uv run ruff check .
uv run ruff format --check src/ tests/ scripts/
uv run mypy src/
QT_QPA_PLATFORM=offscreen uv run pytest
```

If native packages fail to load on macOS after environment changes, see ENV-001 in
`memory/known-issues.md` for the documented local workaround.

### Performance evidence

A deterministic 100,000-value workload measured controller analysis only, excluding file I/O,
charts, and reports. Each mode was warmed up and compared by the median of five runs.

| Mode | Before | After | Improvement |
|------|-------:|------:|------------:|
| First | 0.284455 s | 0.195216 s | 31.4% |
| Second | 0.277398 s | 0.194066 s | 30.0% |
| First + second | 0.281804 s | 0.192316 s | 31.8% |

The change removed repeated Python-level digit extraction across analysis and drill-down. See the
[performance report](../reports/performance-2026-08-06-m3.md) for the full conditions.

### Coverage boundary

The M3 historical trace measured 1,578 of 1,661 executable source lines, or 95.00%. The suite has
since grown from 229 to 241 tests, but an equivalent current measurement has not been recorded and
CI does not enforce coverage. The number is therefore presented only as
[M3 history](../reports/test-coverage-2026-08-06-m3.md), not current coverage.

### Packaging verification

- **macOS arm64:** bundle metadata, architecture, six catalogs, ad-hoc signature integrity,
  headless startup, and ZIP re-extraction passed. Developer ID signing/notarization remain.
- **Windows x64 ZIP:** PE architecture, icon, translations, folder/extracted-ZIP startup, and
  hash parity passed. The executable is not Authenticode-signed.
- **Windows x64 MSI:** 1,194 files, non-elevated per-user install, Start menu shortcut, 8-second
  startup, and complete removal passed. The MSI is not signed.
- **Linux:** configuration exists without target-platform verification.

Checksums and detailed procedures remain in the dated release reports under `reports/`.

### Visual asset verification

`scripts/generate_portfolio_assets.py` creates deterministic fictional transaction data in a
temporary directory and drives the real PySide6 application offscreen. It produces three English/
Korean PNGs and a five-frame 960×640 GIF without reading user data.

```bash
QT_QPA_PLATFORM=offscreen uv run python scripts/generate_portfolio_assets.py
```
