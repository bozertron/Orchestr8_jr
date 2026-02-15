import json
import logging
from typing import Callable, Dict, Optional, Any
from pydantic import ValidationError

from orchestr8_next.city.contracts import InboundEvent, BaseCityEvent, InboundEventAdapter

# Define handler type
EventHandler = Callable[[InboundEvent], None]

class CityBridge:
    """
    Acts as the secure gateway between the Python backend and the Javascript 3D Frontend.
    Strictly validates all incoming payloads against Pydantic contracts.
    """
    
    def __init__(self):
        self._handlers: Dict[str, EventHandler] = {}
        self._logger = logging.getLogger("CityBridge")
        
    def register_handler(self, event_type: str, callback: EventHandler) -> None:
        """Register a callback for a specific event type discriminator."""
        self._handlers[event_type] = callback

    def process_message(self, raw_message: str) -> Optional[BaseCityEvent]:
        """
        Ingests a raw JSON string from the frontend.
        Validates structure and dispatches to registered handlers.
        Handles errors gracefully (R-04-01).
        """
        try:
            # 1. Primary Validation: Ensure it's valid JSON
            payload = json.loads(raw_message)
            
            # 2. Schema Validation: Pydantic Discriminated Union
            event_obj = InboundEventAdapter.validate_python(payload)
            
            # 3. Dispatch Logic
            self._dispatch(event_obj)
            
            return event_obj

        except json.JSONDecodeError as e:
            self._logger.error(f"[Contract Violation] Invalid JSON received: {e}")
            return None
            
        except ValidationError as e:
            self._logger.error(f"[Contract Violation] Schema validation failed: {e}")
            return None
            
        except Exception as e:
            self._logger.critical(f"[System Error] Unexpected bridge failure: {e}", exc_info=True)
            return None

    def _dispatch(self, event: BaseCityEvent) -> None:
        # Pydantic models with literal discriminators have the 'type' field
        event_type = getattr(event, "type", None)
        
        if event_type and event_type in self._handlers:
            try:
                self._handlers[event_type](event)
            except Exception as e:
                self._logger.error(f"Error in handler for {event_type}: {e}")
        else:
            self._logger.warning(f"No handler registered for event type: {event_type}")
