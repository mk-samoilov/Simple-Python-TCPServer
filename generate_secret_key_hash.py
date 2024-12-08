import hashlib

def generate_hash(text: str) -> str:
    return hashlib.sha256(str(text).encode()).hexdigest()

if __name__ == "__main__":
    key = input("input key: ")
    print(f"key: {key}")
    print(f"hash: {generate_hash(key)}")
