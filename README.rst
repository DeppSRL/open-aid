OpenAID
=======

Vedi la cartella `project/` per il codice sorgente.

Vedi la cartella `docs/` per la documentazione completa del progetto.


Configuration
-------------

`OPENAID_CRS_DONOR`: definisce il codice del donor del sito. (6 italy)
`OPENAID_DSD_FILE`: file sdmx contenete la struttura delle codelist. (resources/crs/dsd.xml)


Development
-----------

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
Basta copiarli nella directory ``resources/data``, poi lanciare::

    $ python project/manage.py crs resources/data/italy.2004-2012.csv

Si può importare un subset dei dati (ultime 1380 linee) con::

    $ python project/manage.py crs resources/data/italy.subset.csv


Occorre importare i dati di contesto (iso codes, popolazione e pil), con ::

    $ python project/manage.py import_context_data resources/territori.json -v2


A questo punto è possibile lanciare il runserver, per vedere l'applicazione::

    $ python project/manage.py runserver



Testing
-------

To start all Django TestCase modules:

::

    $ python project/manage.py test

To start functional test with selenium:

::

    $ python project/manage.py test tests.functional_tests

License
-------

Vedi il file LICENSE.txt
Vedi gli autori di questo progetto nel file CONTRIBUTORS.txt


-----

Generated with `cookiecutter`_ and `openpolis`_ /`django16-template`_ 0.1


.. _cookiecutter: https://github.com/audreyr/cookiecutter
.. _openpolis: https://github.com/openpolis
.. _django16-template: https://github.com/openpolis/django16-template