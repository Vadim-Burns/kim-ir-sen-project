import inject


def DI():
    def di_configuration(binder):
        pass

    inject.configure_once(di_configuration)
