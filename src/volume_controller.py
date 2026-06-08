import platform


class SystemVolumeController:
    """Controls system volume on Windows using pycaw."""

    def __init__(self, mock=False):
        self.mock = mock
        self.available = False
        self.current_mock_volume = 50
        self.volume = None
        self.message = ""

        if self.mock:
            self.message = "Running in mock mode. System volume will not be changed."
            return

        if platform.system() != "Windows":
            self.message = "System volume control is only available on Windows."
            return

        try:
            from ctypes import POINTER, cast

            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_,
                CLSCTX_ALL,
                None,
            )

            self.volume = cast(interface, POINTER(IAudioEndpointVolume))
            self.available = True
            self.message = "System volume control is active."

        except Exception as error:
            self.message = f"Could not initialize system volume control: {error}"

    def set_volume_percent(self, percent):
        percent = max(0, min(100, int(percent)))

        if self.available and self.volume is not None:
            self.volume.SetMasterVolumeLevelScalar(percent / 100, None)
        else:
            self.current_mock_volume = percent

    def get_volume_percent(self):
        if self.available and self.volume is not None:
            return int(self.volume.GetMasterVolumeLevelScalar() * 100)

        return int(self.current_mock_volume)
