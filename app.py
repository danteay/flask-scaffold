"""Application entry point"""

import os

from src.server import app


def main():
    """Start application"""

    port = os.getenv("PORT", "8000")
    app.run("0.0.0.0", port=port)


if __name__ == '__main__':
    main()
