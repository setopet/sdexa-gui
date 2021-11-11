export function LoadingAnimation(id) {
    'use strict';

    const getAnimationHtml = () => {
        return `
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>`
    }

    const savedHtml = document.getElementById(id).innerHTML;
    document.getElementById(id).innerHTML = getAnimationHtml();

    this.stop = () => {
        document.getElementById(id).innerHTML = savedHtml;
        return this;
    }

    return this;
}