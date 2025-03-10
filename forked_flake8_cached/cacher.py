import hashlib
import marshal
import os
from typing import cast

import flake8.checker as f8checker


Results = tuple[str, f8checker.Results, dict[str, int]]


class Cacher:
    """Class to implement saving/loading cache for given file."""

    def __init__(self, file_name: str, cache_path: str) -> None:
        """Init cache class for the given file."""
        self.file_name = file_name
        checksum = hashlib.md5(file_name.encode())  # nosec
        self.cache_path = os.path.join(cache_path, str(checksum.hexdigest()))

    def get(self) -> Results | None:
        """Get cached result from the cache_path if available and valid."""
        if not os.path.exists(self.cache_path):
            return None
        with open(self.cache_path, "rb") as fr:
            mtime, results = marshal.load(fr)  # nosec
            # if the mtime doesn't change then return cache.
            # otherwise it is invalid
            current_mtime = os.path.getmtime(self.file_name)
            if mtime == current_mtime:
                return cast(Results, results)
        return None

    def save(self, results: Results) -> None:
        """Save the given result to the cache file."""
        with open(self.cache_path, "wb") as fw:
            current_mtime = os.path.getmtime(self.file_name)
            marshal.dump((current_mtime, results), fw)
