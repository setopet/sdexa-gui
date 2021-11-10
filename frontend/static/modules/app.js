import {Controller} from "./Controller.js";
import {HttpService} from "./HttpService.js";
import {InputService} from "./InputService.js";
import {ModalService} from "./ModalService.js";
import {AlertService} from "./AlertService.js";

function getInstance (constructor, ...dependencies) {
    const instance = {};
    return constructor.bind(instance)(...dependencies);
}

const httpService = getInstance(HttpService);
const modalService = getInstance(ModalService);
const inputService = getInstance(InputService);
const alertService = getInstance(AlertService);

window.$ctrl = getInstance(Controller, httpService, modalService, inputService, alertService);