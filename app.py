from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from dotenv import load_dotenv
from supabase import create_client, Client
import requests

# Loads from .env
load_dotenv()
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_ANON_KEY")
tmdb_key = os.getenv("TMDB_API_KEY")
tmdb_base_url = os.getenv("TMDB_BASE_URL")

# Initialize Supabase client
supabase: Client = create_client(supabase_url, supabase_key)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure random key in production

# Get data from api
def tmdb_get(path, params=None):
    params = params or {}
    params["api_key"] = tmdb_key
    resp = requests.get(f"{tmdb_base_url}/{path}", params=params)
    resp.raise_for_status()
    return resp.json()

def tmdb_get_data():
    return {
        "popular_movies": tmdb_get("movie/popular", {"page": 1}),
        "top_rated_movies": tmdb_get("movie/top_rated", {"page": 1}),
        "popular_tv_shows": tmdb_get("tv/popular", {"page": 1}),
        "top_rated_tv_shows": tmdb_get("tv/top_rated", {"page": 1})
    }

@app.route('/')
def landing():
    tmdb_data = tmdb_get_data()
    return render_template('landing.html', tmdb_data=tmdb_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Authenticate user with Supabase
        try:
            response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            
            # Store user session data
            session['user'] = {
                'id': response.user.id,
                'email': response.user.email,
            }
            
            flash('Login successful!', 'success')
            return redirect(url_for('landing'))
            
        except Exception as e:
            flash(f'Login failed: {str(e)}', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        verify_password = request.form.get('verify-password')
        
        # Validate password match
        if password != verify_password:
            flash('Passwords do not match!', 'error')
            return render_template('signup.html')
        
        # Register user with Supabase
        try:
            response = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            flash('Registration successful! Please check your email to confirm your account.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            flash(f'Registration failed: {str(e)}', 'error')
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    # Sign out from Supabase
    supabase.auth.sign_out()
    
    # Clear session
    session.clear()
    
    flash('You have been logged out.', 'info')
    return redirect(url_for('landing'))

if __name__ == '__main__':
    app.run(debug=True)
