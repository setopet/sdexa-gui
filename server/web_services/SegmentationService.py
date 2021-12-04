"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from server import *


class SegmentationService(WebService):
    """Handles REST routes for the segmentation of the surview"""
    def __init__(self, request_context, user_service):
        super().__init__(request_context, user_service)
        self.routes = [
            Route('/surview/segmentation', self.get_surview_segmentation, ["GET"]),
            Route('/surview/segmentation', self.set_custom_segmentation, ["POST"]),
            Route('/surview/segmentation/download', self.download_surview_segmentation, ["GET"])
        ]

    def get_surview_segmentation(self):
        user_session = self.user_service.get_user_session()
        surview = user_session.surview
        if surview is None:
            return NOT_FOUND
        return self.send_jpeg(surview.get_segmentation_overlay_image())

    def download_surview_segmentation(self):
        user_session = self.user_service.get_user_session()
        surview = user_session.surview
        if surview is None:
            return NOT_FOUND
        csv = surview.get_segmentation_csv()
        return self.send_csv(csv)

    def set_custom_segmentation(self):
        user_session = self.user_service.get_user_session()
        surview = user_session.surview
        if surview is None:
            return ERROR
        request = self.request_context.get()
        try:
            surview.set_custom_segmentation(self.get_file(request))
        except Exception as exception:
            return str(exception), 400
        return SUCCESS
