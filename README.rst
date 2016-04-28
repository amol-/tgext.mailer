About tgext.mailer
-------------------------

.. image:: https://travis-ci.org/amol-/tgext.mailer.png
    :target: https://travis-ci.org/amol-/tgext.mailer

.. image:: https://coveralls.io/repos/amol-/tgext.mailer/badge.png
    :target: https://coveralls.io/r/amol-/tgext.mailer

.. image:: https://pypip.in/v/tgext.mailer/badge.png
   :target: https://pypi.python.org/pypi/tgext.mailer

.. image:: https://pypip.in/d/tgext.mailer/badge.png
   :target: https://pypi.python.org/pypi/tgext.mailer

tgext.mailer is a TurboGears2 extension for sending emails with transaction
manager integration. Whenever the transaction manager provided with TurboGears
commits the transaction all the emails are sent, when the transaction is
abort the mails are discarded.

While there are other extensions available for sending emails on TurboGears,
like TurboMail. Those are not bound to the transaction manager, have a more
complex structure or are not actively maintained anymore. This lead to the
birth of ``tgext.mailer``.

tgext.mailer code is adapted from the *pyramid_mailer* project which uses
``repoze.sendmail`` to perform actual email delivery.


Installing
-------------------------------

tgext.mailer can be installed from pypi::

    pip install tgext.mailer

should just work for most of the users.

Enabling
-------------------------------

To enable tgext.mailer put inside your application
``config/app_cfg.py`` the following::

    import tgext.mailer
    tgext.mailer.plugme(base_config)

or you can use ``tgext.pluggable`` when available::

    from tgext.pluggable import plug
    plug(base_config, 'tgext.mailer')

tgext.mailer will then load the options from your application
configuration file, refer to the **Configuration File Options**
section for a complete list of available options.

Sending Emails
--------------------------------

Sending emails is performed through the mailer object, each request has its
own mailer object, which is in charge of sending only the emails of that
request. If you don't pass any request to the ``get_mailer`` call, the
application wide mailer is returned (Do not use it inside a request)::

   from tgext.mailer import get_mailer
   mailer = get_mailer(request)

To send a message, you must first create a
``tgext.mailer.message.Message`` instance::

    from tgext.mailer import Message

    message = Message(subject="hello world",
                      sender="admin@mysite.com",
                      recipients=["john.doe@gmail.com"],
                      body="Hi John!")

The ``Message`` is then passed to the ``Mailer`` instance. You can either
send the message right away::

    mailer.send(message)

or add it to your mail queue (a maildir on disk)::

    mailer.send_to_queue(message)

If you want to send the email without registering it on the transaction manager,
to make sure it gets sent even in case of transaction failures, use::

    mailer.send_immediately(message)


Configuration File Options
--------------------------------

The available settings are listed below. Place them under ``[app:main]`` in your configuration *.ini file.

==========================      ====================================            ===============================
Setting                         Default                                         Description
==========================      ====================================            ===============================
**mail.debugmailer**            **False**                                       Store emails on disk for debugging
**mail.host**                   ``localhost``                                   SMTP host
**mail.port**                   ``25``                                          SMTP port
**mail.username**               **None**                                        SMTP username
**mail.password**               **None**                                        SMTP password
**mail.tls**                    **False**                                       Use TLS
**mail.ssl**                    **False**                                       Use SSL
**mail.keyfile**                **None**                                        SSL key file
**mail.certfile**               **None**                                        SSL certificate file
**mail.queue_path**             **None**                                        Location of maildir
**mail.default_sender**         **None**                                        Default from address
**mail.debug**                  **0**                                           SMTP debug level
==========================      ====================================            ===============================

In test units that have to check for sent email, make sure to set **mail.debugmailer** to ``"dummy"``
it will save outgoing emails in ``mailer.output`` instead of actually sending them.

Transactions
------------

If you are using transaction management then **tgext.mailer** will only 
send the emails (or add them to the mail queue)
when the transactions are committed.

For example::

    import transaction

    from tgext.mailer.mailer import Mailer
    from tgext.mailer import Message

    mailer = Mailer()
    message = Message(subject="hello world",
                      sender="admin@mysite.com",
                      recipients=["john.doe@gmail.com"],
                      body="Hi John!")

    mailer.send(message)
    transaction.commit()


The email is not actually sent until the transaction is committed.

Usually TurboGears will automatically commit the transaction for your
at the end of the request so you don't need to explicitly commit or abort
within code that sends mail.  Instead, if an exception is raised, the
transaction will implicitly be aborted and mail will not be sent; otherwise
it will be committed, and mail will be sent.

If you use the **Application wide email manager** it is usually best practice
to only use ``send_immediately`` method, to avoid registering the same mail manager
in multiple transactions.

Attachments
-----------

Attachments are added using the ``tgext.mailer.message.Attachment``
class::

    from tgext.mailer import Attachment
    from tgext.mailer import Message

    message = Message()

    photo_data = open("photo.jpg", "rb").read()
    attachment = Attachment("photo.jpg", "image/jpg", photo_data)

    message.attach(attachment)

You can pass the data either as a string or file object, so the above code
could be rewritten::


    from tgext.mailer import Attachment
    from tgext.mailer import Message

    message = Message()

    attachment = Attachment("photo.jpg", "image/jpg",
                            open("photo.jpg", "rb"))

    message.attach(attachment)

A transfer encoding can be specified via the ``transfer_encoding`` option.
Supported options are currently ``base64`` (the default) and
``quoted-printable``.

You can also pass an attachment as the ``body`` and/or ``html``
arguments to specify ``Content-Transfer-Encoding`` or other
``Attachment`` attributes::

    from tgext.mailer import Attachment
    from tgext.mailer import Message

    body = Attachment(data="hello, arthur",
                      transfer_encoding="quoted-printable")
    html = Attachment(data="<p>hello, arthur</p>",
                      transfer_encoding="quoted-printable")
    message = Message(body=body, html=html)

