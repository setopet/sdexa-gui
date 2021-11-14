/** Shows error messages inside the alert list. **/
export function AlertService() {
    'use strict';

    const getAlertHtml = message => {
        return `
            <div class="alert alert-danger" role="alert">
                <span><strong>An error occured while processing your request:</strong> ${message}</span>
                <button type="button" class="btn-close float-end" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>`;
    }

    /** Add an error alert with the messages of the error to the alert list. **/
    this.error = error => {
        const alertList = document.getElementById("alert-list");
        alertList.innerHTML += "\n" + getAlertHtml(error.message);
    }

    return this;
}