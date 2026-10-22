#!/usr/bin/env bash
# ==============================================================================
# Build Script for Render Deployment
# ==============================================================================

# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "📦 Upgrading pip and setuptools (ensures pkg_resources is available)..."
pip install --upgrade pip setuptools

echo "📦 Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

echo "🎨 Collecting static files (WhiteNoise)..."
python manage.py collectstatic --no-input

echo "🗄️ Running database migrations..."
python manage.py migrate

echo "👤 Initializing admin user (admin / admin123456) and test data..."
python manage.py setup_test_data --student-count 100

echo "✅ Build completed successfully!"
