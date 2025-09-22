import csv
import secrets

from bip_utils import Bip39SeedGenerator, Bip44, Bip44Changes, Bip44Coins
from mnemonic import Mnemonic


def generate_wallets(filename: str, count: int = 1):
    mnemo = Mnemonic()

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["address", "private_key", "seed_phrase"])

        for _ in range(count):
            entropy = secrets.token_bytes(16)
            seed_phrase = mnemo.to_mnemonic(entropy)
            seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()
            bip44_wallet = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)
            account = (
                bip44_wallet.Purpose()
                .Coin()
                .Account(0)
                .Change(Bip44Changes.CHAIN_EXT)
                .AddressIndex(0)
            )

            address = account.PublicKey().ToAddress()
            private_key = account.PrivateKey().Raw().ToHex()

            writer.writerow([address, private_key, seed_phrase])

            print(f"Address: {address}")


if __name__ == "__main__":
    generate_wallets("wallets.csv", 10)
