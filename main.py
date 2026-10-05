#!/usr/bin/env python3
"""
YouTube Storage Tool - Main Entry Point

A tool for encoding files into video format and decoding them back.
This allows storing files as videos that can be uploaded to platforms like YouTube.

MVC Structure:
  models/      — Business logic (VideoEncoder, VideoDecoder)
  views/       — UI layout (MainView)
  controllers/ — Event handling & wiring (AppController)
"""

from views.main_view import MainView
from controllers.app_controller import AppController


def main():
    """Create the View, attach the Controller, start the event loop."""
    view = MainView()
    AppController(view)   # binds all button callbacks to the view
    view.mainloop()


if __name__ == "__main__":
    main()
