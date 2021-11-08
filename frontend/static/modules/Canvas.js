export function Canvas() {
    this.drawImage = (blob, canvasId) => {
        const image = new Image();
        const imageSrc = URL.createObjectURL(blob);
        const canvas = document.getElementById(canvasId);
        canvas.width = 1900;
        canvas.height = 700;
        const context = canvas.getContext("2d");
        image.onload = event => context.drawImage(event.target, 0, 0);
        image.src = imageSrc;
        return canvas;
    }

    this.drawSelection = canvas => {
        
    }

    return this;
}


