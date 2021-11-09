export function InputService() {
    'use strict';

    this.getInputFile = field_id => {
        return document.querySelector(`input[id=${field_id}]`);
    }

    return this;
}