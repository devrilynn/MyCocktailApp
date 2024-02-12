# app.py
from flask import Flask, render_template, request, url_for, redirect, session

app = Flask(__name__)

USER_DATA_FILE = "user_data.txt"

users = []

def write_user_data():
    with open(USER_DATA_FILE, 'a') as f:
        for user in users:
            f.write(f"{user['first-name']}, {user['last-name']}, {user['email']}, {user['password']}\n")
    
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match', 
                                   first_name=first_name, last_name=last_name, 
                                   email=email, password=password, confirm_password=confirm_password)
        
        if email and password:
            users.append({'first-name': first_name, 'last-name': last_name, 'email': email, 'password': password})
            
            # Write user data to file after each registration
            write_user_data()
            
            return redirect(url_for('confirm_registration'))
    
    return render_template('register.html')

@app.route('/confirm_registration', methods=['GET'])
def confirm_registration():
    return render_template('confirm_registration.html')

if __name__ == '__main__':
    app.run(debug=True)
