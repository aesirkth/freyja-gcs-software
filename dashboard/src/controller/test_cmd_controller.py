from src.state.cmd_queue import cmd_queue
from src.core.cmd_transport import CommandTransport
import logging

logger = logging.getLogger(__name__)

def cmd_controller(command_transport: CommandTransport) -> None:
    try:
        payload = cmd_queue.g.get()
        if payload != None:
            res = command_transport.write(payload)
            if not isinstance(res, int):
                raise ValueError
    except Exception as e:
        logger.error(f"Error while calling command transport service: {e}")
