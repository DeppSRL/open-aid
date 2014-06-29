Installazione
=============

Questi i passi per installare il sistema sul proprio box di sviluppo.


Configurazione
--------------

`OPENAID_CRS_DONOR`: definisce il codice del donor del sito. (6 italy)
`OPENAID_DSD_FILE`: file sdmx contenete la struttura delle codelist. (resources/crs/dsd.xml)


Setup
-----

Clona questo repository, entra nella cartella creata poi esegui:

::
    $ git checkout -b develop
    $ git pull origin develop
    $ pip install -r requirements/development.txt

Copia il file ``config/samples/.env`` in ``config/env`` e scommenta e modifica la URL di connessione al DB::

    # openaid environment variables
    PROJECT_TITLE=OpenAID Website
    SECRET_KEY=xg_%ur#cc@b%w%13z8q+z+wg0wq6+h+)!*0x&eu96y0(4@&39*
    DATABASE_URL=pgsql://user:passwd@localhost/openaid

E' necessario usare postgres, perché su sqlite c'è una select distinct che non è supportata.

Effettuare il ``syncdb``::

    $ python project/manage.py crs syncdb --migrate

Al primo lancio, occorre importare i dati dei progetti (si trovano sul NAS, sotto ``DEPP/Progetti/Open AID/Dati``).
Basta copiarli nella directory ``resources/fixtures``, poi lanciare::

    $ python project/manage.py loaddata resources/fixtures/codelists.fixtures.json
    $ python project/manage.py loaddata resources/fixtures/projects.fixtures.json


Occorre importare i dati di contesto (iso codes, popolazione e pil), con ::

    $ python project/manage.py import_context_data resources/territori.json -v2


A questo punto è possibile lanciare il runserver, per vedere l'applicazione::

    $ python project/manage.py runserver



Testing
-------

Per far partire i test::

    $ python project/manage.py test

Per far partire i test funzionali, con Selenium::

    $ python project/manage.py test tests.functional_tests
