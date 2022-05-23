from threading import Timer
# import streamlit as st
# from streamlit.script_run_context import add_script_run_ctx

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        """_summary_
            - init RepeatedTimer object
        Args:
            interval (int): seconds
            function (obj): function object
        """
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)
    
    def _get_return(self):
        return self.function(*self.args, **self.kwargs)
    
    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            # st.script_run_context.add_script_run_ctx(self._timer) 
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False