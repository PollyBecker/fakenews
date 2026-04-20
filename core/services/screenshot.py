import io

try:
    from PIL import ImageGrab
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


class ScreenshotService:
    def __init__(self, navigator=None):
        self.navigator = navigator

    def capture(self) -> bytes:
        if self.navigator:
            return self.navigator.get_screenshot()

        if PIL_AVAILABLE:
            img = ImageGrab.grab()
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            return buf.getvalue()

        return b''
