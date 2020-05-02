# Ultimaker M240 Command

As Ultimaker printers, at least the Ultimaker 3 printer, do not implement the M240 command for taking pictures, the necessary code to do it is here.

This will have the printer save take an image with its camera and save it to the removable drive whenever the M240 command is called.

**MAKE SURE YOU BACK UP ANY OF THE FILES THE GUIDE SAYS TO EDIT BEFORE YOU TRY TO INSTALL ANYTHING**

To install, you can try putting the `add_m240_procedure.sh` and takePictureStep.py in a folder on your Ultimaker, and then running the `add_m240_procedure.sh` script. This is not recommended however, as the script could not be tested to due to the COVID-19 pandemic.

Instead, you can follow these steps to install the functionality manually:

1. Put the takePictureStep.py file in /usr/share/griffin/griffin/printer/procedures
2. Add the following lines to the um3.json file in /usr/share/griffin/griffin/machines:
```
"TAKE_PICTURE": ["genericProcedure.GenericProcedure",
    ["TAKE_PICTURE", "takePictureStep.TakePictureStep"]],
```
It should be added in the section for defining what scripts to call; a safe bet is to look for the `"WAIT_FOR_QUEUE_TO_BE_EMPTY"` procedure and add it after that. The segment should look something like:
```
"WAIT_FOR_QUEUE_TO_BE_EMPTY": ["genericProcedure.GenericProcedure",
            ["WAITING", "waitForQueueEmptyStep.WaitForQueueToBeEmptyStep"]
        ],
```

3. Then add
`"M240": {"procedure": "TAKE_PICTURE"},`
in with the other procedure definitions at the bottom of the file.

You'll also need to go into /etc/usbmount/usbmount.conf and remove the "ro" option to make the drive writable, and then un-plug and re-plug the drive.

Once all these steps are done, restart the printer and it should load the command properly. If the printer won't start up all the way, it's likely because something is wrong in the config file; try editing it to get the printer to start up again or replacing it with your backed-up file if worst comes to worst.

</br>

Additonally, in this repo is the `TimeLapseRetract.py` script. The default PostProcessing script Ultimaker Cura comes with does not use retraction, and so will cause a lot of stringing if you want to do a timelapse. Simply load the `TimeLapseRetract.py` script into Cura, and use that instead, as it does feature retraction. On Macs this is as simple as putting it in Library>Application Support>cura>[version #]>scripts
