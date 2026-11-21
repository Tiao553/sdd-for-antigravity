"""
AgentSpec Session Start Hook
Initializes session context and outputs harness telemetry confirmation.
"""
import sys

def on_session_start():
    # Diagnostic hook executed when a session starts with this plugin active
    pass

if __name__ == "__main__":
    on_session_start()
    sys.exit(0)
