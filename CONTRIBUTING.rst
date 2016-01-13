============
CONTRIBUTING
============

Bug reports
===========

File issues about incorrect data, things to add, etc here:

https://github.com/pyvideo/pyvideo-data/issues

.. Note::

   All work is done on a volunteer basis, so if you write up an issue, it may
   sit there forever.


Working on issues in the issue tracker
======================================

Before working on issues in the issue tracker, please add a comment to the issue
stating that you're planning to work on it and any other details you think are
helpful to communicate with everyone else.

For example::

    I'd like to work on this issue. If I don't hear from anyone in the next
    couple of days, I'll work on it and submit a pull request.


Then work on the task and produce a pull request.

Someone with authority will review the pull request and you'll go back and
forth with that person honing the data until it's good enough. At that point,
the person will merge it.


Adding new conferences/files
============================

Before adding any new data, please create an issue for it in the issue tracker.

Data is located in ``data/``.

The top level of directories are by user group or conference. Directory names
are slugs.

Inside those directories, create one JSON file for each individual video.


Editing existing data
=====================

Before editing any data, please create an issue for it in the issue tracker.

Files can be edited with any editor. You can also write scripts. Make sure
any changes you make aren't destructive.
