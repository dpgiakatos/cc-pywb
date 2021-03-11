class OutputFieldMapper(object):
    """Allows to map output field names or remove output fields"""

    def __init__(self, field_map={}):
        """
        :param field_map  dictionary with mappings from source to
        target name to rename output fields, or a mapping of source
        field name to `None` to remove a field
        """
        if not isinstance(field_map, dict):
            raise TypeError("Output field map must be of type `dict`")
        self.map = field_map
        # keep deletions in a separate data structure for faster processing
        self.deletions = [k for (k, v) in self.map.items() if not v]
        for k in self.deletions:
            del(self.map[k])

    def __call__(self, res):
        """Wraps the cdx_iter in the supplied tuple returning a
        tuple <wrap_iter(cdx_iter), ...>"""
        cdx_iter, errs = res
        return self.wrap_iter(cdx_iter), errs

    def wrap_iter(self, cdx_iter):
        for cdx in cdx_iter:
            for k in self.deletions:
                if k in cdx:
                    del(cdx[k])
            for k in self.map.keys() & cdx.keys():
                cdx[self.map[k]] = cdx[k]
                del(cdx[k])
            yield cdx
