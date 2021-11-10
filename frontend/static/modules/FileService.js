export function FileService() {
    'use strict';

    this.watchFileInput = (field_id, callback) => {
        const inputField = getField(field_id);
        inputField.addEventListener("change", () => {
            callback(inputField.files[0]);
        })
    }

    this.watchFileDrop = (field_id, callback) => {
        const dropField = getField(field_id);
        dropField.ondragover = evt => {
            console.log("hey");
            evt.preventDefault();
        };
        dropField.ondrop = (evt => {
            console.log("hey");
            evt.preventDefault();
            callback(evt.dataTransfer.files[0]);
        });
    }

    const getField = (field_id) => {
        return document.getElementById(field_id);
    }

    this.onFileDrop = event => {
        event.preventDefault();
        console.log(event);
    }


    return this;
}