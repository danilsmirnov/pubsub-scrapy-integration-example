from queue.pubsub import Publisher, Subscriber, Mediator

class MockObject:
    name = 'mock object'



if __name__ == '__main__':
    mock_object = MockObject
    mediator = Mediator()
    subscriber = Subscriber(mediator)
    subscriber.publisher.attach_to_object(mock_object)
    subscriber.send_message('Hello, World!')
    subscriber.publisher.publish('connection', print(mock_object.name ,'connected'))
