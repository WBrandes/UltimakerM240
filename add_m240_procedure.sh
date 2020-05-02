#!/usr/bin/env bash

mv takePictureStep.py /usr/share/griffin/griffin/printer/procedures/takePictureStep.py

sed -i.json '/"M400": {"procedure": "WAIT_FOR_QUEUE_TO_BE_EMPTY"},/a\        "M240": {"procedure": "TAKE_PICTURE"},' /usr/share/griffin/griffin/machines/um3.json

sed -i.json '/\"PRIME_NOZZLE\": \[\"pre_and_post_print.primeNozzleProcedure.PrimeNozzleProcedure\"\],/i\        "TAKE_PICTURE": ["genericProcedure.GenericProcedure",\n            ["TAKE_PICTURE", "takePictureStep.TakePictureStep"]],' /usr/share/griffin/griffin/machines/um3.json

sed -i.conf 's/MOUNTOPTIONS="ro,/MOUNTOPTIONS="/g' /etc/usbmount/usbmount.conf

#rm ./add_m240_procedure.sh
