# 무료 또는 승인 없는 데스크톱 배포 경로 조사

_조사일: 2026-08-10_

## 질문

Benford Lens를 Windows와 macOS에 배포할 때 개발자 계정, 유료 코드 서명, 플랫폼 승인을
피할 수 있는 실용적인 대안이 있는가?

## 범위와 판단 기준

현재의 Python 3.11, PySide6, PyInstaller 배포 구조와 로컬 전용 데이터 처리 원칙을
유지하는 경로를 우선 검토했다. 다음 항목은 서로 다른 문제이므로 분리해서 판단했다.

- **호스팅**: 사용자가 설치 파일을 내려받을 장소
- **코드 서명**: 배포자가 누구인지와 파일 변경 여부를 운영체제가 확인하는 수단
- **플랫폼 검사**: Store 인증, App Review, 또는 자동화된 notarization
- **사용자 경험**: 일반 사용자가 보안 설정을 변경하지 않고 설치·실행할 수 있는지

## 결론

**무료 배포와 승인 없는 배포는 가능하지만, 두 운영체제에서 동시에 무료·무승인·무경고를
만족하는 방법은 없다.** GitHub Releases에 현재 산출물을 그대로 올리는 경로는 무료이고
플랫폼 사전 승인도 없지만, Windows SmartScreen/Smart App Control과 macOS Gatekeeper가
경고하거나 실행을 막을 수 있다.

현실적인 최소비용 조합은 다음과 같다.

1. **Windows: Microsoft Store에 MSIX로 제출** — 신규 개인 개발자는 등록비가 없고,
   Microsoft가 MSIX를 무료로 서명하고 호스팅한다. Microsoft 계정, 정부 발급 신분증과
   셀피를 통한 신원 확인, 앱 인증은 필요하다.
2. **macOS: Apple Developer Program + Developer ID + notarization** — 일반 사용자를 위한
   매끄러운 직접 배포에는 연간 99 USD가 사실상 필요하다. Store 밖 배포의 notarization은
   전체 App Review가 아니라 자동 보안 검사이지만, Apple Developer Program 가입은 필요하다.
3. **공통 호스팅: GitHub Releases** — 서명된 최종 파일, 체크섬, 릴리스 노트를 무료로
   제공한다. 개별 릴리스 파일은 2 GiB 미만이어야 하며 총 릴리스 크기와 대역폭에는 제한이
   없다. 현재 약 81 MB인 macOS ZIP과 Windows ZIP/MSI에는 충분하다.

이 조합이면 Windows용 별도 상용 Authenticode 인증서 비용을 없애고, 필수 현금 비용을
macOS의 연간 프로그램 비용으로 한정할 수 있다.

## 선택지 비교

| 경로 | 직접 비용 | 계정/신원 확인 | 앱 또는 프로젝트 검사 | 일반 사용자 경고 | Benford Lens 적합성 |
|---|---:|---|---|---|---|
| GitHub Releases + 서명 없는 현재 ZIP/MSI | 0 | 기존 GitHub 계정만 | 없음 | Windows/macOS 모두 있음; 일부 환경은 실행 차단 가능 | 테스트·포트폴리오 공개에는 가능, 비전문가 대상 정식 배포에는 낮음 |
| Microsoft Store + MSIX | 0 (신규 개인 계정) | Microsoft 계정, 신분증, 셀피 | Store 인증 필요 | Store 설치 시 SmartScreen 경고 없음 | **Windows 권장**; 현재 MSI를 그대로 내는 대신 MSIX 전환 필요 |
| Microsoft Store + 현재 MSI/EXE | Store 등록은 0 | 동일 | Store 인증 필요 | Store 경로는 매끄럽지만 게시자가 파일을 먼저 서명해야 함 | 무료 서명 목적에는 부적합 |
| SignPath Foundation | 0 (선정된 OSS 프로젝트) | 개인 신원 확인은 요구하지 않는다고 안내 | 프로젝트 신청·선정과 CI 원본 검증 필요 | 신뢰 향상 가능, SmartScreen 무경고를 모든 새 파일에 보장하지는 못함 | **Windows 보조 후보**; 아직 첫 공개 릴리스가 없어 즉시 자격 충족 여부 불확실 |
| Apple Developer ID + notarization | 연 99 USD | Apple 계정 및 등록 확인 | 자동 notarization | 정상적인 Gatekeeper 흐름 | **macOS 정식 배포 권장** |
| Apple 프로그램 비용 면제 | 0 | 적격 법인 등록·확인 | 면제 승인 및 notarization | 정상적인 Gatekeeper 흐름 | 비영리 법인·인가 교육기관·정부기관에 한정; 개인 프로젝트에는 해당하지 않음 |
| 브라우저/PWA 재구축 | 호스팅에 따라 0 가능 | 자체 배포는 플랫폼 계정 불필요 | 네이티브 앱 검사는 없음 | 네이티브 서명 경고 없음 | 대규모 재작성, 최초 접속 인터넷 의존 가능성 때문에 현재 v1.0 대안으로 부적합 |

