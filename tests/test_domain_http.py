import copy
import json
import threading
import unittest
from pathlib import Path
from arrival_cascade.provider import make_server
from arrival_cascade.partner import operate
from arrival_cascade.wire import call, RemoteFailure


class DomainHTTPTests(unittest.TestCase):
    def setUp(self):
        self.data=json.loads(Path('data/release.json').read_text())
        self.source=make_server(('127.0.0.1',0),self.data)
        self.thread=threading.Thread(target=self.source.serve_forever,daemon=True)
        self.thread.start()
        self.base=f'http://127.0.0.1:{self.source.server_port}'
        self.payload={'site': 'north', 'start': '2026-11-12T08:00:00+08:00', 'end': '2026-11-12T22:00:00+08:00'}

    def tearDown(self):
        self.source.shutdown()
        self.source.server_close()
        self.thread.join()

    def test_domain_protocol_matches_local_contract(self):
        result=call(self.base,'/v1/window-check',{'revision':'release-1',**self.payload})
        expected=operate('/v1/window-check',self.payload,self.data)
        self.assertEqual(result,expected)
        self.assertIn('observed_seconds',result)

    def test_domain_revision_is_required(self):
        with self.assertRaises(RemoteFailure):
            call(self.base,'/v1/window-check',{'revision':'old-release',**self.payload})

    def test_query_does_not_rewrite_published_data(self):
        before=copy.deepcopy(self.data)
        operate('/v1/window-check',self.payload,self.data)
        self.assertEqual(before,self.data)


if __name__=='__main__':
    unittest.main()
