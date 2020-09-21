# rover

This is a learning repository for my son and our project to create a 3D printed rover

## Hologram How To:

https://www.hackster.io/hologram/hologram-python-sdk-receiving-data-bccf4c

1. Read device key `import os\os.environ['HOLOGRAM_DEVICE_KEY']`
1. https://hologram.io/docs/reference/cloud/python-sdk/
    1. First do the `.openReceiveSocket()`
    1. Next do the `.popReceivedMessage()` with the event.
