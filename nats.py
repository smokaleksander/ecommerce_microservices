from pynats import NATSClient

with NATSClient() as client:
    client.publish("test-subject", payload=b"test-payload")
