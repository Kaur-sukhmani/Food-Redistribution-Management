import hashlib
import datetime
from flask import *
from session3 import MongoDBHelper
from bson.objectid import ObjectId

web_app = Flask("PlateSaver System")


@web_app.route("/")
def index():
    return render_template('index.html')


@web_app.route("/index1", methods=['GET', 'POST'])
def index1():
    print("index1")
    return render_template('index1.html')


@web_app.route("/index2", methods=['GET', 'POST'])
def index2():
    print("index2")
    return render_template('index2.html')


@web_app.route("/home")
def home():
    return render_template('home.html', name=session['contributor_name'])

@web_app.route("/home2")
def home2():
    return render_template('home2.html', name=session['philanthropists_name'])

@web_app.route("/register1")
def register1():
    return render_template('register1.html')

@web_app.route("/register2")
def register2():
    return render_template('register2.html')

@web_app.route("/register-contributor", methods=['POST'])
def register_contributor():
    register_data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'password': hashlib.sha256(request.form['pswd'].encode('utf-8')).hexdigest(),
        'createdOn': datetime.datetime.today()
    }
    print(register_data)
    db = MongoDBHelper(collection='Contributor')
    db.insert(register_data)

    return redirect('/index1')
    # return render_template("home.html")

@web_app.route("/register-philanthropists", methods=['POST'])
def register_philanthropists():
    register_data2={
        'name': request.form['name'],
        'email': request.form['email'],
        'password': hashlib.sha256(request.form['pwd'].encode('utf-8')).hexdigest(),
        'createdOn': datetime.datetime.today()
    }
    print(register_data2)
    db =MongoDBHelper(collection='charity')
    db.insert(register_data2)

    return redirect('/index2')

@web_app.route("/login-contributor", methods=['POST'])
def login_contributor():
    contributor_data = {
        'email': request.form['email'],
        'password': hashlib.sha256(request.form['pswd'].encode('utf-8')).hexdigest()
    }

    db = MongoDBHelper(collection='Contributor')
    cursor = db.fetch(contributor_data)
    documents = list(cursor)  # Convert cursor to a list of documents

    if len(documents) == 1:
        session['contributor_id'] = str(documents[0]['_id'])
        session['contributor_email'] = documents[0]['email']
        session['contributor_name'] = documents[0]['name']
        return render_template('home.html', name=session['contributor_name'])
    else:
        # Handle the case where no matching documents were found
        return render_template('error.html', message="Invalid credentials", name=session['contributor_name'])

@web_app.route("/login-philanthropists", methods=['POST'])
def login_philanthropists():
    philanthropists_data= {
        'email': request.form['email'],
        'password': hashlib.sha256(request.form['pwd'].encode('utf-8')).hexdigest()
    }
    db = MongoDBHelper(collection='charity')
    cursor=db.fetch(philanthropists_data)
    documents = list(cursor)
    if len(documents) == 1:
        session['philanthropists_id'] = str(documents[0]['_id'])
        session['philanthropists_email'] = documents[0]['email']
        session['philanthropists_name'] = documents[0]['name']
        return render_template('home2.html', name=session['philanthropists_name'])
    else:
        # Handle the case where no matching documents were found
        return render_template('error2.html', message="Invalid credentials", name=session['philanthropists_name'])


# NourishDonor
@web_app.route("/add-contributor", methods=['POST', 'GET'])
def add_contributor():
    donor_data = {
        'name': request.form['name'],
        'phone': request.form['phone'],
        'email': request.form['email'],
        'address': request.form['address'],
        'type': request.form['type'],
        'contributor_id': session['contributor_id'],
        'contributor_email': session['contributor_email'],
        'createdOn': datetime.datetime.today()
    }
    if len(donor_data['name']) == 0 or len(donor_data['phone']) == 0 or len(donor_data['email']) == 0:
        return render_template('error.html', message="Name, Phone, Email cannot be empty")

    print(donor_data)
    db = MongoDBHelper(collection='NourishContributors')
    db.insert(donor_data)

    return render_template('success.html', message="{} added successfully".format(donor_data['name']),
                           name=session['contributor_name'])


@web_app.route("/add-list/<id>")
def add_list(id):
    db = MongoDBHelper(collection='NourishContributors')
    query = {'_id': ObjectId(id)}
    nourish_contributor = db.fetch(query)[0]
    return render_template('add-list.html',
                           NourishContributor=nourish_contributor,
                           contributor_id=session['contributor_id'],  # Corrected field name
                           contributor_email=session['contributor_email'], name=session['contributor_name']
                           # Corrected field name
                           )


