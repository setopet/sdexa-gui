/** @author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM **/
export function ResultModal() {
    this.open = () => {
        const modal = new bootstrap.Modal(document.getElementById("result-modal"));
        modal.show();
        return Promise.resolve(this);
    }

    return this;
}