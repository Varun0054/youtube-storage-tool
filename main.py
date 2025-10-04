#!/usr/bin/env python3
"""
YouTube Storage Tool - Main Entry Point

A tool for encoding files into video format and decoding them back.
This allows storing files as videos that can be uploaded to platforms like YouTube.
"""

from gui.main_window import MainWindow


def main():
    """Main entry point of the application."""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
