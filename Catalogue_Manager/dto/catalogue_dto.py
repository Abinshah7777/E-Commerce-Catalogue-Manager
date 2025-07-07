from datetime import date, datetime

class Catalogue:
    def __init__(self, catalogue_id, catalogue_name, catalogue_version, is_cat_active, catalogue_start, catalogue_end):
        self.catalogue_id = catalogue_id
        self.catalogue_name = catalogue_name
        self.catalogue_version = catalogue_version
        self.is_cat_active = is_cat_active
        self.catalogue_start = catalogue_start
        self.catalogue_end = catalogue_end

    def to_dict(self):
        return {
            "catalogue_id": self.catalogue_id,
            "catalogue_name": self.catalogue_name,
            "catalogue_version": self.catalogue_version,
            "is_cat_active": self.is_cat_active,
            "catalogue_start": self.catalogue_start.strftime('%Y-%m-%d') if isinstance(self.catalogue_start, (date, datetime)) else self.catalogue_start,
            "catalogue_end": self.catalogue_end.strftime('%Y-%m-%d') if isinstance(self.catalogue_end, (date, datetime)) else self.catalogue_end
        }
