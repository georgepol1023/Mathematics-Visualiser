"""Symbolic integration in a separate process, with a time limit.

SymPy can spend minutes (or forever) on integrals that have no simple closed
form. A thread can't be stopped, so the work runs in a child process that is
started in the background when the app opens and replaced if it runs over time.
The window stays responsive throughout.
"""

import multiprocessing
import time

TIMEOUT = 3.0  # seconds


def _serve(conn):
    """Child process: answer integration requests until the pipe closes."""
    import sympy as sp

    conn.send(("ready", None))
    while True:
        try:
            equation, var, lower, upper = conn.recv()
        except (EOFError, OSError):
            return
        try:
            x = sp.Symbol(var)
            value = sp.integrate(sp.sympify(equation), (x, lower, upper))
            try:
                conn.send(("ok", float(value.evalf())))
            except (TypeError, ValueError):
                conn.send(("no closed form", None))
        except Exception as e:  # report SymPy errors instead of dying
            conn.send(("error", f"{type(e).__name__}: {e}"))


class SymbolicWorker:
    """A reusable child process that evaluates definite integrals."""

    def __init__(self):
        self._ctx = multiprocessing.get_context("spawn")
        self._proc = None
        self._conn = None
        self._ready = False

    def start(self):
        """Start the child process (returns at once; SymPy loads in the background)."""
        if self._proc is not None and self._proc.is_alive():
            return
        self._conn, child = self._ctx.Pipe()
        self._proc = self._ctx.Process(target=_serve, args=(child,), daemon=True)
        self._proc.start()
        child.close()
        self._ready = False

    def stop(self):
        if self._proc is not None:
            self._proc.terminate()
            self._proc.join(1)
        if self._conn is not None:
            self._conn.close()
        self._proc = self._conn = None
        self._ready = False

    def _wait_ready(self, pump, limit=60.0):
        """Wait (pumping) for the child to finish importing SymPy."""
        deadline = time.monotonic() + limit
        while not self._ready and time.monotonic() < deadline:
            if self._conn.poll(0.02):
                self._ready = self._conn.recv()[0] == "ready"
            elif pump is not None:
                pump()
        return self._ready

    def integrate(self, equation, var, lower, upper, timeout=TIMEOUT, pump=None):
        """Return (status, value).

        status is "ok" (value is a float), "no closed form", "timeout" or "error"
        (value is a message). `pump` is called while waiting, so a Tk window can
        keep handling events.
        """
        request = (equation, var, float(lower), float(upper))
        try:
            self.start()
            if not self._wait_ready(pump):
                raise OSError("worker did not start")
            self._conn.send(request)
        except (OSError, EOFError):  # the child died; try once with a fresh one
            self.stop()
            self.start()
            if not self._wait_ready(pump):
                self.stop()
                return ("error", "could not start the SymPy worker")
            self._conn.send(request)
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self._conn.poll(0.02):
                try:
                    return self._conn.recv()
                except (OSError, EOFError):
                    self.stop()
                    return ("error", "worker stopped")
            if pump is not None:
                pump()
        # Too slow: stop it and have a fresh worker ready for next time
        self.stop()
        self.start()
        return ("timeout", None)
