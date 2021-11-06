import {baseUrl} from "./config.js";

export function controller() {
    'use strict';
    const vm = this;

    vm.uploadSurview = () => {
        const file = getInputField("surview").files[0];
        uploadFile(file, baseUrl + "surview").then(reloadPage);
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