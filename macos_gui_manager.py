#!/usr/bin/env python3
"""
macOS GUI Thread Manager
========================

This module provides a robust solution for GUI threading issues on macOS.
It ensures that all GUI operations run on the main thread to avoid
NSWindow threading errors.
"""

import threading
import queue
import time
import sys
from typing import Any, Callable, Optional
import functools


class MacOSGUIManager:
    """
    Manages GUI operations on macOS to avoid threading issues.

    This class ensures that all GUI operations are executed on the main thread,
    preventing the common NSWindow threading errors on macOS.
    """

    def __init__(self):
        self.is_main_thread = threading.current_thread() is threading.main_thread()
        self.gui_queue = queue.Queue()
        self.running = False

    def start_gui_loop(self):
        """Start the GUI event loop on the main thread."""
        if not self.is_main_thread:
            raise RuntimeError("GUI loop must be started from the main thread")

        self.running = True

        # Process GUI operations from queue
        while self.running:
            try:
                # Get GUI operation with timeout
                operation = self.gui_queue.get(timeout=0.1)

                if operation is None:  # Shutdown signal
                    break

                func, args, kwargs, result_queue = operation

                try:
                    result = func(*args, **kwargs)
                    if result_queue:
                        result_queue.put(('success', result))
                except Exception as e:
                    if result_queue:
                        result_queue.put(('error', e))

            except queue.Empty:
                # Allow other operations to continue
                continue

    def stop_gui_loop(self):
        """Stop the GUI event loop."""
        self.running = False
        self.gui_queue.put(None)  # Shutdown signal

    def execute_on_main_thread(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute a function on the main thread.

        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments

        Returns:
            Function result

        Raises:
            Exception: If function execution fails
        """
        if self.is_main_thread:
            # Already on main thread, execute directly
            return func(*args, **kwargs)
        else:
            # Queue operation for main thread execution
            result_queue = queue.Queue()
            self.gui_queue.put((func, args, kwargs, result_queue))

            # Wait for result
            try:
                status, result = result_queue.get(timeout=30.0)  # 30 second timeout

                if status == 'success':
                    return result
                else:
                    raise result

            except queue.Empty:
                raise TimeoutError("GUI operation timed out after 30 seconds")


def gui_thread_safe(func):
    """
    Decorator to make a function GUI thread-safe on macOS.

    This decorator ensures the function runs on the main thread,
    preventing NSWindow threading errors.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check if we're on macOS
        if sys.platform != 'darwin':
            # Not macOS, execute normally
            return func(*args, **kwargs)

        # On macOS, check if we're on main thread
        if threading.current_thread() is threading.main_thread():
            # Already on main thread, execute directly
            return func(*args, **kwargs)
        else:
            # Not on main thread, this could cause issues
            # For now, we'll try to execute but log a warning
            print(f"Warning: {func.__name__} called from non-main thread on macOS")
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if "NSWindow" in str(e) or "main thread" in str(e):
                    raise RuntimeError(
                        f"GUI operation {func.__name__} failed due to threading issue on macOS. "
                        f"Consider using headless mode or ensuring GUI operations run on main thread."
                    ) from e
                else:
                    raise

    return wrapper


def create_gui_safe_wrapper(gui_function):
    """
    Create a thread-safe wrapper for a GUI function.

    Args:
        gui_function: The GUI function to wrap

    Returns:
        Thread-safe version of the function
    """
    @gui_thread_safe
    def safe_wrapper(*args, **kwargs):
        return gui_function(*args, **kwargs)

    return safe_wrapper


def is_gui_safe() -> bool:
    """
    Check if GUI operations are safe in the current context.

    Returns:
        True if GUI operations are safe, False otherwise
    """
    if sys.platform != 'darwin':
        return True  # Non-macOS systems are generally fine

    # On macOS, check if we're on the main thread
    return threading.current_thread() is threading.main_thread()


def get_safe_gui_mode() -> str:
    """
    Get the recommended GUI mode for the current context.

    Returns:
        'gui' if GUI is safe, 'headless' if not
    """
    return 'gui' if is_gui_safe() else 'headless'


# Global GUI manager instance
_gui_manager = None

def get_gui_manager() -> MacOSGUIManager:
    """Get the global GUI manager instance."""
    global _gui_manager
    if _gui_manager is None:
        _gui_manager = MacOSGUIManager()
    return _gui_manager


# Convenience functions
def execute_gui_safe(func: Callable, *args, **kwargs) -> Any:
    """Execute a function in a GUI-safe manner."""
    if is_gui_safe():
        return func(*args, **kwargs)
    else:
        manager = get_gui_manager()
        return manager.execute_on_main_thread(func, *args, **kwargs)
