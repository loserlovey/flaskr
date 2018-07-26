# flaskr

## setup enviroment
1. create folder like:

├── config.py
├── db
│   └── flaskr.db
├── deployment
│   ├── flaskr
│   └── flaskr.conf
├── flaskrapp
│   ├── __init__.py
│   ├── static
│   │   └── style.css
│   ├── templates
│   │   ├── layout.html
│   │   ├── login.html
│   │   └── show_entries.html
│   └── views.py
├── README.md
├── requirements.txt
├── run.py
└── schema.sql


2. sudo apt install supervisor

3. sudo cp deployment/flaskr /etc/nginx/site-available/
   sudo ln -s ../sites-available/flaskr
   sudo cp deployment/flaskr.conf /etc/supervisor/conf.d/
   sudo service nginx reload
   sudo service nginx restart
   sudo service supervisor reload
   sudo service supervisor restart

   

