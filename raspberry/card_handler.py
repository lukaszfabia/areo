#!/usr/bin/env python3

# pylint: disable=no-member

import time
import RPi.GPIO as GPIO
from config import *
from mfrc522 import MFRC522


def rfid_read() -> tuple[list[int], int]:
    MIFAREReader = MFRC522()
    while True:
        (status, _) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        if status == MIFAREReader.MI_OK:
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            if status == MIFAREReader.MI_OK:
                num = sum(uid[i] << (i * 8) for i in range(len(uid)))
                print(f"Card read UID: {uid} > {num}")
                time.sleep(0.5)
                return uid, num


def health() -> None:
    print("\nThe RFID reader test.")
    print("Place the card close to the reader (on the right side of the set).")

    try:
        rfid_read()
        print("The RFID reader tested successfully.")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    health()
