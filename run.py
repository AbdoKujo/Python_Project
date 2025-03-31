#!/usr/bin/env python
from app import create_app
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create app with the specified configuration
app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=app.config['DEBUG'])

