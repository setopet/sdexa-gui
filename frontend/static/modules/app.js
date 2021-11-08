import {Controller} from "./Controller.js";
import {FileService} from "./FileService.js";

function getInstance (factory, ...dependencies) {
    const instance = {};
    return factory.bind(instance)(...dependencies);
}

const fileService = getInstance(FileService);
const controller = getInstance(Controller, fileService);

window.$ctrl = controller;