from constants import DEVICE
from state import get_settings, get_context
from models.interface_types import InterfaceType


class ImageGenerator:
    def __init__(self):
        self.app_settings = get_settings()
        self.config = self.app_settings.settings
        self.context = get_context(InterfaceType.CLI)

    def generate_image(self, prompt):
        print("Generating image: " + prompt)
        self.config.lcm_diffusion_setting.prompt = prompt
        result = self.context.generate_text_to_image(
            settings=self.config,
            device=DEVICE,
        )
        return result
