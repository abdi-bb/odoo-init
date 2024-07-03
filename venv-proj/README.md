<!-- Minimal Odoo Development Guide -->

# PHASE 1

## PROJECT SETUP

### 1. Install and Set Up PostgreSQL

#### Install PostgreSQL System-wide

```sh
sudo apt update
sudo apt install postgresql # Installs PostgreSQL
```

#### Create Database and Dedicated Database User

1. **Ensure your PostgreSQL server is running**:

    ```sh
    sudo service postgresql start
    ```

2. **Create a PostgreSQL User for the Current System User**:

    ```sh
    sudo su -c "createuser -s $USER" postgres # Creates db superuser
    ```

    It's good idea to create our dedicated db user as a super user to be able to create and drop databases that are used by Odoo
instances

   ```sh
    sudo su -c "createuser -s library_db_usr" postgres # Create db superuser using your targeted db user
   ```

   Set a password for this db user to match with the password from the config file

    Using postgres system user
   
   ```sh
  sudo -u postgres psql -c "ALTER USER library_db_usr WITH PASSWORD 'library_db_pwd'"
   ```

   or alternatively using current system user

   ```sh
  sudo -u $USER psql -c "ALTER USER library_db_usr WITH PASSWORD 'library_db_pwd'" -d postgres
   ```


---

### 2. Install Odoo

#### 1. Install the Odoo System Dependencies

```sh
sudo apt update
sudo apt upgrade
sudo apt install git # Install Git
sudo apt install python3-dev python3-pip python3-wheel python3-venv # Python 3 for dev
sudo apt install build-essential libpq-dev libxslt-dev libzip-dev libldap2-dev libsasl2-dev libssl-dev
```

#### 2. Create the Project Directory

```sh
mkdir ~/work15 # Create a directory to work in
cd ~/work15 # Go into our work directory
```

#### 3. Create and Activate a Virtual Environment

```sh
python3 -m venv ~/work15/env15
source ~/work15/env15/bin/activate
```

#### 4. Install Odoo

**Clone Odoo from GitHub (for development)**

```sh
git clone https://github.com/odoo/odoo.git -b 15.0 \
--depth=1 # Get Odoo sources Or Download the zipped file and extract
```

**Install Required Python Packages and Odoo Itself**

```sh
pip install -U pip
pip install -r ~/work15/odoo/requirements.txt
pip install -e ~/work15/odoo
```

---

# PHASE 2

## Build Your Apps/Modules

#### Copy and Edit the Config File(Follow this for simplicity)

```sh
cp odoo/debian/odoo.conf ~/work15/library.conf
nano ~/work15/library.conf
```

Edit the config file to look like this:

```ini
[options]
; This is the password that allows database operations:
; admin_passwd = admin
admin_passwd = master
db_host = localhost
db_name = library
db_port = 5432
db_user = library_db_usr
db_password = library_db_pwd
http_port = 8069
;addons_path = /usr/lib/python3/dist-packages/odoo/addons
```

OR

#### Create a full Config File (Skip this one if you follow the above)

```sh
odoo --save --stop-after-init # Creates ~/.odoorc config file
odoo -c ~/work15/library.conf --save --stop #To create our own full custom config
```

```sh
odoo -c ~/work15/library.conf -i base # To run the odoo server using our custom config and to
```


To save the log output to a file:

```sh
odoo --logfile=~/work15/odoo.log
```

### 1. Create a New Custom Addons Directory

```sh
mkdir ~/work15/library
```

### 2. Create Your New App/Module

Use Scaffold to Create a Skeleton for the Module:

```sh
odoo scaffold library_app ~/work15/library
```

Add your custom addons and Odoo's addons to the config file:

edit the `library.conf` to include this line at the end

```ini
[options]
; This is the password that allows database operations:
; admin_passwd = admin
admin_passwd = master
db_host = localhost
db_name = library
db_port = 5432
db_user = library_db_usr
db_password = library_db_pwd
http_port = 8069
;addons_path = /usr/lib/python3/dist-packages/odoo/addons
addons_path = /home/abdi/work15/library,/home/abdi/work15/odoo/addons,/home/abdi/work15/odoo/odoo/addons
```

Or use the folllowing command(Note this will add the full config params to the file)

```sh
odoo -c library.conf --addons-path="./library,./odoo/addons,./odoo/odoo/addons" --save --stop
```

Edit the `__manifest__.py` file with your own information: Like this eg.

```sh
{
    "name": "Library Management",
    "summary": "Manage library catalog and book lending.",
    "author": "Daniel Reis",
    "license": "AGPL-3",
    "website": "https://github.com/PacktPublishing/Odoo-15-Development-Essentials",
    "version": "15.0.1.0.0",
    "category": "Services/Library",
    "depends": ["base"],
    "application": True,
}
```

#### Install Your App

Although you haven't completed your app, you can install it to see it listed correctly:

Before installing, it's convenient to add your app icon

