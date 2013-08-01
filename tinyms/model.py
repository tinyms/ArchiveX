__author__ = 'tinyms'


class ArchiveXConfig():
    Port = 8888
    def dict(self,cfg=None):
        if not cfg:
            m = dict()
            m["Port"] = ArchiveXConfig.Port
            return m
        else:
            ArchiveXConfig.Port = cfg["Port"]
            pass
