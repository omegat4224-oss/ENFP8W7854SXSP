#!/usr/bin/env python3
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
FILES = [
    "README.md",
    "chat_archive.json",
    "ip_manifest.json",
    "system_fingerprint.json",
    "provenance.log",
]


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def refresh_json_metadata(filename: str) -> dict:
    path = BASE_DIR / filename
    payload = json.loads(load_text(path))
    payload["timestamp"] = utc_now_iso() if payload.get("timestamp") in (None, "AUTO") else payload.get("timestamp")
    payload["hash"] = sha256_text(json.dumps(payload, sort_keys=True, ensure_ascii=False))
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return payload


def build() -> str:
    refreshed = {
        "chat_archive.json": refresh_json_metadata("chat_archive.json"),
        "ip_manifest.json": refresh_json_metadata("ip_manifest.json"),
        "system_fingerprint.json": refresh_json_metadata("system_fingerprint.json"),
    }

    file_hashes = {}
    combined_parts = []
    for filename in FILES:
        content = load_text(BASE_DIR / filename)
        combined_parts.append(content)
        file_hashes[filename] = sha256_text(content)

    timestamp = utc_now_iso()
    combined_hash = sha256_text("".join(combined_parts))
    genesis = {
        "timestamp": timestamp,
        "files": FILES,
        "file_hashes": file_hashes,
        "combined_hash": combined_hash,
        "refreshed_payloads": refreshed,
    }
    genesis_hash = sha256_text(json.dumps(genesis, sort_keys=True, ensure_ascii=False))

    (BASE_DIR / "GENESIS_HASH.txt").write_text(genesis_hash + "\n", encoding="utf-8")
    (BASE_DIR / "genesis.json").write_text(
        json.dumps({"genesis": genesis, "genesis_hash": genesis_hash}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"GENESIS HASH: {genesis_hash}")
    return genesis_hash


if __name__ == "__main__":
    build()
