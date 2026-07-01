import signal


def install_shutdown(runtime):

    signal.signal(

        signal.SIGINT,

        lambda *_: runtime.shutdown(),

    )

    signal.signal(

        signal.SIGTERM,

        lambda *_: runtime.shutdown(),

    )
