import os
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, send_from_directory, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.core.forms import FileUploadForm
from app.models import Podcast
from app.extensions import db

# Import our new service functions
from app.services.text_extractor import extract_text_from_file
from app.services.script_generator import generate_podcast_script
from app.services.audio_generator import generate_audio_from_script
from flask import send_file


core_bp = Blueprint('core_bp', __name__,
                  template_folder='../templates',
                  static_folder='../static')

@core_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = FileUploadForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        
        # Ensure upload folder exists
        upload_path = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_path, exist_ok=True)
        filepath = os.path.join(upload_path, filename)
        file.save(filepath)

        # --- Start the AI Pipeline ---
        
        # 1. Create a record in the database
        new_podcast = Podcast(original_filename=filename, author=current_user)
        db.session.add(new_podcast)
        db.session.commit()
        
        # 2. Extract Text
        text = extract_text_from_file(filepath)
        if not text:
            flash('Could not extract text from the file.', 'danger')
            new_podcast.status = 'failed'
            db.session.commit()
            return redirect(url_for('core_bp.dashboard'))

        # 3. Generate Script (For now, we run this synchronously)
        # In a true production app, this would be a background task (e.g., using Celery)
        script = generate_podcast_script(text)
        if script.startswith("Error:"):
            flash(f'AI script generation failed: {script}', 'danger')
            new_podcast.status = 'failed'
            db.session.commit()
            return redirect(url_for('core_bp.dashboard'))

        # 4. Generate Audio
        generated_folder = current_app.config['GENERATED_FOLDER']
        os.makedirs(generated_folder, exist_ok=True)
        audio_filename = f"{os.path.splitext(filename)[0]}_{new_podcast.id}.mp3"
        audio_filepath = os.path.join(generated_folder, audio_filename)
        
        success = generate_audio_from_script(script, audio_filepath)

        # 5. Update Database Record
        if success:
            new_podcast.status = 'completed'
            new_podcast.generated_audio_path = audio_filepath
            db.session.commit()
            flash('Your podcast has been successfully generated!', 'success')
        else:
            new_podcast.status = 'failed'
            db.session.commit()
            flash('Audio generation failed.', 'danger')

        return redirect(url_for('core_bp.dashboard'))

    # Fetch podcast history for the current user
    
    page = request.args.get('page', 1, type=int)
    pagination = Podcast.query.filter_by(user_id=current_user.id)\
                              .order_by(Podcast.created_at.desc())\
                              .paginate(page=page, per_page=5, error_out=False)
    user_podcasts = pagination.items

    return render_template('dashboard.html', title='Dashboard', form=form, podcasts=user_podcasts, pagination=pagination)

@core_bp.route('/download/<int:podcast_id>')
@login_required
def download_podcast(podcast_id):
    podcast = Podcast.query.get_or_404(podcast_id)

    # Ensure the podcast belongs to the current user
    if podcast.user_id != current_user.id:
        flash("You are not authorized to download this podcast.", "danger")
        return redirect(url_for('core_bp.dashboard'))

    if not podcast.generated_audio_path or not os.path.exists(podcast.generated_audio_path):
        flash("Generated audio not found.", "danger")
        return redirect(url_for('core_bp.dashboard'))

    return send_file(podcast.generated_audio_path, as_attachment=True)

@core_bp.route('/podcast/delete/<int:podcast_id>', methods=['POST'])
@login_required
def delete_podcast(podcast_id):
    """
    Deletes a podcast record from the database and its associated audio file.
    """
    # Find the podcast in the database or return a 404 error
    podcast = Podcast.query.get_or_404(podcast_id)

    # Security Check: Ensure the podcast belongs to the current user
    if podcast.author.id != current_user.id:
        flash('You do not have permission to delete this podcast.', 'danger')
        abort(403) # Forbidden

    try:
        # Check if an audio file exists and delete it from the server's filesystem
        if podcast.generated_audio_path and os.path.exists(podcast.generated_audio_path):
            os.remove(podcast.generated_audio_path)
            print(f"Deleted audio file: {podcast.generated_audio_path}")

        # Delete the record from the database
        db.session.delete(podcast)
        db.session.commit()
        flash('Podcast history entry has been successfully deleted.', 'success')

    except Exception as e:
        # If anything goes wrong, roll back the change and show an error
        db.session.rollback()
        flash(f'Error deleting podcast: {e}', 'danger')
        print(f"Error during podcast deletion: {e}")

    # Redirect the user back to the dashboard
    return redirect(url_for('core_bp.dashboard'))