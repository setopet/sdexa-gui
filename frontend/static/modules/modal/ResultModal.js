export function ResultModal() {
    this.open = () => {
        const modal = new bootstrap.Modal(document.getElementById("result-modal"));
        modal.show();
        return Promise.resolve(this);
    }

    return this;
}