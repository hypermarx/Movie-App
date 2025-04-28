from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from supabase import create_client, Client

# Direct Supabase credentials
supabase_url = "https://gpfljnclvvwogzvmrtku.supabase.co"
supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdwZmxqbmNsdnZ3b2d6dm1ydGt1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDU4Nzg5MTQsImV4cCI6MjA2MTQ1NDkxNH0.9_2vn4JmwC54IkwItneVIhHZqaWuti3BC9hZSRshwC8"

# Initialize Supabase client
supabase: Client = create_client(supabase_url, supabase_key)

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure random key in production

@app.route('/')
def landing():
    return render_template('landing.html')

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
