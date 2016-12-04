class ContextManagerMixin(object):
    """
    Used to "mixin" context manager functionality, where native @context_manager is not enough.
    This also simplifies the "on_success" handling (when context manager is exited from without
    and exception)

    attribute matching the name set in class attribute _in_context_attribute_name will be set to
    True once the context manager is entered into and flipped back to False once out.

    If method matching name set on _on_success_callback_name is present on the object, we call it
    every time this context manager is exited from without exception.
    Default method name is `on_success`

    example on_success method:
        def on_success(self):
            super(ContextManagerMixin, self).on_success()

    If method matching name set on _on_exit_callback_name is present on the object, we call it
    every time this context manager is exited from - through exception or without.
    Default method name is `on_exit`

    example on_exit method:
        def on_exit(self):
            super(ContextManagerMixin, self).on_exit()
    """

    def on_init(self, *args, **kwargs):
        pass

    def on_enter(self):
        pass

    def on_error(self, type, value, traceback):
        pass

    def on_exit(self):
        pass

    def on_success(self):
        pass

    def __init__(self, *args, **kwargs):
        super(ContextManagerMixin, self).__init__()
        self.is_in_context = False
        self.on_init(*args, **kwargs)

    def __enter__(self):
        self.is_in_context = True
        self.on_enter()
        return self

    def __exit__(self, type, value, traceback):
        self.is_in_context = False

        # if there was no error, call success handler
        try:
            if not type and not value:
                self.on_success()
            else:
                self.on_error(type, value, traceback)
        finally:
            self.on_exit()


class AsyncContextManagerMixin:
    """
    Used to "mixin" context manager functionality, where native async context_manager is not enough.
    This also simplifies the "on_success" handling (when context manager is exited from without
    and exception)

    attribute matching the name set in class attribute _in_context_attribute_name will be set to
    True once the context manager is entered into and flipped back to False once out.

    If method matching name set on _on_success_callback_name is present on the object, we call it
    every time this context manager is exited from without exception.
    Default method name is `on_success`

    example on_success method:

        async def on_success(self):
            super(ContextManagerMixin, self).on_success()
            await long_running_cleanup_fn()

    If method matching name set on _on_exit_callback_name is present on the object, we call it
    every time this context manager is exited from - through exception or without.
    Default method name is `on_exit`

    example on_exit method:

        async def on_exit(self):
            super(ContextManagerMixin, self).on_exit()
            await long_running_cleanup_fn()

    """

    def on_init(self, *args, **kwargs):
        pass

    async def on_enter(self):
        pass

    async def on_error(self, type, value, traceback):
        pass

    async def on_exit(self):
        pass

    async def on_success(self):
        pass

    def __init__(self, *args, **kwargs):
        self.is_in_context = False
        self.on_init(*args, **kwargs)

    async def __aenter__(self):
        self.is_in_context = True
        await self.on_enter()
        return self

    async def __aexit__(self, type, value, traceback):
        self.is_in_context = False

        # if there was no error, call success handler
        try:
            if not type and not value:
                await self.on_success()
            else:
                await self.on_error(type, value, traceback)
        finally:
            await self.on_exit()
