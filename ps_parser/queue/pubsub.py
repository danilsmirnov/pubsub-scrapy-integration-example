import logging
from abc import ABC, abstractmethod
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1, storage


"""
utils for gcloud Pub/Sub https://cloud.google.com/pubsub
"""


# TODO(developer)
# project_id = "your-project-id"
# topic_id = "your-topic-id"
# subscription_id = "your-subscription-id"
# Number of seconds the subscriber should listen for messages
# timeout = 5.0

LOG_LEVEL = logging.INFO
logging.basicConfig(
    format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")


class PublisherMeta(ABC):
    __slots__ = ()
    publisher: pubsub_v1.PublisherClient
    topic_path = None

    @abstractmethod
    def publish_message(self, *args, **kwargs):
        """Method for publishing multiple messages to a Pub/Sub topic."""
        raise NotImplementedError('{}.publish is not defined'.format(self.__class__.__name__))

    @abstractmethod
    def create_topic(self, *args, **kwargs):
        """Method for creating a new Pub/Sub topic."""
        raise NotImplementedError('{}.create_topic is not defined'.format(self.__class__.__name__))

    @abstractmethod
    def delete_topic(self, *args, **kwargs):
        """Method for deleting an existing Pub/Sub topic."""
        raise NotImplementedError('{}.delete_topic is not defined'.format(self.__class__.__name__))

    @abstractmethod
    def detach_subscription(self, *args, **kwargs):
        """Method for detaching a subscription from a topic and drops all messages retained in it."""
        raise NotImplementedError('{}.detach_subscription is not defined'.format(self.__class__.__name__))


class SubscriberMeta(ABC):
    __slots__ = ()
    subscriber: pubsub_v1.SubscriberClient
    subscription_path: None
    streaming_pull_future = None

    @abstractmethod
    def on_message(self, *args, **kwargs):
        def callback(*args, **kwargs):
            pass

        raise NotImplementedError('{}.on_message callback is not defined'.format(self.__class__.__name__))

    @abstractmethod
    def list_subscriptions_in_topic(self, *args, **kwargs):
        """Lists all subscriptions for a given topic."""
        raise NotImplementedError(
            '{}.list_subscriptions_in_topic callback is not defined'.format(self.__class__.__name__))

    @abstractmethod
    def list_subscriptions_in_project(self, *args, **kwargs):
        """Lists all subscriptions in the current project."""
        raise NotImplementedError(
            '{}.list_subscriptions_in_project callback is not defined'.format(self.__class__.__name__))

    @abstractmethod
    def create_subscription(self, *args, **kwargs):
        """Create a new pull subscription on the given topic."""
        raise NotImplementedError('{}.create_subscription callback is not defined'.format(self.__class__.__name__))

    @abstractmethod
    def delete_subscription(self, *args, **kwargs):
        """Deletes an existing Pub/Sub topic."""
        raise NotImplementedError('{}.delete_subscription callback is not defined'.format(self.__class__.__name__))


class Publisher(PublisherMeta):

    def delete_topic(self, *args, **kwargs):
        pass

    def detach_subscription(self, *args, **kwargs):
        pass

    def create_topic(self, *args, **kwargs):
        pass

    def __init__(self, project_id, topic_id):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(project_id, topic_id)

    def publish_message(self):
        for n in range(1, 10):
            data = f'Message number {n}'
            data = data.encode('utf-8')
            future = self.publisher.publish(self.topic_path, data)
            print(future.result())
        print(f'published messages to {self.topic_path}.')


class Subscriber(SubscriberMeta):
    def list_subscriptions_in_project(self, *args, **kwargs):
        pass

    def create_subscription(self, *args, **kwargs):
        pass

    def delete_subscription(self, *args, **kwargs):
        pass

    def list_subscriptions_in_topic(self, *args, **kwargs):
        pass

    def __init__(self, project_id, subscription_id):
        self.subscriber = pubsub_v1.SubscriberClient()
        self.subscription_path = self.subscriber.subscription_path(project_id, subscription_id)

    def on_message(self):
        def callback(message: pubsub_v1.subscriber.message.Message) -> None:
            print(f'recieved {message}')
            message.ack()

        self.streaming_pull_future = self.subscriber.subscribe(self.subscription_path, callback=callback)
        print(f'listening for messages on {self.subscription_path}..\n')
        with self.subscriber:
            try:
                self.streaming_pull_future.result(timeout=5.0)
            except TimeoutError:
                self.streaming_pull_future.cancel()
                self.streaming_pull_future.result()


def implicit():
    """for auth"""
    storage_client = storage.Client()  # .from_service_account_json('../../gcloud-credentials.json')
    buckets = list(storage_client.list_buckets())
    print(buckets)


def bindable(func):
    """
    Javascript function.bind() analogue, using by decorator
    :param func: function to bind
    :return: wrapped
    """

    def wrapper(*args, **kwargs):
        def inner(*a, **kw):
            return func(*args, *a, **kwargs, **kw)

        return inner

    func.bind = wrapper
    return func


def get_logger(name: str, level: int) -> logging.Logger:
    """
    Creates logger
    :param name: logger name
    :param level: integer or logging.LEVEL
    :return: configured logger
    """
    logger = logging.getLogger(name)
    if not level:
        logger.setLevel(LOG_LEVEL)
    else:
        logger.setLevel(level)
    return logger