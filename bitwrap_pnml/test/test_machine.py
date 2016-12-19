""" test state machine operations """
import twisted
from twisted.trial import unittest
from twisted.internet import defer
import bitwrap_pnml
from bitwrap_pnml.storage import Storage

twisted.internet.base.DelayedCall.debug = True

class MachineTestCase(unittest.TestCase):
    """ test machine transactions """

    def setUp(self):
        Storage.truncate()
        self.machine = bitwrap_pnml.get('split_join_1')

    def tearDown(self):
        pass

    @defer.inlineCallbacks
    def test_machine_transaction(self):
        """ invoke state machine transformations """

        req = self.machine.session({
            'oid': 'fake-oid',
            'action': 'T0',
            'payload': {'foo': 'bar'}
        })

        res = yield req.commit()
        assert res['event']['state'] == [0, 0, 0, 1, 0, 0]

        req = self.machine.session({
            'oid': 'fake-oid',
            'action': 'T1'
        })

        res = yield req.commit()
        assert res['event']['state'] == [1, 1, 0, 0, 0, 0]