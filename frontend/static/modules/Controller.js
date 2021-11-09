import {baseUrl} from "./config.js";
import {SelectionCanvas} from "./SelectionCanvas.js";


export function Controller(httpService, modalService, inputService, alertService) {
    'use strict';
    const vm = this;

    vm.uploadSurview = () => {
        const file = inputService.getInputFile("surview").files[0];
        httpService.uploadFile(file, baseUrl + "surview")
            .then(getFullSurview)
            .then(initSelectionCanvas)
            .then(() => openSurviewModal())
            .catch(alertService.error);
    }

    vm.uploadCtProjection = () => {
        const file = inputService.getInputFile("ct_projection").files[0];
        httpService
            .uploadFile(file, baseUrl + "projection")
            .then(getFullCtProjection)
            .then(initSelectionCanvas)
            .then(() => openCtModal())
            .catch(alertService.error);
    }

    vm.switchSurviewView = () => {
        httpService.put(baseUrl + "surview/segmentation")
            .then(reloadPage)
            .catch(alertService.error);
    }

    vm.switchProjectionView = () => {
        httpService.put(baseUrl + "projection/registration")
            .then(reloadPage)
            .catch(alertService.error);
    }

    vm.downloadImage = (route, fileName) => {
        httpService
            .downloadFile(baseUrl + route, fileName)
            .catch(alertService.error);
    }

    const putImagePosition = (url) => {
        const position = { 'posX': vm.selectionCanvas.getX(), 'posY': vm.selectionCanvas.getY() };
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

    const openCtModal = () => {
        const title =
            "Move the rectangle by clicking on the projection image to select the area for registration." +
            "Click the OK button when you are finished.";
        return modalService.openFullscreen(title, () => putImagePosition(baseUrl + "projection/position"));
    }

    const initSelectionCanvas = blob =>  {
        vm.selectionCanvas = new SelectionCanvas("modal-canvas", blob);
        return vm.selectionCanvas.init();
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