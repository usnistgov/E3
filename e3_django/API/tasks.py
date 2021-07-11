from celery import shared_task


@shared_task
def analyze(input):
    """
    Main task that runs analysis.

    :param input: The json input the user provides.
    :return: The json output created by the analysis.
    """

    return {}
