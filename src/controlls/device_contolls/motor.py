import time

from RPi import GPIO


class Motors:
    @staticmethod
    def rotate_list(lines_list: list[int]) -> None:
        for prd in lines_list:
            Motors.rotate(prd)

    @staticmethod
    def rotate(motor_num: int) -> None:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(motor_num, GPIO.OUT)
        GPIO.output(motor_num, True)
        time.sleep(5)
        GPIO.output(motor_num, False)
        GPIO.cleanup()
        time.sleep(5)
