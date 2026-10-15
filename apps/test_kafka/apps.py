import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class TestKafkaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.test_kafka"

    def ready(self):
        from django.conf import settings

        try:
            from kafka import KafkaAdminClient
            from kafka.errors import KafkaError
        except ImportError:
            logger.error("kafka-python is not installed; Kafka features will not work")
            return

        try:
            client = KafkaAdminClient(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                request_timeout_ms=3000,
            )
            client.close()
        except KafkaError as exc:
            logger.error("Kafka unavailable at startup (%s): %s", settings.KAFKA_BOOTSTRAP_SERVERS, exc)
