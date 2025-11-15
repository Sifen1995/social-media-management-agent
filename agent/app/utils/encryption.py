"""
Token encryption utilities for securing social media access tokens.
"""
from cryptography.fernet import Fernet
from app.core.config import settings


class TokenEncryption:
    """Handle encryption and decryption of social media tokens."""

    def __init__(self):
        """Initialize the encryption handler with the secret key."""
        # Use the TOKEN_ENCRYPTION_KEY from settings
        # If not set, generate one (but this should be set in production)
        key = settings.TOKEN_ENCRYPTION_KEY.encode() if settings.TOKEN_ENCRYPTION_KEY else Fernet.generate_key()
        self.cipher = Fernet(key)

    def encrypt(self, token: str) -> str:
        """
        Encrypt a token string.

        Args:
            token: The plain text token to encrypt

        Returns:
            Encrypted token as a string
        """
        if not token:
            return ""

        encrypted_bytes = self.cipher.encrypt(token.encode())
        return encrypted_bytes.decode()

    def decrypt(self, encrypted_token: str) -> str:
        """
        Decrypt an encrypted token.

        Args:
            encrypted_token: The encrypted token string

        Returns:
            Decrypted token as plain text
        """
        if not encrypted_token:
            return ""

        try:
            decrypted_bytes = self.cipher.decrypt(encrypted_token.encode())
            return decrypted_bytes.decode()
        except Exception as e:
            # Log the error but don't expose details
            print(f"Token decryption failed: {e}")
            raise ValueError("Invalid or corrupted token")


# Global instance
token_encryption = TokenEncryption()


def encrypt_token(token: str) -> str:
    """Convenience function to encrypt a token."""
    return token_encryption.encrypt(token)


def decrypt_token(encrypted_token: str) -> str:
    """Convenience function to decrypt a token."""
    return token_encryption.decrypt(encrypted_token)
