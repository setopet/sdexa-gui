/** @author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM **/
import {Controller} from "./Controller.js";
import {HttpService} from "./services/HttpService.js";
import {FileService} from "./services/FileService.js";
import {AlertService} from "./services/AlertService.js";

function getInstance (constructor, ...dependencies) {
    const instance = {};
    return constructor.bind(instance)(...dependencies);
}

const httpService = getInstance(HttpService);
const fileService = getInstance(FileService);
const alertService = getInstance(AlertService);

window.$ctrl = getInstance(Controller, httpService, fileService, alertService);