#!/usr/bin/env python3
"""
NexDex Launcher - Entry point for packaged application
Opens the Flask dashboard automatically in the default browser
"""
import os
import sys
import webbrowser
import time
import threading
from pathlib import Path

# Add src and dashboard to path for packaged app
app_dir = getattr(sys, '_MEIPASS', str(Path(__file__).parent))
sys.path.insert(0, os.path.join(app_dir, 'dashboard'))
sys.path.insert(0, os.path.join(app_dir, 'src'))

# Import Flask app
from dashboard.app import create_app


def launch_browser(port=5000, retries=10):
    """Launch the default browser after server starts"""
    url = f'http://localhost:{port}'
    
    # Wait for server to be ready
    for i in range(retries):
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            
            if result == 0:
                # Server is ready
                time.sleep(0.5)
                webbrowser.open(url)
                print(f"🌐 Dashboard opened in browser: {url}")
                return
        except Exception:
            pass
        
        time.sleep(0.5)


def main():
    """Main entry point"""
    # Get port from environment or use default
    # Using 5555 instead of 5000 to avoid conflict with macOS Control Center
    port = int(os.environ.get('NEXDEX_PORT', 5555))
    
    # Create Flask app
    app = create_app()
    
    # Launch browser in background thread
    browser_thread = threading.Thread(
        target=launch_browser,
        args=(port,),
        daemon=True
    )
    browser_thread.start()
    
    # Print startup message
    print("╔═══════════════════════════════════════════════════════╗")
    print("║                                                       ║")
    print("║              🚀 NexDex Dashboard Starting             ║")
    print("║                                                       ║")
    print("╚═══════════════════════════════════════════════════════╝")
    print()
    print(f"📊 Dashboard: http://localhost:{port}")
    print()
    print("Press Ctrl+C to stop the server")
    print()
    
    # Run the Flask app
    try:
        app.run(
            host='127.0.0.1',
            port=port,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n✅ NexDex dashboard stopped.")
        sys.exit(0)


if __name__ == '__main__':
    main()
