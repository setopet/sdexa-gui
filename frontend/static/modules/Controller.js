import {baseUrl} from "./config.js";
import {SelectionCanvas} from "./SelectionCanvas.js";

export function Controller(fileService, modalService, alertService) {
    'use strict';
    const vm = this;

    vm.uploadSurview = () => {
        const file = fileService.getInputFile("surview");
        fileService.uploadFile(file, baseUrl + "surview")
            .then(getFullSurview)
            .then(blob => {
                vm.canvas = new SelectionCanvas("surview-modal-canvas", blob, 1900, 700);
                return vm.canvas.init();
            })
            .then(() => modalService.openFullscreen("surviewModal"))
            .catch(alertService.error);
    }

    vm.finishSurviewCropping = () => {
        fetch(baseUrl + "surview/cropping", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'posX': vm.canvas.getX(), 'posY': vm.canvas.getY()})
        })
            .then(reloadPage)
            .catch(alertService.error);
    }

    vm.showSegmentation = () => {
        fetch(baseUrl + "surview/segmentation", { method: 'PUT' })
            .then(reloadPage)
            .catch(alertService.error);
    }

    vm.downloadSegmentation = () => {
        fileService
            .downloadFile(baseUrl + "surview/segmentation/download", "segmentation.csv")
            .catch(alertService.error);
    }

    vm.downloadImage = () => {
        fileService
            .downloadFile(baseUrl + "surview/download", "surview.csv")
            .catch(alertService.error);
    }

    vm.uploadCtProjection = () => {
        const file = fileService.getInputFile("ct_projection");
        fileService
            .uploadFile(file, baseUrl + "ct-projection")
            .then(reloadPage)
            .catch(alertService.error);
    }

    const getFullSurview = () => {
        return fetch(baseUrl + "surview/full")
            .then(response => response.blob())
            .catch(alertService.error);
    }

    const reloadPage = () => {
        location.href = '/';
        return Promise.resolve();
    }

    return vm;
}