"""
Hospital Management System - Application Entry Point
Main application launcher
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.views.login import LoginWindow
from app.views.dashboard import Dashboard
from app.services.auth_service import AuthService
from app.utils.db_connector import DatabaseConnector


def main():
    """Main application entry point"""
    try:
        # Initialize database connector
        db_connector = DatabaseConnector()
        
        # Initialize authentication service
        auth_service = AuthService(db_connector)
        
        def on_login_success(user):
            """Callback function after successful login"""
            # Open dashboard
            dashboard = Dashboard(user, auth_service, db_connector)
            dashboard.run()
        
        # Show login window
        login_window = LoginWindow(auth_service, on_login_success)
        login_window.run()
        
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
