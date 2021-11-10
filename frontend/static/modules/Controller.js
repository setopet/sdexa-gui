import {baseUrl} from "./config.js";
import {ModalCanvas} from "./ModalCanvas.js";


export function Controller(httpService, modalService, inputService, alertService) {
    'use strict';
    const vm = this;

    // wenn ich über EventListener gehe, muss ich diese Methode sowieso so schreiben,
    // dass das File woanders herkommen kann.
    vm.uploadSurview = () => {
        const file = inputService.getInputField("surview").files[0];
        httpService.uploadFile(file, baseUrl + "surview")
            .then(getFullSurview)
            .then(initModalCanvas)
            .then(() => openSurviewModal())
            .catch(alertService.error);
    }

    vm.uploadCtProjection = () => {
        const file = inputService.getInputField("projection").files[0];
        httpService
            .uploadFile(file, baseUrl + "projection")
            .then(getFullCtProjection)
            .then(initModalCanvas)
            .then(() => openProjectionModal())
            .catch(alertService.error);
    }

    vm.switchImageView = (route) => {
        httpService.put(baseUrl + route)
            .then(reloadPage)
            .catch(alertService.error);
    }

    vm.downloadImage = (route, fileName) => {
        httpService
            .downloadFile(baseUrl + route, fileName)
            .catch(alertService.error);
    }

    const putImagePosition = (url) => {
        const position = { 'posX': vm.modalCanvas.getX(), 'posY': vm.modalCanvas.getY() };
        httpService.put(url, position)
            .then(reloadPage)
            .catch(alertService.error);
    }

    const openSurviewModal = () => {
        const title =
            "Move the rectangle by clicking on the surview image to select the area for segmenation." +
            "Click the OK button when you are finished.";
        return modalService.openFullscreen(title, () => putImagePosition(baseUrl + "surview/position"));
    }

    const openProjectionModal = () => {
        const title =
            "Move the rectangle by clicking on the projection image to select the area for registration." +
            "Click the OK button when you are finished.";
        return modalService.openFullscreen(title, () => putImagePosition(baseUrl + "projection/position"));
    }

    const initModalCanvas = blob =>  {
        vm.modalCanvas = new ModalCanvas(blob);
        return vm.modalCanvas.init();
    }

    const getFullSurview = () => {
        return httpService.get(baseUrl + "surview/full")
            .then(response => response.blob())
    }

    const getFullCtProjection = () => {
        return httpService.get(baseUrl + "projection/full")
            .then(response => response.blob())
    }

    const reloadPage = () => {
        location.href = '/';
        return Promise.resolve(this);
    }

    return vm;
}