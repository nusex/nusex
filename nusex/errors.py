class NusexError(Exception):
    pass


class InitFailure(NusexError):
    pass


class NotInitialised(NusexError):
    pass


class TemplateBuildError(NusexError):
    pass


class TemplateRenameError(NusexError):
    pass


class NoMatchingTemplates(NusexError):
    pass
