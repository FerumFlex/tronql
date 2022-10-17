class SessionProxy:
    def __init__(self, contextvar):
        self._contextvar = contextvar

    def __getattr__(self, attr):
        context = self._contextvar.get()
        assert context
        return getattr(context, attr)
