from typing import Callable, List, Optional, Any
from functools import reduce
from orchestr8_next.shell.contracts import State
from orchestr8_next.shell.actions import UIAction

# Middleware Type Definition
# Middleware: store -> (next_dispatch -> (action -> None))
Middleware = Callable[['Store'], Callable[[Callable[[UIAction], None]], Callable[[UIAction], None]]]

class Store:
    def __init__(self, reducer: Callable[[State, UIAction], State], initial_state: State, middlewares: List[Middleware] = None):
        if middlewares is None:
            middlewares = []
            
        self._reducer = reducer
        self._state = initial_state
        self._subscribers: List[Callable[[State], None]] = []
        
        # Compose middlewares
        # The chain starts with the base dispatch (reducer execution)
        # And wraps it with each middleware
        chain_link = self._base_dispatch
        
        # Initialize middlewares with the store instance
        # initialized_middlewares = [m(self) for m in middlewares]
        
        # Apply in reverse order so the first in the list is the outer-most wrapper
        for mw in reversed(middlewares):
            chain_link = mw(self)(chain_link)
            
        self.dispatch_function = chain_link

    def get_state(self) -> State:
        return self._state

    def dispatch(self, action: UIAction) -> None:
        """
        Public dispatch entry point.
        """
        self.dispatch_function(action)

    def _base_dispatch(self, action: UIAction) -> None:
        """
        The core dispatch logic: run reducer and notify subscribers.
        This is the end of the middleware chain.
        """
        self._state = self._reducer(self._state, action)
        self._notify_subscribers()

    def _notify_subscribers(self) -> None:
        for callback in self._subscribers:
            try:
                callback(self._state)
            except Exception as e:
                # Prevent subscriber errors from crashing the app
                print(f"Error in store subscriber: {e}")

    def subscribe(self, callback: Callable[[State], None]) -> None:
        self._subscribers.append(callback)
