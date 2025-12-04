import sys
from datetime import datetime
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QToolBar,
    QPushButton, QVBoxLayout, QWidget, QSizePolicy
)
from PyQt6.QtWebEngineWidgets import QWebEngineView

class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Python Web Browser")
        self.setGeometry(100, 100, 1000, 700) # x, y, width, height
        
        # 1. Main Widget and Layout
        container = QWidget()
        layout = QVBoxLayout(container)
        self.setCentralWidget(container)

        # 2. Browser Engine
        self.browser = QWebEngineView()
        # Set an initial homepage
        self.browser.setUrl(QUrl("https://www.google.com")) 
        
        # 3. Navigation Toolbar
        nav_toolbar = QToolBar("Navigation")
        self.addToolBar(nav_toolbar)
        
        # Back Button
        back_btn = QPushButton("<- Back")
        back_btn.clicked.connect(self.browser.back)
        nav_toolbar.addWidget(back_btn)
        
        # Forward Button
        forward_btn = QPushButton("Forward ->")
        forward_btn.clicked.connect(self.browser.forward)
        nav_toolbar.addWidget(forward_btn)

        # Reload Button
        reload_btn = QPushButton("Reload")
        reload_btn.clicked.connect(self.browser.reload)
        nav_toolbar.addWidget(reload_btn)

        # Home Button
        home_btn = QPushButton("Home")
        home_btn.clicked.connect(self.navigate_home)
        nav_toolbar.addWidget(home_btn)

        # 4. URL Bar
        self.url_bar = QLineEdit()
        # Connect the Enter key press to the navigate_to_url method
        self.url_bar.returnPressed.connect(self.navigate_to_url) 
        # Add the URL bar and make it expand to fill the space
        nav_toolbar.addWidget(self.url_bar)
        
        # 5. Connect Signal/Slot for URL updates
        # Update the URL bar when the browser navigates
        self.browser.urlChanged.connect(self.update_url_bar)

        # 6. Assemble the Layout (Web view and toolbar are already added)
        layout.addWidget(nav_toolbar)
        layout.addWidget(self.browser)
        
    def navigate_home(self):
        # Go to the initial homepage
        self.browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        # Get the text from the URL bar
        url_text = self.url_bar.text()
        
        # Ensure a proper scheme (like http:// or https://) is present
        if not url_text.startswith(('http://', 'https://')):
            url_text = 'http://' + url_text # Default to http://
            
        # Load the URL in the browser
        self.browser.setUrl(QUrl(url_text))

    def save_to_history(self, url):
        # Save the URL and timestamp to history.txt
        try:
            with open("history.txt", "a") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{timestamp} - {url}\n")
        except Exception as e:
            print(f"Error saving history: {e}")

    def update_url_bar(self, q):
        # Update the URL bar with the currently loaded page's URL
        # Convert QUrl object to a string and display it
        url_str = q.toString()
        self.url_bar.setText(url_str)
        self.save_to_history(url_str)

# Run the Application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleBrowser()
    window.show()
    sys.exit(app.exec())
