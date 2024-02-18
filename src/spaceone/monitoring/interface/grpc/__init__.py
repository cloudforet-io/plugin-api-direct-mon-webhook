from spaceone.core.pygrpc.server import GRPCServer
from spaceone.monitoring.interface.grpc.webhook import Webhook
from spaceone.monitoring.interface.grpc.event import Event

_all_ = ["app"]

app = GRPCServer()
app.add_service(Webhook)
app.add_service(Event)
