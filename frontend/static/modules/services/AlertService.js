/** @author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM **/
/** Shows error messages inside the alert list. **/
export function AlertService() {
    const alertList = document.getElementById("alert-list");

    const getAlertHtml = (message, type) => {
        return `
            <div class="alert alert-${type}" role="alert">
                <span>${message}</span>
                <button type="button" class="btn-close float-end" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>`;
    }

    /** Adds an info alert to the alert list. **/
    this.message = message => {
        alertList.innerHTML += "\n" + getAlertHtml(message, "info");
    }

    /** Adds an error alert with the messages of the error to the alert list. **/
    this.error = error => {
        alertList.innerHTML += "\n" + getAlertHtml(`
            <strong>An error occured while processing your request:</strong> ${error.message}`,
            "danger");
    }

    this.clear = () => {
        alertList.innerHTML = "";
    }

    return this;
}