from server import *


# TODO: Könnte eine ganze Ergebnisseite als HTML zurückgeben wo die ganzen Werte vorausgefüllt sind anhand des Calculation Results
class SdexaService(WebService):
    def __init__(self, request_context, user_service):
        super().__init__(request_context, user_service)
        self.routes = [
            Route('/surview/sdexa/calculation', self.calculate_bone_density, ["PUT"]),
            Route('/surview/sdexa/soft-tissue-region', self.put_soft_tissue_region, ["PUT"]),
            Route('/surview/sdexa/bone-density-image', self.get_bone_density_image, ["GET"])
        ]

    def put_soft_tissue_region(self):
        user_session = self.user_service.get_user_session()
        if not user_session.has_surview():
            return ERROR
        region = tuple(map(self.string_to_int, self.get_json_values("posX", "posY", "dx", "dy")))
        user_session.set_surview_soft_tissue_region(region)
        return SUCCESS

    def calculate_bone_density(self):
        user_session = self.user_service.get_user_session()
        if not user_session.has_scatter():
            return NOT_FOUND
        user_session.surview.calculate_bone_density()
        return SUCCESS

    def get_bone_density_image(self):
        user_session = self.user_service.get_user_session()
        if not user_session.has_scatter() or user_session.surview.abmd_result is None:
            return NOT_FOUND
        return self.send_jpeg(user_session.surview.get_bone_density_image())
