from .create import scheduler

@scheduler.task(
    "interval",
    id="argocd controller",
    seconds=1,
    max_instances=1,
)
def task1():
    with scheduler.app.app_context():
        pass
        # print(scheduler.app.config)