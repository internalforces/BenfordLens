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

## 적용한 GitHub 설정

비공개 상태에서도 제공되는 기능은 준비 PR 전에 실제 서버에 적용하고 다시 읽어 확인했다.

- Actions는 GitHub 소유 Action과 `astral-sh/setup-uv@*`만 허용한다.
- `Protect main` ruleset ID `20656284`가 active다. PR, 최신 `lint-type-test`,
  conversation resolution을 요구하고 삭제와 non-fast-forward update를 차단하며 bypass가
  없다.
- `Protect release tags` ruleset ID `20656289`가 active다. `v[0-9]*.[0-9]*.[0-9]*`
  태그 삭제와 이동을 차단하며 bypass가 없다.
- dependency graph가 SPDX SBOM 45개 구성 요소를 반환한다.
- Dependabot alerts와 security updates가 활성화되어 있고 초기 open alert는 0개다.
- PR #17이 Linux CI와 승인된 macOS/Windows 네이티브 검증을 통과하고 merge commit
  `49edb74`로 병합된 직후 repository-wide `sha_pinning_required=true`를 적용하고 API로
  다시 읽어 확인했다. 같은 merge commit의 `main` CI run `31447921264`도 성공했다.

전체 SHA 강제 설정은 준비 branch가 merge되기 전까지 의도적으로 끈 상태로 유지했다.
기존 `main` workflow의 mutable major tag가 제거된 후 바로 활성화했으므로 현재 허용된
외부 Action도 전체 커밋 SHA 없이는 실행할 수 없다.

Secret scanning은 비공개 상태에서 enable 요청이 HTTP 422
(`Secret scanning is not available for this repository`)로 거절됐다. Private vulnerability
reporting endpoint는 HTTP 404, code-scanning alerts endpoint는 아직 활성화되지 않았다는
HTTP 403을 반환했다. 이 세 기능과 push protection, 첫 CodeQL 실행은 공개 전환 직후
활성화·검증하고 ruleset도 visibility 변경 후 다시 확인한다.

## 검증 결과와 남은 게이트

- 명시적 사람 승인 뒤 실행한 PR #17 Linux CI `31447586712`와 native run `31447586711`이
  새 Action 주요 버전, uv 0.11.30, macOS arm64 ZIP, Windows x64 ZIP/MSI를 모두 검증했다.
- `Protect main` ruleset이 실제 PR merge gate를 적용했고 PR #17은 required check 통과 뒤
  merge됐다. 두 ruleset의 대상·규칙·status context·active 상태·bypass 부재도 merge 후
  다시 읽어 일치함을 확인했다.
- CodeQL upload, secret scanning, private vulnerability reporting은 공개 전환 뒤에만
  최종 검증할 수 있다.

## 공식 근거

- GitHub, [Actions settings and full-length SHA enforcement](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)
- GitHub, [Secure use of third-party Actions](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions)
- GitHub, [Dependabot supported ecosystems](https://docs.github.com/en/code-security/reference/supply-chain-security/supported-ecosystems-and-repositories)
- GitHub, [Creating repository rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)
- GitHub, [Available rules for rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- GitHub, [Code scanning with CodeQL](https://docs.github.com/en/code-security/code-scanning/creating-an-advanced-setup-for-code-scanning)

## 공개 전환 후 이행

TASK-044 승인 후 저장소를 공개로 전환했다. 두 ruleset, selected Actions,
전체 SHA 강제, 읽기 전용 기본 workflow 권한, Dependabot 보호는 변경 후에도
유지됐다. Secret scanning, push protection, private vulnerability reporting을 활성화했고
초기 secret/CodeQL alert 목록은 비어 있었다. 공개 상태의 첫 CodeQL 분석은 PR #21
run `31451987591`에서 52초 만에 통과했다. 세부 근거는
`reports/release-2026-08-11-public-launch.md`에 기록했다.