## 운영체제별 세부 판단

### Windows

#### 1. 무료이면서 일반 사용자 경험이 가장 좋은 경로: Store MSIX

Microsoft는 신규 개인 개발자용 Store 등록비를 면제하고 있다. 새 등록 흐름은 거의 200개
시장에 제공되며, 정부 발급 신분증과 셀피로 신원을 확인한다. MSIX로 제출하면 Store가
패키지를 다시 서명하고 호스팅하므로 별도 Authenticode 인증서를 구매하지 않아도 된다.

현재 WiX MSI를 Store에 링크하는 방식은 이 혜택을 받지 못한다. 기존 MSI/EXE 제출은
설치 파일과 내부 PE 파일을 신뢰된 인증기관의 인증서로 먼저 서명해야 한다. 따라서 무료
경로를 택하려면 PyInstaller one-folder 산출물을 **MSIX로 별도 포장하고 Store 인증을
통과시키는 작은 배포 트랙**을 추가하는 편이 맞다. Microsoft는 Qt를 포함한 기존 Win32
앱의 MSIX 포장을 지원 대상으로 명시한다.

#### 2. 승인 없는 경로: 서명 없는 GitHub Release

가능하지만 사용자는 SmartScreen의 `Windows protected your PC` 경고를 거쳐 직접 실행을
선택해야 한다. 서명 없는 새 버전은 파일 해시 평판을 매번 처음부터 쌓는다. 더 중요한 점은
일부 새 Windows 11 설치에서 Smart App Control이 알려지지 않은 서명 없는 코드를 기본
차단한다는 것이다. 따라서 설치 안내만으로 모든 PC에서 실행 가능하다고 보장할 수 없다.

자체 서명 인증서는 무료이지만 공개 배포에서 신뢰 체인을 만들지 못하므로 SmartScreen
관점에서는 서명하지 않은 파일과 같은 결과다. 체크섬은 다운로드 무결성을 사용자가 직접
확인하는 데 유용하지만 운영체제 신뢰를 대신하지 않는다.

#### 3. 오픈소스 무료 서명: SignPath Foundation

SignPath Foundation은 선정된 오픈소스 프로젝트에 Windows EXE/MSI Authenticode 서명을
무료로 제공한다. 개인 인증서가 아니라 `SignPath Foundation` 명의 인증서를 사용하며,
공개 저장소에서 나온 빌드인지 확인하는 CI 구성이 필요하다.

Benford Lens는 MIT 라이선스와 공개 문서를 갖췄으므로 방향은 잘 맞는다. 다만 공식 조건에
따르면 프로젝트가 활발히 유지되고, 문서화되어 있으며, **서명하려는 형태로 이미 릴리스된
상태**여야 한다. 현재 공개 v1.0.0 릴리스가 없으므로, 먼저 unsigned preview를 공개한 뒤
신청하거나 사전 문의해야 할 가능성이 높다. 또한 신청·선정 절차가 있으므로 “승인 없는
방법”은 아니다.

### macOS

#### 1. 무료·승인 없는 직접 배포

현재 ad-hoc 서명된 `.app` ZIP을 GitHub Releases로 배포할 수 있다. 사용자는 최초 실행을
시도한 뒤 `시스템 설정 → 개인정보 보호 및 보안 → 그래도 열기(Open Anyway)`로 예외를
승인할 수 있다. Apple은 이 버튼이 실행 시도 후 약 한 시간 동안 표시된다고 안내한다.

기술적으로 배포는 되지만 보안 설정을 직접 우회하게 만드는 흐름이라 비전문가 대상 제품과
잘 맞지 않으며, 조직에서 관리하는 Mac은 사용자가 예외를 허용하지 못할 수도 있다.

