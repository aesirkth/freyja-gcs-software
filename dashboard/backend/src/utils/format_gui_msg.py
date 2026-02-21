import logging

logger = logging.getLogger(__name__)

def format_gui_msg(msg):
    try:
        if msg.value0:
            pass

        elif msg.value1:
            # Logic for value 1
            pass

        elif msg.value2:
            # Logic for value 2
            pass

        elif msg.value3:
            # Logic for value 3
            pass

        elif msg.value4:
            # Logic for value 4
            pass

        elif msg.value5:
            # Logic for value 5
            pass

        elif msg.value6:
            # Logic for value 6
            pass

        elif msg.value7:
            # Logic for value 7
            pass

        elif msg.value8:
            # Logic for value 8
            pass

        elif msg.value9:
            # Logic for value 9
            pass

        elif msg.value10:
            # Logic for value 10
            pass

        elif msg.value11:
            # Logic for value 11
            pass

        else:
            # Catch-all for undefined values
            pass

    except Exception as e:
        logger.error(f"Error while formatting GSE data. {e}")