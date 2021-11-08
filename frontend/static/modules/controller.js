import {baseUrl} from "./config.js";

export function Controller(fileService) {
    'use strict';
    const vm = this;

    vm.uploadSurview = () => {
        const file = getInputField("surview").files[0];
        fileService.uploadFile(file, baseUrl + "surview")
            .then(getFullSurview)
            .then(openSurviewModal);
    }

    vm.showSegmentation = () => {
        fetch(baseUrl + "surview/segmentation", { method: 'PUT' }).then(reloadPage);
    }

    vm.downloadSegmentation = () => {
        fileService.downloadFile(baseUrl + "surview/segmentation/download", "segmentation.csv");
    }

    vm.downloadImage = () => {
        fileService.downloadFile(baseUrl + "surview/download", "surview.csv");
    }

    vm.uploadCtProjection = () => {
        const file = getInputField("ct_projection").files[0];
        fileService.uploadFile(file, baseUrl + "ct-projection").then(reloadPage);
    }

    const getFullSurview = () => {
        fetch(baseUrl + "surview/full")
            .then(response => response.blob())
            .then(drawImage);
    }

    const drawImage = (blob) => {
        const image = new Image();
        const imageSrc = URL.createObjectURL(blob);
        const canvas = document.getElementById("surview-modal-canvas");
        canvas.width = 1900;
        canvas.height = 700;
        const context = canvas.getContext("2d");
        image.onload = event => context.drawImage(event.target, 0, 0);
        image.src = imageSrc;
    }

    const openSurviewModal = () => {
        const myModal = new bootstrap.Modal(document.getElementById('surviewModal'));
        myModal.show();
    }

    const getInputField = (field_id) => {
        return document.querySelector(`input[id=${field_id}]`);
    }

    const reloadPage = () => {
        location.href = '/';
    }

    return vm;
}