#### 2. 경고 없는 일반적인 직접 배포

Gatekeeper가 신뢰하는 Store 밖 배포에는 Apple이 발급한 Developer ID 인증서와
notarization이 필요하다. Developer ID 인증서는 Apple Developer Program 회원에게만
발급되며 프로그램 비용은 연간 99 USD다. 제3자 무료 인증서나 self-signing으로 이 Apple
신뢰 체인을 대체할 수 없다. SignPath 역시 macOS의 공개 신뢰를 위해서는 Apple 개발자
계정과 Apple 발급 인증서가 필요하다고 명시한다.

비영리 법인, 인가 교육기관, 정부기관은 조건을 만족하면 비용 면제를 신청할 수 있지만,
개인·개인사업자·1인 사업체는 대상이 아니다. 해당 기관이 프로젝트를 공식적으로 맡는
상황이 아니라면 현재 프로젝트의 현실적인 무료 경로로 보기는 어렵다.

## 권장 실행안

### 정식 v1.0을 비전문가에게 제공하려는 경우

- **Windows**: 기존 ZIP/MSI 후보는 보관하고, Store 제출용 MSIX를 추가한다. 무료 개인
  개발자 등록 가능 여부를 한국 등록 화면에서 최종 확인한 뒤 MSIX 변환, 깨끗한 Windows
  VM 설치/실행/제거, Store 인증 순으로 검증한다.
- **macOS**: Apple Developer Program에 가입해 현재 arm64 앱을 Developer ID로 서명하고,
  hardened runtime 검증, notarization, ticket stapling, 깨끗한 Mac 검증을 수행한다.
- **다운로드와 증빙**: GitHub Release에 최종 파일과 SHA-256 체크섬을 함께 게시한다.

예상 플랫폼 비용은 **Windows 0 + macOS 연 99 USD**다. 플랫폼 가입·검사 절차 자체를
모두 없애지는 못하지만, 비전문가가 보안 경고를 우회하도록 요구하지 않는 가장 저렴한
구성이다.

### 비용 0이 절대 조건인 경우

- 두 플랫폼의 unsigned/ad-hoc ZIP을 GitHub Releases에 `preview` 또는 `testing build`로
  공개한다.
- 공식 운영체제 안내에 맞춘 최초 실행 절차와 SHA-256 확인 방법을 제공한다.
- Windows Smart App Control 및 조직 관리 장치에서는 실행이 불가능할 수 있음을 명시한다.
- 이 상태를 “모든 사용자에게 매끄러운 정식 배포”로 표현하지 않는다.

이 경로는 포트폴리오와 제한된 테스터에게는 사용할 수 있지만, 프로젝트가 목표로 하는
비전문가용 v1.0의 기본 배포 경로로는 권장하지 않는다.

## 참고 자료

- Apple, [Choosing a Membership](https://developer.apple.com/support/compare-memberships/)
- Apple, [Developer ID certificate](https://developer.apple.com/help/glossary/developer-id-certificate/)
- Apple, [Distribution](https://developer.apple.com/documentation/technologyoverviews/distribution)
- Apple Support, [Open a Mac app from an unknown developer](https://support.apple.com/guide/mac-help/open-a-mac-app-from-an-unknown-developer-mh40616/mac)
- Apple, [Apple Developer Program fee waiver](https://developer.apple.com/help/account/membership/fee-waivers/)
- Microsoft, [Free developer registration for individual developers](https://learn.microsoft.com/en-us/windows/apps/publish/whats-new-individual-developer)
- Microsoft, [How to distribute your Win32 application through Microsoft Store](https://learn.microsoft.com/en-us/windows/apps/distribute-through-store/how-to-distribute-your-win32-app-through-microsoft-store)
- Microsoft, [Code signing options for Windows app developers](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/code-signing-options)
- Microsoft, [SmartScreen reputation for Windows app developers](https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation)
- Microsoft, [Smart App Control overview](https://learn.microsoft.com/en-us/windows/apps/develop/smart-app-control/overview)
- GitHub, [About releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- GitHub, [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- SignPath Foundation, [Free Code Signing for Open Source software](https://signpath.org/)
- SignPath Foundation, [Conditions for Open Source projects](https://signpath.org/terms.html)
- SignPath, [Building Trusted Software for macOS](https://signpath.io/blog/building-trusted-software-for-macos-a-how-to-guide-for-digital-signing)
