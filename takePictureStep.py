import logging
import requests
from datetime import datetime

from griffin.printer.procedures.procedureStep import ProcedureStep

log = logging.getLogger(__name__.split(".")[-1])


class TakePictureStep(ProcedureStep):
    def __init__(self, key):
        super().__init__(key)

    def run(self):
        current_image = requests.get("http://localhost:8080/?action=snapshot")
        with open("/media/usb1/" + datetime.now().strftime("%Y%d%m%H%M%S") +".jpg", "wb") as f:
            for chunk in current_image:
                f.write(chunk)

    def getDurationEstimate(self):
        return 1
