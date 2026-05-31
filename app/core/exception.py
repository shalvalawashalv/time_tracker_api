class ActivityNotFoundError(Exception):
    pass


class ActiveSessionAlreadyExistsError(Exception):
    pass


class SessionNotFoundError(Exception):
    pass


class SessionAlreadyStoppedError(Exception):
    pass


class SessionNotCompletedError(Exception):
    pass


class DataConsistencyError(Exception):
    pass