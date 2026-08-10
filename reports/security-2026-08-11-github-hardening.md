# GitHub 공급망 및 저장소 거버넌스 강화

_점검일: 2026-08-11_

## 적용한 소스 정책

- 모든 workflow `uses:` 참조를 전체 40자리 커밋 SHA로 고정하고 사람이 확인할 수 있도록
  대응 릴리스 태그 주석을 남겼다.
- `actions/checkout`은 v7.0.1, `astral-sh/setup-uv`는 v9.0.0,
  `actions/upload-artifact`는 v7.0.1, `actions/download-artifact`는 v8.0.1,
  `github/codeql-action`은 v4.37.6 커밋을 사용한다.
- workflow의 uv 자체도 `0.11.30`으로 고정해 `latest` 해석을 제거했다.
- 기본 토큰 권한은 `contents: read`다. 릴리스 workflow에서는 두 네이티브 빌드가
  검증한 산출물을 Actions artifact로 넘기고, 마지막 태그 전용 작업만
  `contents: write`를 받는다.
- 공개 저장소에서만 실행되는 Python CodeQL workflow를 추가했다. 비공개 GitHub Free
  상태에서는 작업이 명시적으로 건너뛰어지며, 공개 전환 뒤 실행 결과를 별도로 확인한다.
- Dependabot이 `uv`와 GitHub Actions를 매주 확인한다.
- CODEOWNERS가 workflow, 릴리스 노트, 패키징, 고지, ruleset 구성을 소유한다.
- `protect-main.json`은 PR, 최신 `lint-type-test` 통과, review thread 해결, 삭제 및
  force-push 차단을 요구한다. `protect-release-tags.json`은 `v*.*.*` 태그의 삭제와
  이동을 차단한다.

## 릴리스 workflow 변경

기존 workflow는 태그 작업 초기에 draft Release를 만들고 각 네이티브 job에 쓰기 토큰을
주어 파일을 직접 올렸다. 새 workflow는 다음 경계를 사용한다.

1. 읽기 전용 metadata job이 버전과 릴리스 노트를 검사한다.
2. 읽기 전용 Windows/macOS job이 패키지를 빌드·검증하고 7일 보존 artifact로 넘긴다.
3. 두 job이 모두 성공한 태그 실행에서만 쓰기 권한을 가진 publisher가 정확히 6개 파일인지
   비교한다.
4. 같은 태그의 기존 비-draft Release가 있으면 중단한다. 없거나 draft인 경우에만 정확한
   노트와 파일을 올린 뒤 공개한다.

따라서 플랫폼 job 실패 시 공개 또는 부분 draft Release가 생성되지 않고, PR 빌드는
Release 쓰기 권한을 받지 않는다.

## GitHub 설정 적용 순서

workflow가 merge되기 전 전체 SHA 강제 설정을 켜면 현재 `main`의 mutable tag workflow가
즉시 실패하므로 다음 순서를 지킨다.

1. 준비 PR의 표준 CI와 명시적으로 승인된 네이티브 패키지 checks를 통과시킨다.
2. PR을 `main`에 merge한다.
3. Actions 허용 범위를 GitHub 소유 Actions와 `astral-sh/setup-uv`로 제한하고
   `sha_pinning_required=true`를 설정한다.
4. 공개 GitHub Free에서 사용할 수 있는 repository ruleset 두 개를 import 또는 API로
   적용한다.
5. dependency graph/alerts, Dependabot security updates, private vulnerability reporting,
   secret scanning, push protection, CodeQL을 활성화하고 실제 상태를 다시 읽어 확인한다.

3단계는 merge 직후 수행할 수 있다. Ruleset 및 GitHub Advanced Security의 공개 무료
기능은 최종 공개 전환 직후 적용·검증한다. 저장소가 비공개인 동안 해당 기능이 계정 플랜에
제공되지 않는 것은 설정 누락과 구분해 기록한다.

## 남은 검증 게이트

- 이 변경은 release workflow의 path에 해당하므로 PR 생성 시 Windows/macOS 배포 빌드가
  실행된다. 프로젝트 헌법에 따라 그 직전에 사람 승인을 받아야 한다.
- 새 Action 주요 버전과 uv 버전은 PR의 실제 hosted runner에서 검증한다.
- Ruleset JSON은 정적 테스트로 대상·규칙·status context를 확인하지만, GitHub에 적용한
  뒤 API 응답과 보호 동작을 다시 확인해야 한다.
- CodeQL upload, secret scanning, private vulnerability reporting은 공개 전환 뒤에만
  최종 검증할 수 있다.

## 공식 근거

- GitHub, [Actions settings and full-length SHA enforcement](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)
- GitHub, [Secure use of third-party Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
- GitHub, [Dependabot supported ecosystems](https://docs.github.com/en/code-security/reference/supply-chain-security/supported-ecosystems-and-repositories)
- GitHub, [Creating repository rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)
- GitHub, [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- GitHub, [Code scanning with CodeQL](https://docs.github.com/en/code-security/code-scanning/creating-an-advanced-setup-for-code-scanning)