```sh
mkdir -p ~/work15/library/library_app/static/description
cp ~/work15/odoo/addons/note/static/description/icon.png ~/work15/library/library_app/static/description/
```

```sh
odoo -c ~/work15/library.conf -d library -i library_app
```

#### Upgrade Your App

Whenever you make changes to the XML file, upgrade your app. If you change Python code, restart the server:

```sh
odoo -c ~/work15/library.conf -u library_app
```

Or after installing watchdog, use the `--dev=all` option to auto-reload during development:

```sh
odoo -c ~/work15/library.conf -u library_app --dev=all
```

### 3. Adding Automated Tests (To Follow TDD)

Once you write tests, you can run them using:

```sh
odoo -c ~/work15/library.conf -u library_app --test-enable
```

### 4. Implement the Model Layer

Create the model file `~/work15/library/library_app/models/library_book.py`

```sh
from odoo import fields, models

class Book(models.Model):
    _name = "library.book"
    _description = "Book"

    name = fields.Char("Title", required=True)
    isbn = fields.Char("ISBN")
    active = fields.Boolean("Active?", default=True)
    date_published = fields.Date()
    image = fields.Binary("Cover")
    publisher_id = fields.Many2one("res.partner", string="Publisher")
    author_ids = fields.Many2many("res.partner", string="Authors")
```

### 5. Set Up Security Groups and Access Controls

#### Create Security Groups and Rules

Create `~/work15/library/library_app/security/library_security.xml`:

```xml
<odoo>
    <data>
        <!-- Library User Group -->
        <record id="library_group_user" model="res.groups">
            <field name="name">User</field>
            <field name="category_id" ref="base.module_category_services_library"/>
            <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
        </record>
        <!-- Library Manager Group -->
        <record id="library_group_manager" model="res.groups">
            <field name="name">Manager</field>
            <field name="category_id" ref="base.module_category_services_library"/>
            <field name="implied_ids" eval="[(4, ref('library_group_user'))]"/>
            <field name="users" eval="[(4, ref('base.user_root')), (4, ref('base.user_admin'))]"/>
        </record>
        <!-- Row-level access rule /record rule -->
        <record id="book_user_rule" model="ir.rule">
            <field name="name">Library Book User Access</field>
            <field name="model_id" ref="model_library_book"/>
            <field name="domain_force">[('active', '=', True)]</field>
            <field name="groups" eval="[(4, ref('library_group_user'))]"/>
        </record>
    </data>
</odoo>
```

#### Create Access Controls For the security groups inside `ir.model.access.csv`

Create `~/work15/library/library_app/security/ir.model.access.csv`:

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_book_user,BookUser,model_library_book,library_group_user,1,1,1,0
access_book_manager,BookManager,model_library_book,library_group_manager,1,1,1,1
```

#### Assign Users to Security Groups

...


### 6. Implement the View Layer

Create menu items and views:

#### Menu Items

Create `~/work15/library/library_app/views/library_menu.xml`:

```xml
<odoo>
    <!-- Library App Menu -->
    <menuitem id="menu_library" name="Library"/>
    <!-- Action to open the Book list -->
    <record id="action_library_book" model="ir.actions.act_window">
        <field name="name">Library Books</field>
        <field name="res_model">library.book</field>
        <field name="view_mode">tree,form</field>
    </record>
    <!-- Menu item to open the Book list -->
    <menuitem id="menu_library_book" name="Books" parent="menu_library" action="action_library_book"/>
</odoo>
```

#### Form, Tree and Search Views

Create `~/work15/library/library_app/views/book_view.xml`:

```xml
<odoo>
    <record id="view_form_book" model="ir.ui.view">
        <field name="name">Book Form</field>
        <field name="model">library.book</field>
        <field name="arch" type="xml">
            <form>
                <header>
                    <button name="button_check_isbn" type="object"
                        string="Check ISBN" />
                </header>
                <sheet>
                    <group name="group_top">
                        <group name="group_left">
                            <field name="name" />
                            <field name="author_ids" widget="many2many_tags" />
                            <field name="publisher_id" />
                            <field name="date_published" />
                        </group>
                        <group name="group_right">
                            <field name="isbn" />
                            <field name="active" />
                            <field name="image" widget="image" />
                        </group>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_tree_book" model="ir.ui.view">
        <field name="name">Book List</field>
        <field name="model">library.book</field>
        <field name="arch" type="xml">
            <tree>
                <field name="name"/>
                <field name="author_ids" widget="many2many_tags" />
                <field name="publisher_id"/>
                <field name="date_published"/>
            </tree>
        </field>
    </record>

    <record id="view_search_book" model="ir.ui.view">
        <field name="name">Book Filters</field>
        <field name="model">library.book</field>
        <field name="arch" type="xml">
            <search>
                <field name="publisher_id"/>
                <filter name="filter_inactive"
                    string="Inactive"
                    domain="[('active','=',True)]"/>
                <filter name="filter_active"
                    string="Active"
                    domain="[('active','=',False)]"/>
            </search>
        </field>
    </record>
