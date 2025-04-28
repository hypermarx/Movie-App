from flask import Flask, render_template, request, redirect, url_for, flash, session

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
        
        # Here you would typically validate the user credentials
        # For now, we'll just redirect back to the landing page
        # In a real app, you would add authentication logic
        
        return redirect(url_for('landing'))
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        verify_password = request.form.get('verify-password')
        
        # Here you would typically validate the form data and create a new user
        # For now, we'll just redirect back to the landing page
        # In a real app, you would add user creation logic
        
        return redirect(url_for('landing'))
    
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
