from pathlib import Path
import json, unittest, yaml
HERE=Path(__file__).resolve().parent
class DesignContractChecks(unittest.TestCase):
 def test_openapi_parses_and_has_page_routes(self):
  d=yaml.safe_load((HERE/'openapi.v014.yaml').read_text())
  self.assertEqual(d['openapi'],'3.1.0')
  required={'/api/v1/system/info','/api/v1/overview','/api/v1/ontology/terms','/api/v1/ontology/terms/{id}','/api/v1/graph/neighborhood','/api/v1/obligations','/api/v1/obligations/{id}/evidence','/api/v1/releases','/api/v1/releases/{id}/assessments','/api/v1/validation/status'}
  self.assertTrue(required.issubset(d['paths']))
  self.assertTrue(all(set(v)=={'get'} for v in d['paths'].values()))
 def test_goldens_are_internally_consistent(self):
  cases=json.loads((HERE/'release-decision-goldens.json').read_text())['cases']
  self.assertEqual(len({c['id'] for c in cases}),len(cases))
  for c in cases:
   if not c['inventoryComplete'] or not c['obligations']: expected='unknown'
   elif 'unqualified' in c['obligations']: expected='unqualified'
   elif 'unknown' in c['obligations']: expected='unknown'
   else: expected='qualified'
   self.assertEqual(c['expected'],expected,c['id'])
if __name__=='__main__': unittest.main()
