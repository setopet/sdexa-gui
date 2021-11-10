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
        dropField.ondrop = (evt => {
            evt.preventDefault();
            dropField.style.backgroundColor = '';
            callback(evt.dataTransfer.files[0]);
        });
        dropField.ondragover = evt => {
            evt.preventDefault();
            dropField.style.backgroundColor = 'lightskyblue';
        };
        dropField.ondragleave = () => {
            dropField.style.backgroundColor = '';
        }
    }

    const getField = (field_id) => {
        return document.getElementById(field_id);
    }

    return this;
}