from typing import Optional

from bubop import logger
from bubop.exceptions import AuthenticationError
from gkeepapi import Keep
from gkeepapi.node import Label
from gkeepapi.node import List as GKeepList
from gkeepapi.node import TopLevelNode

from taskwarrior_syncall.sync_side import SyncSide


class GKeepSide(SyncSide):
    def __init__(self, gkeep_user: str, gkeep_passwd: str, **kargs):
        self._keep: Keep
        self._gkeep_user = gkeep_user
        self._gkeep_passwd = gkeep_passwd

        super().__init__(**kargs)

    def start(self):
        super().start()
        logger.debug("Connecting to Google Keep...")
        self._keep = Keep()
        success = self._keep.login(self._gkeep_user, self._gkeep_passwd)
        if not success:
            raise AuthenticationError(appname="Google Keep")

        logger.debug("Connected to Google Keep.")

    def finish(self):
        logger.info("Flushing data to remote Google Keep...")
        self._keep.sync()

    def _note_has_label(self, note: TopLevelNode, label: Label) -> bool:
        """True if the given Google Keep note has the given label."""
        for la in note.labels.all():
            if label == la:
                return True

        return False

    def _note_has_label_str(self, note: TopLevelNode, label_str: str) -> bool:
        """True if the given Google Keep note has the given label."""
        for la in note.labels.all():
            if label_str == la.name:
                return True

        return False

    def _get_label_by_name(self, label: str) -> Optional[Label]:
        for la in self._keep.labels():
            if la.name == label:
                return la

    def _create_list(self, title: str, label: Optional[Label] = None) -> GKeepList:
        """Create a new list of items in Google Keep.

        Applies the given label to the note - if one was provided
        """
        li = self._keep.createList(title)
        if label is not None:
            li.labels.add(label)

        return li
