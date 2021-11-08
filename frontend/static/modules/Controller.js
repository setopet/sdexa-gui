import {baseUrl} from "./config.js";
import {Canvas} from "./Canvas.js";

export function Controller(fileService, modalService, alertService) {
    'use strict';
    const vm = this;

    vm.uploadSurview = () => {
        const file = fileService.getInputFile("surview");
        const canvas = new Canvas("surview-modal-canvas", 1900, 700);
        fileService.uploadFile(file, baseUrl + "surview")
            .then(getFullSurview)
            .then(blob => canvas.drawImage(blob))
            .then(() => canvas.drawRectangle(512,512, 800, 0))
            .then(() => modalService.openFullscreen("surviewModal"))
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