@web_app.route("/add-list-db", methods=['POST'])
def add_list_db():
    add_list = {
        'name': request.form['name'],
        'dom': request.form['dateOfManufacture'],
        'expiry_date': request.form['expiryDate'],
        'quantity': int(request.form['quantity']),
        'type': request.form['type'],
        'NourishContributor_name': session['contributor_name'],
        'NourishContributor_id': ObjectId(request.form['id']),  # Corrected field name
        'NourishContributor_email': session['contributor_email'],  # Corrected field name
        # 'NourishContributor_name': request.form['NourishContributor_name'],
        # 'NourishContributor_id': request.form['NourishContributor_id'],  # Corrected field name
        # 'NourishContributor_email': request.form['NourishContributor_email'],  # Corrected field name
        'createdOn': datetime.datetime.today()
    }
    if len(add_list['name']) == 0 or len(str(add_list['quantity'])) == 0 or len(add_list['expiry_date']) == 0:
        return render_template('error.html', message="name, expiry date adn quantity cannot be empty",
                               name=session['contributor_name'])

    print(add_list)
    db = MongoDBHelper(collection='list')
    db.insert(add_list)

    return render_template('success.html',
                           message="In {} \n {} added to the list ".format(add_list['NourishContributor_email'],
                                                                           add_list['name']),
                           name=session['contributor_name'])

@web_app.route('/add-philanthropists', methods=['POST', 'GET'])
def add_philanthropists():
    philanthropists_data = {
        'type': request.form['type'],
        'name': request.form['name'],
        'phone': request.form['phone'],
        'email': request.form['email'],
        'address': request.form['address'],
        'philanthropists_id': session['philanthropists_id'],
        'philanthropists_name': session['philanthropists_name'],
        'philanthropists_email': session['philanthropists_email'],
        'createdOn': datetime.datetime.today()
    }
    print(philanthropists_data)
    if len(philanthropists_data['name']) == 0 or len(philanthropists_data['address']) == 0:
        return render_template('error2.html', message="name, address cannot be empty",
                               name=session['philanthropists_name'],
                               email=session['philanthropists_email'])

    db = MongoDBHelper(collection='Philanthropists')
    db.insert(philanthropists_data)
    return render_template('success2.html', message="{} added successfully".format(philanthropists_data['name']))




@web_app.route('/fetch-contributor', methods=['GET'])
def fetch_contributor():
    db = MongoDBHelper(collection='NourishContributors')
    query = {}
    documents = db.fetch(query)

    print(documents, type(documents))

    return render_template('all-contributors.html', documents=documents, name=session['contributor_name'])


@web_app.route("/fetch-list/<id>")
def fetch_list(id):
    db = MongoDBHelper(collection="NourishContributors")
    query = {'_id': ObjectId(id)}
    NourishContributor = db.fetch(query)[0]  # Fetch the first document in the list

    db = MongoDBHelper(collection="list")
    query = {'NourishContributor_id': id}
    documents = db.fetch(query)

    print(documents, type(documents))
    return render_template('list.html',
                           documents=documents,
                           name=session['contributor_name'],
                           NourishContributor=NourishContributor)

@web_app.route('/fetch-philanthropists', methods=['GET'])
def fetch_philanthropists():
    db = MongoDBHelper(collection='Philanthropists')
    query = {}  # You can add filter conditions here if needed
    documents = db.fetch(query)
    return render_template('all-philanthropists.html', documents=documents, name=session['philanthropists_name'])

@web_app.route('/delete-contributor/<id>')
def delete_contributor(id):
    db = MongoDBHelper(collection='NourishContributors')
    query = {'_id': ObjectId(id)}
    contributor = db.fetch(query)[0]
    db.delete(query)
    return render_template('success.html', message="Constributor- {} deleted ".format(contributor['name']))

@web_app.route('/delete-philanthropists/<id>')
def delete_philanthropists(id):
    db = MongoDBHelper(collection='Philanthropists')
    query = {'_id': ObjectId(id)}
    Philanthropists = db.fetch(query)[0]
    db.delete(query)
    return render_template('success.html', message="{} deleted successfully".format(Philanthropists['name']))



@web_app.route('/update-contributor/<id>')
def update_contributor(id):
    db = MongoDBHelper(collection='NourishContributors')
    query = {'_id': ObjectId(id)}
    NourishContributor = db.fetch(query)[0]
    return render_template('update-contributor.html', NourishContributors=NourishContributor,
                           name=session['contributor_name'])


@web_app.route('/update-contributor-db', methods=['POST'])
def update_contributor_db():
    update_data = {
        'name': request.form['name'],
        'phone': request.form['phone'],
        'email': request.form['email'],
        'address': request.form['address'],
        'type': request.form['type']
    }
    if len(update_data['name']) == 0 or len(update_data['phone']) == 0 or len(update_data['email']) == 0:
        return render_template('error.html', message="Name, Phone and Email cannot be Empty")

    print(update_data)
    db = MongoDBHelper(collection='NourishContributors')
    query = {'_id': ObjectId(request.form['cont_id'])}
    db.update(update_data, query)

    return render_template('success.html', message="{} updated successfully".format(update_data['name']))

