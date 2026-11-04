from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_model import audit

class StaticAuditTests(unittest.TestCase):
    def test_model_structure(self):
        self.assertEqual(audit(), [])
