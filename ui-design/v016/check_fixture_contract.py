import json
from pathlib import Path
p=Path(__file__).with_name('policy_golden_candidates.json')
cases=json.loads(p.read_text(encoding='utf-8'))['cases']
assert len(cases)>=8
assert len({x['id'] for x in cases})==len(cases)
for x in cases:
    assert x['assessment'] in {'qualified','unqualified','unknown'}
    assert x['assurance'] in {'verified','unverified','blocked'}
    assert x['evidence'] and set(x['evidence']) <= {'eligible','ineligible','indeterminate'}
    if not x['catalogComplete'] or not x['metadataComplete'] or not x['provenanceTrusted']:
        assert x['assessment']=='unknown'
    if x['validation']=='not_run': assert x['assurance']=='blocked'
print(f'PASS: {len(cases)} candidate fixture contract checks (NOT runtime policy tests)')
