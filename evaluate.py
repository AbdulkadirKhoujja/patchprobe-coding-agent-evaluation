"""Offline repeatable evaluation of a synthetic candidate vs a reference patch."""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def run_case(implementation, suite):
    env = os.environ.copy()
    env['PYTHONPATH'] = str(ROOT / implementation)
    cmd = [sys.executable, '-m', 'unittest', 'discover', '-s', str(ROOT / 'tests'), '-p', f'test_{suite}.py', '-v']
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env, cwd=ROOT, timeout=30)
    out = proc.stdout
    executed = re.search(r'Ran (\d+) tests?', out)
    failures = re.search(r'FAILED \((.*?)\)', out)
    return {
        'implementation': implementation,
        'suite': suite,
        'exit_code': proc.returncode,
        'tests_run': int(executed.group(1)) if executed else None,
        'passed': proc.returncode == 0,
        'failure_summary': failures.group(1) if failures else None,
        'failed_cases': re.findall(r'^((?:FAIL|ERROR): .+)$', out, flags=re.MULTILINE),
        'raw_output': out,
    }


def main():
    cases = [run_case(impl, suite) for impl in ('candidate', 'reference') for suite in ('public', 'holdout')]
    outdir = ROOT / 'evidence'
    outdir.mkdir(exist_ok=True)
    public_record = [{k: v for k, v in c.items() if k != 'raw_output'} for c in cases]
    (outdir / 'results.json').write_text(json.dumps({'schema': 'synthetic-agent-evaluation-v1', 'cases': public_record}, indent=2) + '\n', encoding='utf-8')
    lines = ['# Executed evidence — synthetic coding-agent evaluation', '',
             'Run with `python evaluate.py`. `candidate` is a **deliberately flawed synthetic patch**, not a claim about real LLM performance.', '',
             '| Implementation | Suite | Tests | Outcome |', '|---|---|---:|---|']
    for c in cases:
        lines.append(f"| {c['implementation']} | {c['suite']} | {c['tests_run']} | {'PASS' if c['passed'] else 'FAIL (expected for seeded candidate)'} |")
    lines.extend(['', '## Seeded candidate failures (observed)', ''])
    bad = next(c for c in cases if c['implementation']=='candidate' and c['suite']=='holdout')
    for fail in bad['failed_cases']:
        lines.append('- ' + fail.replace('FAIL: ', '').replace('ERROR: ', ''))
    lines += ['', '## Interpretation',
              'The public suite alone does not establish correctness. Held-out checks expose global-event-ID deduplication, stale-event selection, unsafe input handling and mutable payload sharing. The reference implementation passes the same checks. These are local test observations about two given Python files, not empirical AI model benchmark scores.',
              '', 'See `REVIEW.md` for PR-style review and remedial acceptance criteria.', '']
    (outdir / 'report.md').write_text('\n'.join(lines), encoding='utf-8')
    for c in cases:
        print(f"{c['implementation']} {c['suite']}: {c['tests_run']} run; {'PASS' if c['passed'] else 'FAIL'}")
    if not (cases[0]['passed'] and not cases[1]['passed'] and cases[2]['passed'] and cases[3]['passed']):
        raise SystemExit('UNEXPECTED_EVALUATION_RESULT')
    print('EVALUATION_DESIGN_VALIDATED')


if __name__ == '__main__':
    main()
