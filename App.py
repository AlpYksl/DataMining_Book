from flask import *  

app = Flask(__name__)
  
# Pass the required route to the decorator.
@app.route("/")
def message():
    return render_template('login.html')  
    

if __name__ == '__main__':
   app.run()