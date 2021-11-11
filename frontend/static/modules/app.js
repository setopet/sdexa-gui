import {Controller} from "./Controller.js";
import {HttpService} from "./services/HttpService.js";
import {FileService} from "./services/FileService.js";
import {ModalService} from "./services/ModalService.js";
import {AlertService} from "./services/AlertService.js";

function getInstance (constructor, ...dependencies) {
    const instance = {};
    return constructor.bind(instance)(...dependencies);
}

const httpService = getInstance(HttpService);
const modalService = getInstance(ModalService);
const fileService = getInstance(FileService);
const alertService = getInstance(AlertService);

window.$ctrl = getInstance(Controller, httpService, modalService, fileService, alertService);