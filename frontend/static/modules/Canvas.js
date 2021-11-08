export function Canvas(id, width, height) {
    this.canvas = document.getElementById(id);
    this.width = width;
    this.height = height;
    this.canvas.width = this.width;
    this.canvas.height = this.height;

    this.drawImage = (image) => {
        const element = new Image();
        element.src = URL.createObjectURL(image);
        const context = this.canvas.getContext("2d");
        return new Promise(resolve => {
            element.onload = event => { // Feuert hier das onload Event beim zweiten Neuzeichnen etwa doppelt?
                context.drawImage(event.target, 0, 0);
                resolve(this);
            };
        });
    }

    return this;
}


