
def read_next_frame_and_apply(ser: serial.Serial, empty_tel_object: TelemetryInput, empty_gcs_state_object: GCSState) -> bool:
    try:
        frame = read_usb_frame(ser)
        if not frame:
            return False
      
        usb_id, usb_pkt_timestamp, usb_pkt_payload = frame
        if not usb_id or not usb_pkt_payload:
            return False

        decode_pkt = DECODERS.get(usb_id)
        if decode_pkt:
            if usb_id == 0x700:
                decode_pkt(usb_pkt_payload, empty_gcs_state_object)
                apply_unix_timestamp(usb_pkt_timestamp, empty_gcs_state_object)
            else:
                decode_pkt(usb_pkt_payload, empty_tel_object)
                apply_unix_timestamp(usb_pkt_timestamp, empty_tel_object)
            return True
       
        return False
    except Exception as e:
        logger.error(f"Error while reading and applying bytes to target object. {e}")
        return None