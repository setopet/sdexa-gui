import {Controller} from "./Controller.js";
import {FileService} from "./FileService.js";
import {Canvas} from "./Canvas.js";
import {ModalService} from "./ModalService.js";
import {AlertService} from "./AlertService.js";

function getInstance (factory, ...dependencies) {
    const instance = {};
    return factory.bind(instance)(...dependencies);
}

const fileService = getInstance(FileService);
const modalService = getInstance(ModalService);
const alertService = getInstance(AlertService);

window.$ctrl = getInstance(Controller, fileService, modalService, alertService);