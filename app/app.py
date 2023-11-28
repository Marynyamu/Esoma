from flask import Flask, render_template, request
import os
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__,
            template_folder=os.path.abspath(os.path.join(os.getcwd(), '..', 'templates')),
            static_folder=os.path.abspath(os.path.join(os.getcwd(), '..', 'static'))
           )

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/db_name'  # Replace with your database connection details
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Import the User model
from models.user import User

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/join')
def join():
    return render_template('join.html')

@app.route('/register', methods=['GET','POST'])
def register():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    phoneNumber = request.form['phoneNumber']

     # Implement password hashing for security
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Check if the user already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return "Username already exists. Please choose a different one."

    # Create a new user object
    new_user = User(username=username, email=email, password=password, phone_number=phone_number)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # Basic validation checks (you can add more complex validation logic)
    if not username.isalpha():
        return "Invalid username. It should only contain letters."

    # Check if the email is valid (basic check for example)
    if "@" not in email or "." not in email:
        return "Invalid email address."

    # Password strength check (example: at least 6 characters)
    if len(password) < 6:
        return "Password should be at least 6 characters long."

    # If all checks pass, you might save the user data or perform other actions
    # For now, let's just acknowledge successful registration
    return f"Registration successful for {username} with email {email}."



if __name__ == '__main__':
    app.run(debug=True)

