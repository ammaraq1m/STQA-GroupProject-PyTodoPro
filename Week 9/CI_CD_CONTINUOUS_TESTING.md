# PyTodo Pro · Proposed CI/CD and continuous testing

## Test selection and gates

| Stage and trigger | Existing evidence and selection | Gate and reporting |
| --- | --- | --- |
| Pull requests and main pushes | Fast smoke: A01 API registration and GAP03/GAP04 completion-window exclusion checks. They passed historically, use disposable SQLite and require no browser server or live clock for the boundary checks. | Any assertion failure, collection error or missing report makes the smoke check fail. Publish JUnit and assertion evidence. |
| Main pushes, nightly and manual dispatch | Run the unmodified Week 6 manifest (20 API, seven defensive security, six new integration and 12 Chromium/comparison cases). Record 12 deliberate deferrals. This includes GAP01/02 and GAP05, which failed historically, and the defensive source checks that report open controls. The nightly job can also run on demand for a branch through manual dispatch. | Preserve the runner's nonzero outcome, publish merged JSON, JUnit, logs and screenshots, and distinguish product Fail, infrastructure failure and Not Run. A missing artifact or setup failure requires investigation. |
| Proposed candidate acceptance | Same focused regression on the candidate revision, plus verified closure of release-blocking defects, reviewed high-risk coverage, native accessibility and compatibility checks, and approved representative performance criteria. | Require Week 7 exit evidence and named approval before enabling a deployment job. Current results fail this gate. |

The smoke lane gives fast feedback about selected controls. It cannot stand in for the full release gate. The full lane's latest recorded result was 25 pass, 20 fail and 12 deferred. On a build with known failures, keep a defect-linked comparison for triage, including expected failing case IDs, owner, expiry and confirmation plan. A red result remains red. New failures and unexpected passes warrant review. Fixes should pass defect-specific confirmation and the related regression before closure. If the project adopts branch protection, require the smoke lane and publish the full lane prominently. Require a green candidate run for release. Any exception requires explicit, documented review. [Week 6 manifest](../Week%206%20-%20Test%20Automation%20and%20Regression/tests/manifest.json) · [Regression evidence](../Week%206%20-%20Test%20Automation%20and%20Regression/REGRESSION_TESTING.md) · [Week 7 gates](../Week%207/Software%20Test%20Plan.md#entry-exit-and-completion-criteria)

## Inactive GitHub Actions example

The YAML below is a proposed configuration stored in this document. It assumes a Linux runner, checkout-local browser installation and pinning to the historical Python and Node versions. Use read-only repository permissions and synthetic fixture data. GitHub runs each job in a disposable checkout. The full job stages only source and test inputs. Its artifact directory starts empty so failed setup cannot publish archival evidence as new. [GitHub Actions Python guidance](https://docs.github.com/en/actions/tutorials/build-and-test-code/python) · [Playwright CI guidance](https://playwright.dev/docs/ci)

```yaml
name: PyTodo Pro continuous testing example
'on':
  pull_request:
  push:
    branches: [main]
  schedule:
    - cron: '20 2 * * *'
  workflow_dispatch:

permissions:
  contents: read

jobs:
  smoke:
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v5
        with:
          python-version: '3.14.2'
      - name: Install Week 6 Python requirements
        run: python -m pip install -r 'Week 6 - Test Automation and Regression/requirements.txt'
      - name: Run selected regression cases
        shell: bash
        run: |
          stage="$RUNNER_TEMP/pytodo-smoke"
          mkdir -p "$stage/cases/tests" "$stage/cases/logs"
          cp app.py helpers.py "$stage/"
          cp -R templates static "$stage/"
          cp 'Week 4 - Web and API Testing/tests/test_api.py' "$stage/cases/tests/"
          cp 'Week 6 - Test Automation and Regression/tests/test_gaps.py' "$stage/cases/tests/"
          cd "$stage/cases"
          python -B -m pytest -p no:cacheprovider -q --junitxml=logs/junit.xml \
            'tests/test_api.py::test_A01_registration' \
            'tests/test_gaps.py::test_dashboard_completion_window[GAP03]' \
            'tests/test_gaps.py::test_dashboard_completion_window[GAP04]'
      - name: Archive smoke evidence
        if: ${{ !cancelled() }}
        uses: actions/upload-artifact@v4
        with:
          name: smoke-${{ github.run_id }}-${{ github.run_attempt }}
          path: ${{ runner.temp }}/pytodo-smoke/cases/logs
          if-no-files-found: error

  focused-regression:
    if: github.event_name != 'pull_request'
    runs-on: ubuntu-24.04
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v5
        with:
          python-version: '3.14.2'
      - uses: actions/setup-node@v6
        with:
          node-version: '24.22.2'
      - name: Stage sources and install pinned stack and Chromium
        shell: bash
        run: |
          stage="$RUNNER_TEMP/pytodo-focused"
          mkdir -p "$stage"
          cp app.py helpers.py "$stage/"
          cp -R templates static "$stage/"
          for week in 'Week 4 - Web and API Testing' 'Week 5 - Security and Performance Testing' 'Week 6 - Test Automation and Regression'; do
            mkdir -p "$stage/$week/tests"
            cp "$week"/tests/*.* "$stage/$week/tests/"
          done
          python -m pip install -r 'Week 6 - Test Automation and Regression/requirements.txt'
          cd "$stage/Week 6 - Test Automation and Regression"
          npm --prefix tests ci
          npm --prefix tests exec -- playwright install --with-deps chromium
      - name: Run focused regression
        shell: bash
        run: |
          cd "$RUNNER_TEMP/pytodo-focused/Week 6 - Test Automation and Regression"
          python -B tests/run.py
      - name: Archive focused evidence
        if: ${{ !cancelled() }}
        uses: actions/upload-artifact@v4
        with:
          name: focused-${{ github.run_id }}-${{ github.run_attempt }}
          path: |
            ${{ runner.temp }}/pytodo-focused/Week 6 - Test Automation and Regression/logs
            ${{ runner.temp }}/pytodo-focused/Week 6 - Test Automation and Regression/screenshots
          if-no-files-found: error
```

The three smoke selectors passed in the local Week 9 rehearsal. The staged full runner reproduced the archived 25 Pass, 20 Fail and 12 Not Run with zero infrastructure errors. GitHub Actions execution remains unverified. Before adoption, validate the exact action versions on the target GitHub runner, inspect artifact access and retention, and exercise setup and failure paths. The workflow example contains no deployment job. Scheduled performance and full cross-browser/native follow-up need separate environments and acceptance criteria. Published artifacts should contain fixture-only traces and retain case IDs, revision, tool versions and attempt metadata.
