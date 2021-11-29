"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from flask import jsonify
from server import *


class SdexaService(WebService):
    def __init__(self, request_context, user_service):
        super().__init__(request_context, user_service)
        self.routes = [
            Route('/surview/sdexa/calculation', self.calculate_bone_density, ["PUT"]),
            Route('/surview/sdexa/soft-tissue-region', self.put_soft_tissue_region, ["PUT"]),
            Route('/surview/sdexa/bone-density-image', self.get_bone_density_image, ["GET"]),
            Route('/surview/sdexa/bone-density-results', self.get_bone_density_results, ["GET"]),
        ]

    def put_soft_tissue_region(self):
        user_session = self.user_service.get_user_session()
        surview = user_session.surview
        if surview is None:
            return ERROR
        region = tuple(map(self.string_to_int, self.get_json_values("posX", "posY", "dx", "dy")))
        surview.set_soft_tissue_region(region)
        return SUCCESS

    def calculate_bone_density(self):
        user_session = self.user_service.get_user_session()
        if not user_session.has_scatter():
            return NOT_FOUND
        try:
            user_session.surview.calculate_bone_density()
        except Exception as exception:
            return str(exception), 400
        return SUCCESS

    def get_bone_density_image(self):
        user_session = self.user_service.get_user_session()
        if not user_session.has_scatter() or user_session.surview.abmd_result is None:
            return NOT_FOUND
        return self.send_jpeg(user_session.surview.get_bone_density_image())

    def get_bone_density_results(self):
        user_session = self.user_service.get_user_session()
        if not user_session.has_scatter() or user_session.surview.abmd_result is None:
            return NOT_FOUND
        return jsonify(
            abmd_mean=f"{user_session.surview.get_bone_density_mean(): .2f}",
            abmd_std=f"{user_session.surview.get_bone_density_std(): .2f}"
        )

