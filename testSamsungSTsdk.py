from pysmartthings import SmartThings
import asyncio

async def push_notification(device_id, message):
    token = "YOUR_SMARTTHINGS_TOKEN"
    api = SmartThings(token)

    try:
        devices = await api.devices()
        device = next((d for d in devices if d.device_id == device_id), None)

        if device:
            await device.send_notification(message)
            print(f"Notification sent to device: {device.label}")
        else:
            print(f"Device with ID {device_id} not found")
    except Exception as e:
        print(f"Error sending notification: {str(e)}")

async def main():
    # Samsung TV device ID
    tv_device_id = "YOUR_TV_DEVICE_ID"
    
    # Samsung Smart Watch device ID
    watch_device_id = "YOUR_WATCH_DEVICE_ID"

    # Message to send
    message = "Hello from SmartThings!"

    # Send notification to TV
    await push_notification(tv_device_id, message)

    # Send notification to Smart Watch
    await push_notification(watch_device_id, message)

if __name__ == "__main__":
    asyncio.run(main())
