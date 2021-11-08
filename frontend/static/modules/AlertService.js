export function AlertService() {
    // TODO: Fehler in AlertBox anzeigen
    this.error = e => {
        console.log(e);
    }

    return this;
}