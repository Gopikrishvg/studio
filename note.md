google cloude ssh
    sudo ssh -i /Users/apple/Documents/googlecloud.pem  bitnami@104.196.26.239
change owner
    sudo chown -R bitnami:bitnami  .
    sudo chown -R www-data:www-data .

Apache Server reload
    sudo service apache2 reload

institute.Conf

listen 89
<VirtualHost *:89>
    # The ServerName directive sets the request scheme, hostname and port that
    # the server uses to identify itself. This is used when creating
    # redirection URLs. In the context of virtual hosts, the ServerName
    # specifies what hostname must appear in the request's Host: header to
    # match this virtual host. For the default virtual host (this file) this
    # value is not decisive as it is used as a last resort host regardless.
    # However, you must set it for any further virtual host explicitly.
    #ServerName www.example.com

    ServerAdmin gopikrishvg@gmail.com
    ServerName institute.com
    DocumentRoot /home/bitnami/pythonprojects/institute

    # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
    # error, crit, alert, emerg.
    # It is also possible to configure the loglevel for particular
    # modules, e.g.
    #LogLevel info ssl:warn

    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined

    # For most configuration files from conf-available/, which are
    # enabled or disabled at a global level, it is possible to
    # include a line for only one particular virtual host. For example the
    # following line enables the CGI configuration for this host only
    # after it has been globally disabled with "a2disconf".
    #Include conf-available/serve-cgi-bin.conf
    Alias /static /home/bitnami/pythonprojects/institute/static

    <Directory /home/bitnami/pythonprojects/institute/static>
            Require all granted
    </Directory>

    <Directory /home/bitnami/pythonprojects/institute/institute>
            <Files wsgi.py>
                    Require all granted
            </Files>
    </Directory>

    WSGIScriptAlias / /home/bitnami/pythonprojects/institute/institute/wsgi.py
    WSGIDaemonProcess institute python-path=/home/bitnami/pythonprojects/institute python-home=/home/bitnami/pythonprojects/institute/venv
    WSGIProcessGroup institute
    WSGIPassAuthorization on

</VirtualHost>

Settings.py

pip install django-cors-headers

INSTALLED_APPS = (

    ...
    'corsheaders',
    ...
)

MIDDLEWARE = [

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    ...
]

sudo a2ensite studio
