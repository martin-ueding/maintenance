.. Copyright © 2013 Martin Ueding <dev@martin-ueding.de>

#########
Changelog
#########

v1.7.14
    - *git-autopush*: Enable fetch again

v1.7.13
    - Move all the task script from ``/usr/bin`` to
      ``/usr/lib/maintenance/tasks``. That way, Debian Linitan does not
      complain about missing manual pages. Also, it will motivate the user to
      run the tasks through the ``maintenance`` program instead of invocing the
      scripts directly.

v1.7.12
    - **Added**: *octave-history* to clean out ``.octave_hist``
    - **Added**: *xauthority* to clean in ``~``
    - **Added**: *xsession-errors* to clean in ``~``
    - Use ``with`` statement in locks

v1.7.11
    - *git-autopush*: Split up finding of repos into *git-find-repos* script
    - **Added**: *git-find-repos*
    - *git-autopush*: Cache the last published commits in order to remove the
      remote refs in ``git log``.

v1.7.10
    - *backup-chaos*: Backup ``Dokumente/Listen``

v1.7.9
    - **Added**: *download-mysql-backup*

v1.7.8
    - *git-autopush*: Rewrite in Python 3

v1.7.7
    - *ctags*: Prevent script from failing
    - *git-autopush*: Fetch first

v1.7.6
    - *git-autopush*: Fetch foreign remotes

v1.7.5
    - *rebuild-website*: Remove since it is buggy

v1.7.4
    - *git-autopush*: Reflect name change in ``git-push-*``

v1.7.3
    - **Added**: Generate ``tags`` file with ``ctags``

v1.7.2
    - *git-autopush*: Fix spacing in all cases
    - *maintenance*: Improve output by forcing the output of one thread into
      one block.
    - *ppa*: Change the series after it has been changed from ``UNRELEASED``

v1.7.1
    - *git-autopush*: Fix spacing

v1.7
    - *rebuild-website*: Log the output
    - Show output of the one disk heavy task
    - Add override to run selected tasks

v1.6
    - *Added*: Rebuild my personal website
    - Change the interval of tasks

v1.5.6
    - *git-autopush*: Push repos to bitbucket

v1.5.5
    - Let script succeed

v1.5.4
    - Run ``backup-chaos`` more often

v1.5.3
    - Prevent scripts from failing

v1.5.2
    - Fix JSON notation

v1.5.1
    - **Added**: Remove flash cookies
    - Make output of blank lines consistent

v1.5
    - **Added**: Clean up ``.DS_Store``
    - *ppa*: Improve package handling

v1.4.4
    - *git-autopush*: Let ``git-autopush`` write to ``backup-status``

v1.4.3
    - *git-autopush*: Dirty → Push

v1.4.2
    - *git-autopush*: Create git repos on remotes automatically, if they are
      missing
    - Run git-autopush more often

v1.4.1
    - Copy podcasts to devices

v1.4
    - *git-autopush*: Show which git repos needs to be created on the remote
      servers.

v1.3.4
    - Run PPA script more often

v1.3.3
    - **Added**: peer-review
    - Print whole command

v1.3.2
    - *ppa*: Perform upgrades as well
    - Print waiting tasks as well

v1.3.1
    - New tasks

v1.3
    - ``--local`` option
    - Minor fixes in scripts
    - Only check for power if possible

v1.2
    - List with public packages into config
    - GPLv2+ license

v1.1.1
    - **Added**: New tasks
    - *ppa*: Publish more packages

v1.1
    - Multiple processes in parallel

v1.0.2
    - Fix syntax error

v1.0.1
    - Save after every run
    - Fixes in scripts

v1.0
    - Use ``tasks.js`` to organize tasks

v0.9.2
    - *ppa*: More packages uploaded

v0.9.1
    - *ppa*: Upload maintenance scripts as well

v0.9
    Initial version
