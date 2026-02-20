import logging
from models.proto import surtr_pb2
from typing import Callable, Dict

logger = logging.getLogger(__name__)

Augmentor = Callable[[surtr_pb2.SurtrMessage], None]

class CommandRegistry:
    def __init__(self):
        self._registry: Dict[int, Augmentor] = {
            0x01: self._apply_0x01,
        }

    def augment_cmd_instance(self, cmd_instance: surtr_pb2.SurtrMessage, cmd_id: int) -> surtr_pb2.SurtrMessage | None:
        try:
            fn = self._registry.get(cmd_id)
            if not fn:
                return None
            fn(cmd_instance)
            return cmd_instance
        except Exception as e:
            logger.error(f"Error while augmenting command instance. {e}")
            return None

    def _apply_0x01(self, ac_id: str, value: int, cmd_instance: surtr_pb2.SurtrMessage):
        cmd_instance.sw_ctrl.id = ac_id
        cmd_instance.sw_ctrl.state = value

    def list_available_commands(self):
        return {k: v.__name__ for k, v in self._registry.items()}
