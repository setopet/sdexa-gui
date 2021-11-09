import {baseUrl} from "./config.js";
import {SelectionCanvas} from "./SelectionCanvas.js";


export function Controller(fileService, modalService, alertService) {
    'use strict';
    const vm = this;

    // TODO: Fehlermanagement über .catch ermöglichen, indem bei jedem fetch() der StatusCode gecheckt wird
    //  -> dafür fetch()-Calls in HttpService auslagern
    vm.uploadSurview = () => {
        const file = fileService.getInputFile("surview");
        fileService.uploadFile(file, baseUrl + "surview")
            .then(getFullSurview)
            .then(initSelectionCanvas)
            .then(() => openSurviewModal())
            .catch(alertService.error);
    }

    vm.uploadCtProjection = () => {
        const file = fileService.getInputFile("ct_projection");
        fileService
            .uploadFile(file, baseUrl + "projection")
            .then(getFullCtProjection)
            .then(initSelectionCanvas)
            .then(() => openCtModal())
            .catch(alertService.error);
    }

    vm.switchSurviewView = () => {
        fetch(baseUrl + "surview/segmentation", { method: 'PUT' })
            .then(reloadPage)
            .catch(alertService.error);
    }

    vm.switchProjectionView = () => {
        fetch(baseUrl + "projection/registration", { method: 'PUT' })
            .then(reloadPage)
            .catch(alertService.error);
    }

    vm.downloadImage = (route, fileName) => {
        fileService
            .downloadFile(baseUrl + route, fileName)
            .catch(alertService.error);
    }

    const putImagePosition = (url) => {
        const position = { 'posX': vm.selectionCanvas.getX(), 'posY': vm.selectionCanvas.getY() };
        putJsonToUrl(url, position)
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
        return fetch(baseUrl + "surview/full")
            .then(response => response.blob())
    }

    const getFullCtProjection = () => {
        return fetch(baseUrl + "projection/full")
            .then(response => response.blob())
    }

    const putJsonToUrl = (url, data) => {
        return fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
    }

    const reloadPage = () => {
        location.href = '/';
        return Promise.resolve(this);
    }

    return vm;
}