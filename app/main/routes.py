from flask import Blueprint, render_template
from app.extensions import db, bcrypt
# Create a Blueprint for our main pages
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='../templates', # Look for templates in the app/templates folder
    static_folder='../static'      # Look for static files in the app/static folder
)

@main_bp.route('/')
def index():
    """Serves the homepage."""
    return render_template('index.html', title='Welcome')

@main_bp.route('/about')
def about():
    """Serves the about page."""
    return render_template('about.html', title='About Us')