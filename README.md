# PyCtrlD

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A unofficial Python client library for the [Control D](https://controld.com/) API.

## What not supported?

Organizations endpoint and features are not tested and may not work as expected.

## Installation

```bash
pip install pyctrld
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv add pyctrld
```

## Quick Start

```python
from pyctrld import ControlDApi

# Initialize the API client
api = ControlDApi(token="your_api_token_here")

# List all devices
devices = api.devices.list_all_devices()
for device in devices:
    print(f"Device: {device.name} - {device.status}")

# Get account information
account = api.account.user_data()
print(f"Account: {account.email}")

# List all profiles
profiles = api.profiles.profiles.list()
for profile in profiles:
    print(f"Profile: {profile.name}")

# Create a new device
from pyctrld import CreateDeviceFormData

new_device = api.devices.create_device(
    data=CreateDeviceFormData(
        name="My DNS Device",
        icon="router",
        profile_id="PK123456"
    )
)
print(f"Created device with ID: {new_device.device_id}")
```

## Disclaimer

This is an **unofficial** library and is not affiliated with, officially maintained by, or endorsed by Control D. Use at your own risk.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [Control D Website](https://controld.com/)
- [Control D API Documentation](https://docs.controld.com/reference/get-started)
- [PyCtrlD GitHub Repository](https://github.com/xenolex/PyCtrlD)

## Support

If you encounter any issues or have questions:

1. Check the [GitHub Issues](https://github.com/xenolex/PyCtrlD/issues)
2. Review the [Control D API Documentation](https://docs.controld.com/reference/get-started)
3. Open a new issue with detailed information about your problem
