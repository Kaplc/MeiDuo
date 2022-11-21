from celery_tasks.main import celery_app


@celery_app.task(name='ab')
def test(a, b):
    print(123)
    res = a + b
    return res


if __name__ == '__main__':
    add = test.delay(1, 2)
    print(add)
