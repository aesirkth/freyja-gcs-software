import logging
from src.state.cmd_queue import cmd_queue
from src.core.cmd_transport import CommandTransport
from src.core.cmd_registry import CommandRegistry
from models.proto import surtr_pb2
import asyncio

logger = logging.getLogger(__name__)

async def cmd_controller(command_transport: CommandTransport, command_registry: CommandRegistry) -> None:
    try:
        try:
            cmd = cmd_queue.get_nowait()
            print(f"Latest command: {cmd_id}")
        except asyncio.QueueEmpty:
            await cmd_queue.put(1)
            cmd_id = cmd_queue.get_nowait()
            logger.debug("No registered commands in the command queue.")

        print(cmd)
        empty_cmd_instance = surtr_pb2.SurtrMessage()
        payload: surtr_pb2.SurtrMessage  = command_registry.augment_cmd_instance(cmd["id"], cmd["value"], empty_cmd_instance, cmd_id)
        if isinstance(payload, surtr_pb2.SurtrMessage):
            res = command_transport.write(payload)
            if not isinstance(res, int):
                raise ValueError
    except Exception as e:
        logger.error(f"Error while calling command transport service: {e}")
