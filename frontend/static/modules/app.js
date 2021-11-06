import {controller} from "./controller.js";

function getInstance (factory) {
    const instance = {};
    return factory.bind(instance)();
}

window.$ctrl = getInstance(controller);
