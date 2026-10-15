from  .BaseController import BaseController

class DataController(BaseController):
    def __init__(self):
        # Call the parent class constructor to initialize app_settings (اصحي يا بابا )
        super().__init__()

    # make  a  new function to validate the file extension and size
    def validate_uploaded_file(self, file):
        pass  # TODO: check file.content_type and file.size against self.app_settings
