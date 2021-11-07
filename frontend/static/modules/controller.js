import {baseUrl} from "./config.js";

export function controller() {
    'use strict';
    const vm = this;

    vm.uploadSurview = () => {
        const file = getInputField("surview").files[0];
        uploadFile(file, baseUrl + "surview").then(reloadPage);
    }

    vm.showSegmentation = () => {
        fetch(baseUrl + "surview/segmentation", { method: 'PUT' }).then(reloadPage);
    }

    vm.downloadSegmentation = () => {
        // Credits to https://stackoverflow.com/questions/32545632/how-can-i-download-a-file-using-window-fetch
        fetch(baseUrl + "surview/segmentation/download", { method: 'GET'})
            .then(response => response.blob())
            .then(blob => {
                const link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = "segmentation.csv";
                document.body.appendChild(link);
                link.click();
                link.remove();
            })
    }

    vm.uploadCtProjection = () => {
        const file = getInputField("ct_projection").files[0];
        uploadFile(file, baseUrl + "ct-projection").then(reloadPage);
    }

    const uploadFile = (file, route) => {
        const data = new FormData();
        data.append('file', file);
        return fetch(route, {
            method: 'POST',
            body: data
        });
    }

    const getInputField = (field_id) => {
        return document.querySelector(`input[id=${field_id}]`);
    }

    const reloadPage = () => {
        location.href = '/';
    }

    return vm;
}