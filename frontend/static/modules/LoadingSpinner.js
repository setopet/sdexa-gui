export function LoadingSpinner(field_id) {
    'use strict';

    const getAnimationHtml = () => {
        return `<div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>`
    }

    const savedHtml = document.getElementById(field_id).innerHTML;
    document.getElementById(field_id).innerHTML = getAnimationHtml();

    this.stop = () => {
        document.getElementById(field_id).innerHTML = savedHtml;
    }

    return this;
}