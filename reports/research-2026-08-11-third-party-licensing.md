# 공개 배포용 제3자 라이선스 조사

_조사일: 2026-08-11_

## 질문

Benford Lens의 MIT 소스와 PyInstaller 기반 Windows/macOS 패키지를 공개할 때 어떤
제3자 라이선스 고지, 소스 제공, 재링크 가능성, 패키지 검증이 필요한가?

## 범위

Python 3.11, Python 런타임 의존성, PySide6/Qt, PyInstaller, macOS 시스템 라이브러리,
Windows WiX 도구 체인을 검토했다. 현재 `uv.lock`의 Python 3.11용 macOS arm64 및
Windows x64 해석 결과를 기준으로 했으며, 법률 자문이나 모든 배포 상황에 대한 결론이
아닌 재현 가능한 엔지니어링 점검으로 한정했다.

## 확인 결과

1. 기존 `pyside6` 메타 패키지는 앱이 사용하지 않는 Addons 모듈까지 설치했다. 그 결과
   비공개 v1.0.0 패키지에는 GPL-3.0-only로 제공되는 Qt Virtual Keyboard가 우연히
   포함됐다. 공개 전 이를 그대로 노출하지 않는다.
2. 앱이 실제로 import하는 QtCore, QtGui, QtWidgets, QtSvg는
   `pyside6-essentials==6.11.1`로 충족된다. 메타 패키지를 Essentials로 교체하면
   `pyside6-addons`를 잠금 파일과 패키지에서 제거할 수 있다.
3. Essentials에도 QML/Quick 등 사용하지 않는 모듈이 있다. 사양 파일에서 모든
   Qt 6.11 GPL-only 모듈 이름을 거부하고, 네이티브 패키지 검증에서도 같은 목록을
   검사해야 한다.
4. Qt/PySide LGPL 배포 경로는 해당 라이선스 전문, 저작권·귀속 정보, 정확한 대응 소스
   접근 경로, 동적 라이브러리를 수정판으로 교체할 수 있는 실질적 안내가 필요하다.
   Benford Lens는 Qt 라이브러리를 동적으로 로드하고 DRM을 추가하지 않으며,
   `docs/qt-relinking.md`에 교체·재서명 절차를 제공한다.
5. Python 패키지 메타데이터만으로는 NumPy/SciPy/Pillow/Matplotlib가 포함하는 네이티브
   코드, 글꼴, 렌더링 라이브러리의 고지를 빠뜨리기 쉽다. 설치된 정확한 배포판의
   라이선스 파일을 결정론적으로 묶고 SHA-256 목록을 남기는 방식이 적합하다.
6. PyInstaller는 GPL-2.0-or-later와 배포 예외를 제공하므로, 생성된 실행 파일에
   PyInstaller를 사용했다는 이유만으로 애플리케이션 라이선스가 GPL로 바뀌지는 않는다.
   다만 bootloader를 포함한 도구 고지는 제3자 고지 묶음에 기록한다.
7. WiX 5.0.2는 Microsoft Reciprocal License로 제공된다. 빌드 도구로만 사용하더라도
   정확한 버전과 전문을 보존한다. 운영체제 제공 시스템 라이브러리는 별도 복사본이
   아닌 플랫폼 구성요소로 구분한다.

## 선택지

| 선택지 | 장점 | 위험/비용 | 판단 |
|---|---|---|---|
| 기존 `pyside6` 패키지 유지 | 변경이 가장 작음 | 사용하지 않는 Addons 및 GPL-only 모듈이 패키지에 섞임 | 공개 배포에 사용하지 않음 |
| `pyside6-essentials`로 축소하고 모듈 거부 목록 적용 | 실제 앱 범위와 배포 범위가 일치하고 산출물 검증 가능 | 사양 및 플랫폼별 패키지 검증 유지 필요 | **채택** |
| Qt를 정적으로 링크 | 단일 파일 구성 가능 | 재링크용 오브젝트 제공 등 의무와 빌드 복잡도 증가 | 현재 구조에 부적합 |
| 상용 Qt 라이선스 취득 | 상용 조건으로 별도 운영 가능 | 비용 및 별도 계약 관리 | 현재 오픈소스 배포에 불필요 |

## 권장 구현

- 런타임 의존성을 `pyside6-essentials==6.11.1`로 제한하고 잠금 파일에서
  PySide6 Addons를 제거한다.
- `THIRD_PARTY_NOTICES.md`와 `third_party_licenses/`를 소스, macOS 앱 Resources,
  Windows portable 폴더, MSI 설치 폴더에 모두 포함한다.
- Qt 6.11 GPL-only 모듈 전체를 PyInstaller 분석 결과와 완성된 패키지에서 모두
  거부한다.
- 앱 안에서 네트워크나 브라우저를 열지 않고 고지 파일을 읽을 수 있게 한다.
- 정확한 Qt/PySide 소스 태그·커밋·아카이브 해시와 라이선스 파일 해시를 보존하고,
  GitHub 소스 및 이슈 기반 서면 요청 경로를 최소 3년간 유지한다.
- 공개 v1.0.0을 기존 파일로 덮어쓰거나 삭제하지 않는다. 고지 완결 패치를 새 버전으로
  네이티브 재빌드하고, 새 체크섬 및 검증 기록과 함께 공개한다.

## 검증 경계

정적 검사와 단위 테스트는 고지 파일의 존재·재현성, 잠금 버전, 거부 목록, 패키징
스크립트 정책을 확인한다. 실제 macOS ZIP, Windows ZIP/MSI에 고지 파일과 허용된 Qt
구성만 들어갔는지는 네이티브 배포 빌드를 해야 확정할 수 있다. 이 빌드는 프로젝트
헌법과 공개 전 목표의 명시적 사람 승인 이후에만 수행한다.

## 참고 자료

- Qt, [Qt for Python licensing](https://doc.qt.io/qtforpython-6/licenses.html)
- Qt, [Open-source licensing obligations](https://www.qt.io/licensing/open-source-lgpl-obligations)
- Qt, [Qt licensing FAQ](https://www.qt.io/faq/tag/qt-open-source-licensing)
- Qt, [Qt Virtual Keyboard](https://doc.qt.io/qt-6/qtvirtualkeyboard-index.html)
- Qt, [Qt sources](https://code.qt.io/cgit/)
- Python Software Foundation, [Python 3 license](https://docs.python.org/3/license.html)
- PyInstaller, [License](https://pyinstaller.org/en/stable/license.html)
- Matplotlib, [License](https://matplotlib.org/stable/project/license.html)
- Pillow, [External libraries](https://pillow.readthedocs.io/en/stable/installation/building-from-source.html#external-libraries)
- WiX Toolset, [WiX source license at v5.0.2](https://github.com/wixtoolset/wix/blob/v5.0.2/LICENSE.TXT)
