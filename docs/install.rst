Installazione
=============

Questi i passi per installare il sistema sul proprio box di sviluppo.

Setup
-----

Clona questo repository, entra nella cartella creata poi esegui:

::

    $ mkvirtualenv open-aid
    $ git clone git@github.com:DeppSRL/open-aid.git
    $ cd open-aid/
    $ git checkout -b develop
    $ git pull origin develop
    $ pip install -r requirements/development.txt

Copia il file ``config/samples/.env`` in ``config/.env`` e scommenta e modifica la URL di connessione al DB e SOLR::

    # openaid environment variables
    PROJECT_TITLE=OpenAID Website
    SECRET_KEY=xg_%ur#cc@b%w%13z8q+z+wg0wq6+h+)!*0x&eu96y0(4@&39*
    DEBUG=on
    DATABASE_URL=pgsql://user:password@host:5432/dbname

    # one index for each languages in settings.LANGUAGES ('en', 'it')
    SOLR_BASE_URL=http://127.0.0.1:8080/solr/open-aid-{lang}

Database
~~~~~~~~

E' necessario usare postgres, perché su sqlite c'è una select distinct che non è supportata.

Effettuare il ``syncdb``::

    $ python project/manage.py crs syncdb --migrate

Al primo lancio, occorre importare i dati dei progetti (si trovano sul NAS, sotto ``DEPP/Progetti/Open AID/Dati``).
Basta copiarli nella directory ``resources/fixtures``, poi lanciare::

    $ python project/manage.py loaddata resources/fixtures/codelists.fixtures.json
    $ python project/manage.py loaddata resources/fixtures/projects.fixtures.json


Occorre importare i dati di contesto (iso codes, popolazione e pil), con ::

    $ python project/manage.py import_context_data resources/territori.json -v2

[NOTA: non ha senso importare separatamente i dati di contesto, dovremo metterli dentro resources/codelists/recipient.csv]

Search index
~~~~~~~~~~~~

Aggiungere un core per ogni codice  in settings.LANGUAGES sul servizio solr con la configurazione presente ``config/solr/schema.xml``. ::

    http://127.0.0.1:8080/solr/open-aid-en
    http://127.0.0.1:8080/solr/open-aid-it

Nel file ``config/.env`` viene impostata solo la base dell'url.
Una volta riavviato tomcat6/7 sarà possibile indicizzare i contenuti ::

    $ python project/manage.py rebuild_index -k2
        -k : processi paralleli

Traduzioni testi statici
~~~~~~~~~~~~~~~~~~~~~~~~
::
    cd project/openaid
    django-admin.py compilemessages

Runserver
---------

A questo punto è possibile lanciare il runserver, per vedere l'applicazione::

    $ python project/manage.py runserver

Testing
-------

Per far partire i test::

    $ python project/manage.py test

Per far partire i test funzionali, con Selenium::

    $ python project/manage.py test tests.functional_tests

