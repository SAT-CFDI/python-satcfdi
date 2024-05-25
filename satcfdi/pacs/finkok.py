from . import PAC, Environment


class Finkok(PAC):
    """
    Finkok, S.A. P. I. de C.V.
    Finkok
    """

    RFC = "FIN1203015JA"

    def __init__(
        self, username: str, password: str, environment=Environment.PRODUCTION
    ):
        super().__init__(environment)
        self.username = username
        self.password = password

    @property
    def host(self):
        if self.environment == Environment.TEST:
            return "https://demo-facturacion.finkok.com"
        return "https://facturacion.finkok.com"
