# Benford Lens — Verification

[한국어](#한국어) · [English](#english)

## 한국어

### 현재 품질 기준선

v1.0.1 이후 현재 소스 기준선에서 다음 검사를 실행합니다.

| 검사 | 현재 결과 |
|------|-----------|
| Ruff lint / format | 통과 |
| mypy | 22개 소스 파일, 오류 없음 |
| pytest | 259개 테스트 통과 |
| GitHub Actions | `main`과 pull request에서 lint·타입·테스트 검사 |

테스트는 자릿수 계산, 전처리, 데이터 특성, 참고 통계, 컨트롤러 상태, UI 흐름,
HTML 보고서, 번역 카탈로그와 운영체제별 레이아웃을 포함합니다. Qt UI 테스트는
`QT_QPA_PLATFORM=offscreen`으로 실행할 수 있습니다.

### 재현 명령

```bash
uv sync --locked --group dev
uv run ruff check .
uv run ruff format --check src/ tests/ scripts/
uv run mypy src/
QT_QPA_PLATFORM=offscreen uv run pytest
```

macOS에서 가상환경 변경 뒤 NumPy, Pandas 또는 PySide6 네이티브 모듈 로딩 중 Python이
중단되면 가상환경의 숨김 플래그를 제거한 뒤 다시 실행합니다.

```bash
chflags -R nohidden .venv
```

이 우회책은 개발 가상환경에만 적용되며 애플리케이션 데이터에는 영향을 주지 않습니다.

### 성능 검증

결정론적 합성 값 100,000개를 사용해 파일 입출력, 차트, 보고서를 제외한 컨트롤러 분석
경로를 측정했습니다. 각 모드는 워밍업 후 5회 실행 중앙값을 비교했습니다.

| 모드 | 변경 전 | 변경 후 | 개선 |
|------|--------:|--------:|-----:|
| 첫째 자리 | 0.284455초 | 0.195216초 | 31.4% |
| 둘째 자리 | 0.277398초 | 0.194066초 | 30.0% |
| 첫째 + 둘째 | 0.281804초 | 0.192316초 | 31.8% |

개선 내용은 분석과 드릴다운에서 반복하던 Python 수준 자릿수 추출을 한 번으로 합친
것입니다. 수치는 동일 개발 환경에서 얻은 비교 측정이며 모든 장치의 성능을 보장하지 않습니다.

M3 시점의 표준 라이브러리 `trace` 측정은 실행 가능 소스 1,661줄 중 1,578줄(95.00%)이었습니다.
이 값은 현재 커버리지가 아니라 당시 기준선의 이력입니다. CI는 현재 커버리지 비율을
강제하지 않습니다.

### 패키징 경계

- **macOS Apple Silicon:** 릴리스 워크플로가 아키텍처, 메타데이터, 번역, 고지,
  ad-hoc 서명 무결성, 압축 해제와 헤드리스 실행을 검사합니다. Developer ID 서명·공증과
  클린 머신 검증은 남아 있습니다.
- **Windows x64:** 릴리스 워크플로가 ZIP 실행과 WiX MSI 설치·실행·제거, 번역, 고지와
  체크섬을 검사합니다. Microsoft Store 또는 Authenticode 기반 서명과 클린 머신 검증은
  남아 있습니다.
- **Linux:** PyInstaller 설정은 있으나 공개 Linux 패키지는 제공하지 않습니다.

공개 릴리스에는 패키지별 SHA-256 파일이 포함됩니다. 현재 패키지는 서명되지 않았으므로
운영체제의 경고 또는 차단이 발생할 수 있습니다.

### 시각 자료 재현

`scripts/generate_portfolio_assets.py`는 임시 디렉터리의 결정론적 합성 데이터를 사용해
실제 PySide6 앱 화면을 생성합니다. 실제 사용자 파일을 읽지 않습니다.

```bash
QT_QPA_PLATFORM=offscreen uv run python scripts/generate_portfolio_assets.py
```

---

## English

### Current quality baseline

The current source baseline after v1.0.1 uses the following checks.

| Check | Current result |
|-------|----------------|
| Ruff lint / format | Passed |
| mypy | 22 source files, no issues |
| pytest | 259 tests passed |
| GitHub Actions | Lint, type, and test checks on `main` and pull requests |

The suite covers digit calculations, preprocessing, data characteristics, reference statistics,
controller state, UI workflows, HTML reports, translation catalogs, and platform-specific layout.
Qt UI tests run with `QT_QPA_PLATFORM=offscreen`.

### Reproduce

```bash
uv sync --locked --group dev
uv run ruff check .
uv run ruff format --check src/ tests/ scripts/
uv run mypy src/
QT_QPA_PLATFORM=offscreen uv run pytest
```

If Python aborts while loading NumPy, Pandas, or PySide6 native modules after a macOS virtual
environment change, clear the environment's hidden file flags and rerun the checks:

```bash
chflags -R nohidden .venv
```

This workaround affects only the development environment, not application data.

### Performance evidence

A deterministic 100,000-value workload measured controller analysis only, excluding file I/O,
charts, and reports. Each mode was warmed up and compared by the median of five runs.

| Mode | Before | After | Improvement |
|------|-------:|------:|------------:|
| First digit | 0.284455 s | 0.195216 s | 31.4% |
| Second digit | 0.277398 s | 0.194066 s | 30.0% |
| First + second | 0.281804 s | 0.192316 s | 31.8% |

The change removed repeated Python-level digit extraction across analysis and drill-down. These
are controlled comparative measurements, not a performance guarantee for every machine.

The M3 historical standard-library `trace` run covered 1,578 of 1,661 executable source lines,
or 95.00%. That is a historical baseline rather than current coverage; CI does not currently
enforce a coverage percentage.

### Packaging boundaries

- **macOS Apple Silicon:** the release workflow checks architecture, metadata, translations,
  notices, ad-hoc signature integrity, extraction, and headless startup. Developer ID signing,
  notarization, and clean-machine verification remain.
- **Windows x64:** the release workflow checks ZIP startup, WiX MSI install/startup/uninstall,
  translations, notices, and checksums. Microsoft Store or Authenticode signing and clean-machine
  verification remain.
- **Linux:** a PyInstaller configuration exists, but no public Linux package is offered.

Public releases include a SHA-256 file for each package. The current packages are unsigned, so
the operating system may warn about or block them.

### Reproduce visual assets

`scripts/generate_portfolio_assets.py` uses deterministic synthetic data in a temporary directory
to capture the real PySide6 application. It does not read user files.

```bash
QT_QPA_PLATFORM=offscreen uv run python scripts/generate_portfolio_assets.py
```
