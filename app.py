from flask import Flask, render_template, request
from forms import RegistrationForm
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

'''
# To generate a secret key, run the following code once in a Python shell:
import secrets 
print(secrets.token_hex(16))
'''
app = Flask(__name__)

# ✅ Add a secret key (required for CSRF)
app.config['SECRET_KEY'] = '6d3552184a04f416e7c240dc7f0fe13a'  # use a random value in real apps

# ✅ Enable CSRF protection
csrf = CSRFProtect(app)

# ✅ Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///whollyroasters.db'
db = SQLAlchemy(app)
with app.app_context():
    # ✅ Define the User model
    class User(db.Model):
        # Custom name for the table
        #__tablename__ = 'Users'
        
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(50), index=True, unique=True)
        password = db.Column(db.String(128))

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"
    
    # ✅ Define the ShippingInfo model
    class ShippingInfo(db.Model):
        ship_id = db.Column(db.Integer, primary_key=True)
        full_name = db.Column(db.String(50))
        address = db.Column(db.String(50))
        user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f"<{self.full_name}'s address is {self.address}.>"
    
    db.create_all()
    
    User.query.delete()
    user1 = User(username = "coffeeaddict", password = "1234")
    db.session.add(user1)
    db.session.commit()    
    
    ShippingInfo.query.delete()
    ship1 = ShippingInfo(full_name="Claudia Reyes", address="Amsterdam 210, CDMX, Mexico", user_id=2)
    ship2 = ShippingInfo(full_name="Roy Latte", address="Beau St, Bath BA1 1QY, UK", user_id=1)
    db.session.add(ship1)
    db.session.add(ship2)
    db.session.commit()
    
# end db app context

@app.route("/", methods=["GET"])
def welcome():
    #return "Welcome to Wholly Roasters!"
    return render_template("home.html", name = "Parker")

@app.route("/about", methods=["GET"])
def about():
    #return "This is the 'About Us' page."
    return render_template("about.html")

@app.route("/inventory", methods=["GET"])
def inventory():
    return render_template("inventory.html", 
                           count = 5,
                           beans = ["Arabica", 
                                    "Robusta", 
                                    "Liberica", 
                                    "Excelsa", 
                                    "Maragogype", 
                                    "Typica", 
                                    "Bourbon", 
                                    "Caturra", 
                                    "Gesha", 
                                    "Pacamara", 
                                    "SL28", 
                                    "SL34"])

@app.route("/shop", methods=["GET"])
def shop():
    return render_template("shop.html", 
                           cart = ["12oz Medium Roast", 
                                   "24oz French Roast", 
                                   "96oz Whole Beans"])

'''
@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    errors = []   
    if request.method == "POST":
        username = request.form["uname"]
        password = request.form["pword"]
        confirm = request.form["confirm"]
        # Here you would typically save the user info to a database
        message = f"Successfully registered user: {username}!"
        
        if not username:
            errors.append("Username can't be blank!")
        
        if not password:
            errors.append("Password can't be blank!")
            
        if not confirm:
            errors.append("Password can't cannot be blank!")
            
        if len(username) < 3:
            errors.append("Username must be greater than 3 characters!")
            
        if password != confirm:
            errors.append("Passwords don't match!")
        
        if errors:
            message = "Registration failed! See errors below:"
        else:
            message = f"Successfully registered {username}."
    
    return render_template("register.html",
                           message=message,
                           errors=errors)
'''
@app.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    form = RegistrationForm()

    if request.method == "POST":
        if form.validate_on_submit():
            user_match = User.query.filter_by(username=form.data['uname']).first()
            if user_match:
                message = "User already exists!"
                return render_template("register.html",
                                       message=message,
                                       form=form)
                        
            '''
            username = form.data["uname"]
            password = form.data["pword"]            
            '''
            confirm = form.data["confirm"]
            
            username=form.uname.data
            newUser = User(
                username=username, 
                password=form.pword.data)
            db.session.add(newUser)
            db.session.commit()
            message = f"Successfully registered {username}!"
        else:
            message = "Registration failed."

    return render_template("register.html",
                           message=message,
                           form=form)
    
@app.route("/admin", methods=["GET"])
def admin():
    users = User.query.all()
    shippers = ShippingInfo.query.all()
    return render_template("admin.html", users=users, shippers=shippers)

if __name__ == "__main__":
    app.run(debug=True)