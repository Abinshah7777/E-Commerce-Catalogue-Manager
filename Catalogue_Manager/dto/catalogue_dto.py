class Catalogue:
    def __init__(self, catalogue_id, catalogue_name, catalogue_version,
                 is_cat_active, catalogue_start, catalogue_end):
        self.catalogue_id = catalogue_id
        self.catalogue_name = catalogue_name
        self.catalogue_version = catalogue_version
        self.is_cat_active = is_cat_active
        self.catalogue_start = catalogue_start
        self.catalogue_end = catalogue_end

    def __str__(self):
        return (f"ID: {self.catalogue_id}, Name: {self.catalogue_name}, "
                f"Version: {self.catalogue_version}, Active: {'Yes' if self.is_cat_active else 'No'}, "
                f"Start: {self.catalogue_start}, End: {self.catalogue_end}")

    def to_dict(self):
        return self.__dict__