@web_app.route('/update-philanthropists/<id>', methods=['POST', 'GET'])
def update_philanthropists(id):
    db = MongoDBHelper(collection='Philanthropists')
    query = {'_id': ObjectId(id)}
    print("hello")
    Philanthropists = db.fetch(query)[0]
    return render_template('update-philanthropists.html', Philanthropists=Philanthropists, name=session['philanthropists_name'])

@web_app.route('/update-philanthropists-db', methods=['POST'])
def update_philanthropists_db():
    update2_data={
        'type': request.form['type'],
        'name': request.form['name'],
        'phone': request.form['phone'],
        'email': request.form['email'],
        'address': request.form['address'],
    }
    print(update2_data)
    if len(update2_data['name'])==0 or len(str(update2_data['type']))==0:
        return render_template('error.html', message="{name, type cannot be empty")

    print(update2_data)
    db = MongoDBHelper('Philanthropists')
    query = {'_id': ObjectId(request.form['philanthropists_id'])}
    db.update(update2_data, query)
    return render_template('success.html', message="{} updated successfully".format(update2_data['name']))

@web_app.route("/delete-listItem/<id>")
def delete_listItem(id):
    db = MongoDBHelper(collection='list')
    query = {'_id': ObjectId(id)}
    item = db.fetch(query)[0]
    db.delete(item)
    return render_template("success.html", message="{} deleted successfully".format(item['name']))


@web_app.route("/update-listItem/<id>")
def update_listItem(id):
    db = MongoDBHelper(collection='list')
    query = {'_id': ObjectId(id)}
    item = db.fetch(query)[0]
    print(item)
    return render_template('update-listItem.html', item=item, name=session['contributor_name'])


@web_app.route("/update-listItem-db", methods=["POST"])
def update_listItem_db():
    print("in update_listItem_db")
    update_list_data = {
        'name': request.form['name'],
        'dom': request.form['dateOfManufacture'],
        'expiry_date': request.form['expiryDate'],
        'quantity': request.form['quantity'],
        'type': request.form['type']
    }

    if len(update_list_data['name']) == 0:
        return render_template('error.html', message="name cannot be empty")

    print(update_list_data)
    db = MongoDBHelper(collection='list')
    query = {'name': request.form['name']}
    db.update(update_list_data, query)

    return render_template('success.html', message="{} updated successfully".format(update_list_data['name']))


@web_app.route("/search")
def search():
    return render_template('search.html', name=session['contributor_name'], email=session['contributor_email'])


@web_app.route("/search-contributor", methods=['POST'])
def search_contributor():
    db = MongoDBHelper(collection='NourishContributors')
    query = {'email': request.form['email'], 'contributor_id': session['contributor_id']}
    NourishContributors = db.fetch(query)
    NourishContributors = list(NourishContributors)
    if len(NourishContributors) == 1:
        NourishContributor = NourishContributors[0]
        return render_template('contributor-profile.html', NourishContributor=NourishContributor,
                               name=session['contributor_name'], email=session['contributor_email'])
    else:
        return render_template("error.html", message="Contributor not found")

@web_app.route("/manage-list")
def manage_list():
    db = MongoDBHelper(collection='list')
    query = {}
    list = db.fetch(query)
    print("inside manage list")
    return render_template('manage-list.html', list=list, name=session['contributor_name'], email=session['contributor_email'] )

@web_app.route("/manage-list2")
def manage_list2():
    db = MongoDBHelper(collection='list')
    query = {}
    list = db.fetch(query)
    print("inside manage list")
    return render_template('manage-list2.html', list=list,  name=session['philanthropists_name'], email=session['philanthropists_email'])


@web_app.route("/yes-order/<id>")
def yes_order(id):
    db = MongoDBHelper(collection='list')
    query = {'_id': ObjectId(id)}  # Construct a query dictionary using the provided ID
    doc = db.fetch(query)  # Fetch the document using the query

    return render_template('yes-order.html', doc=doc, name=session['philanthropists_name'],
                           email=session['philanthropists_email'])

@web_app.route("/logout-contributor")
def logout_contributor():
    session.pop('contributor_id', None)
    session.pop('contributor_email', None)
    session.pop('contributor_name', None)
    return redirect('/index1')

@web_app.route("/logout-philanthropists")
def logout_philanthropists():
    session.pop('philanthropists_id', None)
    session.pop('philanthropists_email', None)
    session.pop('philanthropists_name', None)
    return redirect('/index2')



def main():
    web_app.secret_key = 'PlateSaverSystem-key-1'
    web_app.run(port=5001, debug=True)


if __name__ == "__main__":
    main()
