from app.service.raspberrypi.serivce import RaspberryPiService


class RaspberryPiServiceImpl(RaspberryPiService):
    def get_weather(self, reader):
        return super().get_weather(reader)

    def auth_user(self):
        return super().auth_user()
