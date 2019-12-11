from bauh.api.abstract.model import SoftwarePackage
from bauh.api.constants import CACHE_PATH
from bauh.commons import resource
from bauh.gems.web import ROOT_DIR


class WebApplication(SoftwarePackage):

    def __init__(self, url: str = None, name: str = None, description: str = None, icon_url: str = None,
                 installation_dir: str = None, desktop_entry: str = None, installed: bool = False, version: str = None):
        super(WebApplication, self).__init__(id=url, name=name, description=description,
                                             icon_url=icon_url, installed=installed, version=version)
        self.url = url
        self.installation_dir = installation_dir
        self.desktop_entry = desktop_entry

    def has_history(self):
        return False

    def has_info(self):
        return self.installed

    @staticmethod
    def _get_cached_attrs() -> tuple:
        return 'name', 'version', 'url', 'description', 'icon_url', 'installation_dir', 'desktop_entry'

    def can_be_downgraded(self):
        return False

    def get_exec_path(self) -> str:
        if self.installation_dir:
            return '{}/{}'.format(self.installation_dir, self.installation_dir.split('/')[-1])

    def get_type(self):
        return 'web'

    def get_type_icon_path(self) -> str:
        return self.get_default_icon_path()

    def get_default_icon_path(self) -> str:
        return resource.get_path('img/web.png', ROOT_DIR)

    def is_application(self):
        return True

    def supports_disk_cache(self):
        return self.installed

    def get_disk_cache_path(self):
        return self.installation_dir

    def get_data_to_cache(self) -> dict:
        data = {}

        for attr in self._get_cached_attrs():
            if hasattr(self, attr):
                val = getattr(self, attr)

                if val is not None:
                    data[attr] = val

        return data

    def fill_cached_data(self, data: dict):
        for attr in self._get_cached_attrs():
            val = data.get(attr)

            if val and hasattr(self, attr):
                setattr(self, attr, val)

    def can_be_run(self) -> bool:
        return self.installed and self.installation_dir

    def is_trustable(self) -> bool:
        return False

    def get_publisher(self) -> str:
        pass

    def has_screenshots(self) -> bool:
        return False
