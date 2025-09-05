.PHONY: build-app
build-app:
	west build app

.PHONY: flash-app-usb
flash-app-usb:
	west flash --runner stm32cubeprogrammer --port=USB1