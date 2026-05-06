import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

KEY = b'thermalopenssl.h'
IV  = b'thermalopenssl.h'


def decrypt_file(src_path: str, dst_path: str) -> None:
    with open(src_path, 'rb') as f_in:
        ciphertext = f_in.read()

    size = len(ciphertext)
    if size == 0:
        raise ValueError("File is empty.")
    if size % 16 != 0:
        raise ValueError(
            f"File size {size} bytes is not a multiple of 16 (AES block size). "
            "File may be corrupt or not AES-CBC encrypted."
        )

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    with open(dst_path, 'wb') as f_out:
        f_out.write(plaintext)


def encrypt_file(src_path: str, dst_path: str) -> None:
    with open(src_path, 'rb') as f_in:
        plaintext = f_in.read()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(KEY), modes.CBC(IV), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    with open(dst_path, 'wb') as f_out:
        f_out.write(ciphertext)


def batch_decrypt(src_folder: str = 'encrypted', dst_folder: str = 'decrypted') -> None:
    """Decrypt all .conf files from src_folder into dst_folder."""
    os.makedirs(dst_folder, exist_ok=True)
    files = sorted(f for f in os.listdir(src_folder) if f.lower().endswith('.conf'))
    if not files:
        print(f"[WARN] No .conf files found in '{src_folder}'.")
        return

    ok, skipped = 0, []
    for filename in files:
        src = os.path.join(src_folder, filename)
        dst = os.path.join(dst_folder, filename)
        try:
            decrypt_file(src, dst)
            print(f"[DECRYPTED] {src}  ->  {dst}")
            ok += 1
        except Exception as e:
            print(f"[SKIP]      {src}  —  {e}")
            skipped.append(filename)

    print(f"\nDone. {ok} file(s) decrypted to '{dst_folder}'.", end="")
    if skipped:
        print(f" {len(skipped)} file(s) skipped: {', '.join(skipped)}")
    else:
        print()


def batch_encrypt(src_folder: str = 'decrypted', dst_folder: str = 'output') -> None:
    """Encrypt all .conf files from src_folder into dst_folder."""
    os.makedirs(dst_folder, exist_ok=True)
    files = sorted(f for f in os.listdir(src_folder) if f.lower().endswith('.conf'))
    if not files:
        print(f"[WARN] No .conf files found in '{src_folder}'.")
        return

    ok, skipped = 0, []
    for filename in files:
        src = os.path.join(src_folder, filename)
        dst = os.path.join(dst_folder, filename)
        try:
            encrypt_file(src, dst)
            print(f"[ENCRYPTED] {src}  ->  {dst}")
            ok += 1
        except Exception as e:
            print(f"[SKIP]      {src}  —  {e}")
            skipped.append(filename)

    print(f"\nDone. {ok} file(s) encrypted to '{dst_folder}'.", end="")
    if skipped:
        print(f" {len(skipped)} file(s) skipped: {', '.join(skipped)}")
    else:
        print()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Batch encrypt/decrypt .conf files for mi_thermald configs'
    )
    parser.add_argument(
        'mode',
        choices=['decrypt', 'encrypt'],
        help=(
            "decrypt: read .conf from 'encrypted/', write plaintext to 'decrypted/'\n"
            "encrypt: read .conf from 'decrypted/', write ciphertext to 'output/'"
        )
    )
    args = parser.parse_args()

    if args.mode == 'decrypt':
        batch_decrypt()
    else:
        batch_encrypt()
