"""
Character set management and selection logic for Matrix rain effect.

Handles random character selection from the research-identified character pool.
"""

import random
from typing import Final

from . import config


class CharacterPool:
    """
    Manages the character set used for the Matrix rain effect.

    Research findings: "Half-width katakana characters combined with
    Latin letters and numerals" from the 1999 Matrix film.

    Using __slots__ to reduce memory overhead.
    """

    __slots__ = ('use_unicode', 'pool')

    def __init__(self, use_unicode: bool = True):
        """
        Initialize character pool.

        Args:
            use_unicode: If True, use katakana characters. If False, use ASCII only.
        """
        self.use_unicode = use_unicode
        # Optimized: Convert string to tuple for faster random.choice()
        pool_str = config.CHARACTER_POOL if use_unicode else config.ASCII_POOL
        self.pool = tuple(pool_str)

    def get_random_char(self) -> str:
        """
        Select a random character from the pool.

        Research: "Uniform distribution across character pool"

        Returns:
            Random character string
        """
        return random.choice(self.pool)

    def get_random_sequence(self, length: int) -> list[str]:
        """
        Generate a sequence of random characters.

        Args:
            length: Number of characters to generate

        Returns:
            List of random characters
        """
        # Optimized: Use random.choices() for better performance
        return random.choices(self.pool, k=length)


# Global character pool instance
_pool: CharacterPool | None = None


def initialize_pool(use_unicode: bool = True) -> None:
    """
    Initialize the global character pool.

    Args:
        use_unicode: Whether to use Unicode katakana characters
    """
    global _pool
    _pool = CharacterPool(use_unicode)


def get_random_char() -> str:
    """
    Get a random character from the global pool.

    Returns:
        Random character string

    Raises:
        RuntimeError: If pool not initialized
    """
    if _pool is None:
        raise RuntimeError("Character pool not initialized. Call initialize_pool() first.")
    return _pool.get_random_char()


def get_random_sequence(length: int) -> list[str]:
    """
    Generate a sequence of random characters from the global pool.

    Args:
        length: Number of characters to generate

    Returns:
        List of random characters

    Raises:
        RuntimeError: If pool not initialized
    """
    if _pool is None:
        raise RuntimeError("Character pool not initialized. Call initialize_pool() first.")
    return _pool.get_random_sequence(length)
