import logging
from src.state.cmd_queue import cmd_queue
from src.core.cmd_transport import CommandTransport
from src.core.cmd_registry import CommandRegistry
from models.proto import surtr_pb2
import asyncio
import json

logger = logging.getLogger(__name__)

async def cmd_controller(command_transport: CommandTransport, command_registry: CommandRegistry) -> None:
    try:
        try:
            cmd = await cmd_queue.get()
            cmd_dict = json.loads(cmd)
            empty_cmd_instance = surtr_pb2.SurtrMessage()
            payload: surtr_pb2.SurtrMessage  = command_registry.augment_cmd_instance(cmd_dict["id"], cmd_dict["status"], empty_cmd_instance)
            if isinstance(payload, surtr_pb2.SurtrMessage):
                res = command_transport.write(payload)
                if not isinstance(res, int):
                    raise ValueError
            else:
                print("wrong type")

            await asyncio.sleep(0)
        except asyncio.QueueEmpty:
            print("No command in queue")
            logger.debug("No registered commands in the command queue.")

    except Exception as e:
        logger.error(f"Error while calling command transport service: {e}")
