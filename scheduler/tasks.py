from .create import scheduler
from threading import Lock

@scheduler.task(
    "interval",
    id="argocd controller",
    seconds=2,
    max_instances=1,
)
def task1():
    with scheduler.app.app_context():
        pass
    
        # test code
        # config = scheduler.app.config
        # lock = config['ARGOCD_EVENT_LOCK']
        # lock.acquire()
        # print("hello")
        # lock.release()
        # print(scheduler.app.config)