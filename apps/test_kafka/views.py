import json
import logging

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from kafka.errors import KafkaError

kafka_logger = logging.getLogger("kafka_messages")


@csrf_exempt
@require_POST
def produce(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    message = data.get("message", "")
    if not message:
        return JsonResponse({"error": "Field 'message' is required"}, status=400)

    try:
        producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: v.encode("utf-8"),
        )
        future = producer.send(settings.KAFKA_TOPICS["test"], value=message)
        producer.flush()
        record_metadata = future.get(timeout=10)
    except KafkaError as exc:
        return JsonResponse({"error": str(exc)}, status=502)

    return JsonResponse(
        {
            "status": "sent",
            "topic": record_metadata.topic,
            "partition": record_metadata.partition,
            "offset": record_metadata.offset,
        }
    )


@require_GET
def consume(request):
    max_messages = int(request.GET.get("max", 10))

    try:
        topic = settings.KAFKA_TOPICS["test"]
        consumer = KafkaConsumer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id="django-consumer-group",
            enable_auto_commit=False,
            consumer_timeout_ms=3000,
            value_deserializer=lambda b: b.decode("utf-8"),
        )

        partition_ids = consumer.partitions_for_topic(topic) or set()
        tps = [TopicPartition(topic, p) for p in partition_ids]
        consumer.assign(tps)

        for tp in tps:
            committed = consumer.committed(tp)
            if committed is not None:
                consumer.seek(tp, committed)
            else:
                consumer.seek_to_beginning(tp)

        messages = []
        for msg in consumer:
            kafka_logger.info(
                "topic=%s partition=%d offset=%d value=%s", msg.topic, msg.partition, msg.offset, msg.value
            )
            messages.append({"topic": msg.topic, "partition": msg.partition, "offset": msg.offset, "value": msg.value})
            if len(messages) >= max_messages:
                break
        consumer.commit()
        consumer.close()
    except KafkaError as exc:
        return JsonResponse({"error": str(exc)}, status=502)

    return JsonResponse({"consumed": len(messages), "messages": messages})
