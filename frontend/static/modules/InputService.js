export function InputService() {
    'use strict';

    this.getInputField = field_id => {
        return document.querySelector(`input[id=${field_id}]`);
    }

    return this;
}