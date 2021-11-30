"""@author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM"""
from flask import render_template
from config import CONFIG
from server import *


class Server:
    """Initializes web_services and gets their routes."""
    def __init__(self):
        self.routes = [
            Route('/', self.get_root_page, ["GET"])
        ]
        self.user_service = UserService(SessionContext())
        request_context = RequestContext()
        self.routes.extend(SurviewService(request_context, self.user_service).routes)
        self.routes.extend(SegmentationService(request_context, self.user_service).routes)
        self.routes.extend(ScatterService(request_context, self.user_service).routes)
        self.routes.extend(SdexaService(request_context, self.user_service).routes)
        self.routes.extend(ProjectionService(request_context, self.user_service).routes)
        self.routes.extend(RegistrationService(request_context, self.user_service).routes)

    def get_root_page(self):
        user_session = self.user_service.get_user_session()
        return render_template('index.html',
                               surview_present=user_session.has_surview(),
                               scatter_present=user_session.has_scatter(),
                               projection_present=user_session.has_projection(),
                               registration_present=user_session.has_registration())
