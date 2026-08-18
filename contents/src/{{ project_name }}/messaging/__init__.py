from __future__ import annotations

import pulsar

_client: pulsar.Client | None = None
_producer: pulsar.Producer | None = None


async def init_messaging(settings) -> None:
    global _client, _producer
    auth = pulsar.AuthenticationToken(settings.messaging_jwt_token) if settings.messaging_jwt_token else None
    _client = pulsar.Client(settings.messaging_broker_url, authentication=auth)
    _producer = _client.create_producer(settings.messaging_topic)


async def close_messaging() -> None:
    global _client, _producer
    if _producer is not None:
        _producer.close()
        _producer = None
    if _client is not None:
        _client.close()
        _client = None


def get_producer() -> pulsar.Producer:
    if _producer is None:
        raise RuntimeError("Messaging not initialized — call init_messaging() first")
    return _producer
