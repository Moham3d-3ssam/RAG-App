from helpers.config import get_settings, SettingsConfigDict

class BaseController:
  
  def __init__(self):
    self.app_settings = get_settings()