from server import *


class SegmentationService(WebService):
    def __init__(self, request_context, user_service):
        super().__init__(request_context, user_service)
        self.routes = [
            Route('/surview/segmentation', self.switch_surview_segmention_view, ["PUT"]),
            Route('/surview/segmentation/download', self.download_surview_segmentation, ["GET"])
        ]

    # TODO: Statt switch mit Zustand hier ein GET und im UI über Karussel wird immer beides geladen
    def switch_surview_segmention_view(self):
        user_session = self.user_service.get_user_session()
        if not user_session.has_surview():
            return ERROR
        user_session.switch_surview_segmentation()
        return SUCCESS

    def download_surview_segmentation(self):
        user_session = self.user_service.get_user_session()
        if not user_session.has_surview():
            return NOT_FOUND
        csv = user_session.get_surview_segmentation_csv()
        return self.send_csv(csv)