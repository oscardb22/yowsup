from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers import YowLayerEvent, YowLayerTest
from yowsup.layers.auth.protocolentities import StreamFeaturesProtocolEntity, AuthProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.stacks import YowStack


class AuthenticationProtocolLayerTest(YowLayerTest, YowAuthenticationProtocolLayer):
    def setUp(self):
        # YowAuthenticatorLayer.__init__(self)
        super(YowAuthenticationProtocolLayer, self).__init__()
        dummyStack = YowStack()
        self.setStack(dummyStack)

        self.credentials = ("dummyusername", bytearray("password", "latin-1"))
        dummyStack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, self.credentials)
        # ticatorLayer.setProp("credentials", self.credentials)

    def test_streamfeatures(self):
        self._sendFeatures()
        self.assertEqual(self.lowerSink.pop(), StreamFeaturesProtocolEntity(
            ["readreceipts", "groups_v2", "privacy", "presence"]).toProtocolTreeNode())

    def test_auth(self):
        self._sendAuth()
        self.assertEqual(self.lowerSink.pop(), AuthProtocolEntity(self.credentials[0]).toProtocolTreeNode())

    def test_handle_challenge(self):
        node = ProtocolTreeNode("challenge", {}, None, "salt")
        self.handleChallenge(node)

    def test_login_onconnected(self):
        self.onEvent(YowLayerEvent("network.state.connected"))
