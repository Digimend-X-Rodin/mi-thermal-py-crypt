![Mi Thermal](./img/banner_mithermal.png)
# mi-thermal-py-crypt

Python tool to decrypt and re-encrypt `mi-thermald` thermal configuration files (for Xiaomi, Redmi, and Poco devices). Encrypted configs can be decrypted for editing and then re-encrypted so `mi-thermald` accepts them.

## Features

- Decrypt all encrypted `.conf` files from an `encrypted/` folder into a `decrypted/` folder.
- Edit the decrypted `.conf` files in plain text.
- Re-encrypt all `.conf` files from `decrypted/` into an `output/` folder for use on the device.

## Requirements

- Linux (or Termux) with Python 3 installed.
- `cryptography` Python package.

```bash
# Install system dependencies (example for Debian/Ubuntu)
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

## Create and activate Python virtual environment (Linux)

It is recommended to use a virtual environment so this tool and its dependencies stay isolated from the system Python.

```bash
# Create virtual environment in .venv
python3 -m venv .venv

# Activate the virtual environment (bash/zsh)
source .venv/bin/activate

# Now install dependencies inside the venv
pip install cryptography
```

On Termux you can do:

```bash
pkg install python
pip install cryptography
```

## Project layout

```text
project-root/
├── thermal-crypt.py
├── encrypted/   # put encrypted *.conf files here
├── decrypted/   # decrypted *.conf files will be written here
└── output/      # re-encrypted *.conf files will be written here
```

The script will auto-create `decrypted/` and `output/` if they do not exist.

## Usage

Make sure you are in the same directory as `thermal-crypt.py` and (optionally) have your virtual environment activated.

### Decrypt all configs

Reads every `*.conf` from `encrypted/` and writes the decrypted versions to `decrypted/` with the same filenames.

```bash
python3 thermal-crypt.py decrypt
```

### Encrypt all configs

Reads every `*.conf` from `decrypted/` and writes encrypted versions to `output/` with the same filenames.

```bash
python3 thermal-crypt.py encrypt
```

## Notes

- Only files ending with `.conf` are processed; other files in the folders are ignored.
- The AES key and IV match the original C implementation so files remain compatible with `mi-thermald`.

## Original C implementation

- [mi-thermal-crypt](https://github.com/adithya2306/mi-thermal-crypt)
