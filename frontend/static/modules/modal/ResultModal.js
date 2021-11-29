/** @author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM **/
export function ResultModal(bone_density_mean, bone_density_std) {
    document.getElementById("abmd-mean-cell").innerText = bone_density_mean;
    document.getElementById("abmd-std-cell").innerText = bone_density_std;

    this.open = () => {
        const modal = new bootstrap.Modal(document.getElementById("result-modal"));
        modal.show();
        return Promise.resolve(this);
    }

    return this;
}