</odoo>
```

### 7. Implement the Business Logic Layer

Add Methods to the model:

Edit `~/work15/library/library_app/models/library_book.py`:

```python
from odoo import fields, models
from odoo.exceptions import ValidationError

class Book(models.Model):
    _name = "library.book"
    _description = "Book"

    name = fields.Char("Title", required=True)
    isbn = fields.Char("ISBN")
    active = fields.Boolean("Active?", default=True)
    date_published = fields.Date()
    image = fields.Binary("Cover")
    publisher_id = fields.Many2one("res.partner", string="Publisher")
    author_ids = fields.Many2many("res.partner", string="Authors")

    def _check_isbn(self):
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 13:
            ponderations = [1, 3] * 6
            terms = [a * b for a, b in zip(digits[:12],
                ponderations)]
            remain = sum(terms) % 10
            check = 10 - remain if remain != 0 else 0
            return digits[-1] == check

    def button_check_isbn(self):
        for book in self:
            if not book.isbn:
                raise ValidationError("Please provide an ISBN for %s" % book.name)
            if book.isbn and not book._check_isbn():
                raise ValidationError("%s ISBN is invalid" % book.isbn)
        return True
```

### 8. Implement the Website UI

#### Create Controllers and Templates

##### Create Controller for Routing

Create `~/work15/library/library_app/controllers/main.py`:

```python
from odoo import http

class Books(http.Controller):

    @http.route("/library/books")
    def list(self, **kwargs):
        Book = http.request.env["library.book"]
        books = Book.search([])

        return http.request.render(
            "library_app.book_list_template",
            {"books": books}
            )
```

##### Create Templates using QWeb

Create `~/work15/library/library_app/views/book_list_template.xml`:

```xml
<odoo>
<template id="book_list_template" name="Book List">
    <div id="wrap" class="container">
    <h1>Books</h1>
        <t t-foreach="books" t-as="book">
            <div class="row">
                <span t-field="book.name" />,
                <span t-field="book.date_published" />,
                <span t-field="book.publisher_id" />
            </div>
        </t>
    </div>
</template>
</odoo>
```

#### Don't forget updating the `__manifest__.py` file each time you add new xml/csv file

```sh
"data": [
    "security/library_security.xml",
    "security/ir.model.access.csv",
    "views/book_view.xml",
    "views/library_menu.xml",
    "views/book_list_template.xml",
],
```

### Final Steps: Running and Testing Your Odoo Instance

1. **Run Odoo**: Start the Odoo server with your custom configuration file.

    ```sh
    odoo -c ~/work15/library.conf -u library_app --dev=all
    ```

### Summary of Complete Setup

Here’s a complete set of commands for setting up and running the Odoo development environment for your Library Management System:

```sh
sudo apt update
sudo apt install postgresql
sudo service postgresql start
sudo -u postgres psql
CREATE USER library_db_usr WITH PASSWORD 'library_db_pwd';
CREATE DATABASE library OWNER library_db_usr;
GRANT ALL PRIVILEGES ON DATABASE library TO library_db_usr;
\q
sudo su -c "createuser -s $USER" postgres

sudo apt update
sudo apt upgrade
sudo apt install git python3-dev python3-pip python3-wheel python3-venv build-essential libpq-dev libxslt-dev libzip-dev libldap2-dev libsasl2-dev libssl-dev

mkdir ~/work15
cd ~/work15
git clone https://github.com/odoo/odoo.git -b 15.0 --depth=1

python3 -m venv ~/work15/env15
source ~/work15/env15/bin/activate

pip install -U pip
pip install -r ~/work15/odoo/requirements.txt
pip install -e ~/work15/odoo

odoo --save --stop-after-init
odoo -c ~/work15/library.conf --save --stop
odoo -c ~/work15/library.conf
odoo -d library --stop-after-init

mkdir ~/work15/library
odoo scaffold library_app ~/work15/library
odoo -c library.conf --addons-path="./library,./odoo/addons"
odoo --addons-path="~/work15/library,~/work15/odoo/addons" -d library -c ~/work15/library.conf --save --stop

cd ~/work15/library/library_app
mkdir -p ./static/description
cp ~/work15/odoo/addons/note/static/description/icon.png ./static/description/
odoo -c ~/work15/library.conf -d library -i library_app

nano ~/work15/library/library_app/__manifest__.py

odoo -c ~/work15/library.conf -d library -u library_app
odoo -c ~/work15/library.conf -d library -u library_app --dev=all

nano ~/work15/library/library_app/models/library_book.py

nano ~/work15/library/library_app/security/library_security.xml
nano ~/work15/library/library_app/security/ir.model.access.csv
nano ~/work15/library/library_app/views/library_menu.xml
nano ~/work15/library/library_app/views/book_views.xml

nano ~/work15/library/library_app/controllers/main.py
nano ~/work15/library/library_app/views/book_list_template.xml

nano ~/work15/library/library_app/__manifest__.py

odoo -c ~/work15/library.conf -d library -u library_app --dev=all
```
