"""Script used to check ER rendering determinism across PYTHONHASHSEED values."""

import argparse
import hashlib
import os
import subprocess
import sys
from pathlib import Path


def build_env(seed: int) -> dict[str, str]:
    return {
        "HOME": str(Path.home()),
        "PATH": os.environ["PATH"],
        "PYTHONHASHSEED": str(seed),
        "PYTHONPATH": str(Path(__file__).resolve().parents[1]),
    }


def render_script() -> str:
    return """
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import declarative_base

from eralchemy.main import render_er

Base = declarative_base()


class ParentA(Base):
    __tablename__ = "parent_a"
    id = Column(String(), primary_key=True)


class ParentB(Base):
    __tablename__ = "parent_b"
    id = Column(String(), primary_key=True)


class Child(Base):
    __tablename__ = "child"
    id = Column(String(), primary_key=True)
    b_id = Column(String(), ForeignKey(ParentB.id))
    a_id = Column(String(), ForeignKey(ParentA.id))


out = render_er(Base, output=None, mode="dot")
print(out.decode() if isinstance(out, bytes) else out)
"""


def cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seeds",
        type=int,
        default=10,
        help="Number of hash seeds to test.",
    )
    args = parser.parse_args()

    outputs: dict[str, list[int]] = {}
    script = render_script()
    for seed in range(1, args.seeds + 1):
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            check=True,
            env=build_env(seed),
            text=True,
        )
        digest = hashlib.sha256(result.stdout.encode("utf-8")).hexdigest()
        outputs.setdefault(digest, []).append(seed)

    print(f"unique_outputs={len(outputs)}")
    for digest, seeds in sorted(outputs.items()):
        print(f"{digest} seeds={seeds}")


if __name__ == "__main__":
    cli()
