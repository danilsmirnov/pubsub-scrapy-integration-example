import logging



LOG_LEVEL = logging.INFO
logging.basicConfig(
    format="%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")


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


class Publisher:
    """
    Simple class for publisher
    """
    def __init__(self):
        self.log = get_logger('publisher', LOG_LEVEL)
        self.event_channel = list()
        self.log.debug('publisher inited')

    def subscribe(self, event, handler, context):
        if not context:
            context = handler
            self.log.warning('not context')
        # handler = bindable(handler)
        sub = {
            'event': event,
            'handler': handler.bind(context)
        }
        self.event_channel.append(sub)

    def publish(self, event, args):
        for topic in self.event_channel:
            if topic['event'] == event:
                topic['handler'](args)


class Subscriber:
    """
    Simple class for subscriber
    """
    def __init__(self, publisher: Publisher):
        self.log = get_logger('subscriber', LOG_LEVEL)
        self.publisher = publisher
        self.publisher.subscribe('message', self.emit_message, self)
        self.log.debug('chat inited')

    @bindable
    def emit_message(self, message: str):
        print('user sent message', message)

    def send_message(self, message: str):
        self.log.debug('sending message')
        self.publisher.publish('message', message)


class Mediator(Publisher):
    """

    """
    def __init__(self):
        super().__init__()

    def attach_to_object(self, obj: Publisher):
        obj.event_channel = list()
        obj.publish = self.publish
        obj.subscribe = self.subscribe

