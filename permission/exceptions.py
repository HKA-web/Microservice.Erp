class PermissionError(Exception):
    pass


class NotUserNorGroup(PermissionError):
    pass


class ObjectNotPersisted(PermissionError):
    pass


class WrongAppError(PermissionError):
    pass


class MixedContentTypeError(PermissionError):
    pass


class MultipleIdentityAndObjectError(PermissionError):
    pass
