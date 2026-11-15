import json
import unittest
from pathlib import Path
from arrival_cascade.partner import operate, parse_time


class DomainTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads(Path('data/release.json').read_text())

    def test_existing_domain_contract(self):
        result=operate('/v1/window-check',{'site':'west','start':'2026-11-12T08:00:00+08:00','end':'2026-11-12T22:00:00+08:00'},self.data)
        self.assertEqual(result['observed_seconds'],0)
        observed=operate('/v1/window-check',{'site':'north','start':'2026-11-12T08:00:00+08:00','end':'2026-11-12T22:00:00+08:00'},self.data)
        self.assertEqual(observed['observed_seconds'],14*3600)


if __name__=='__main__':
    unittest.main()
