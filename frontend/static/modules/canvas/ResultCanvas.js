/** @author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM **/
import {Canvas} from "./Canvas.js";
import {Pixel} from "./Pixel.js";

/** Manages a canvas element for obtaining information and segmentation from an image  **/
export function ResultCanvas(blob) {
    Canvas.call(this, "result-modal-canvas");
    this.segment = [];
    this.threshold = 10; // Threshold über Knopf einstellen

    this.watchMouseClick = (onClick) => {
            this.canvas.onclick = event => {
            const imageData = getImageDataFromMousePosition(event);
            if (imageData.value > this.threshold) {
                this.segmentClicked = true;
                markSegment(imageData.x, imageData.y, 1);
                onClick(this.segment);
            } else {
                this.segmentClicked = false;
                clearSegment();
                onClick(this.segment);
            }
        }
    }

    /** Watches mouse hover over the canvas and passes image information to
     * @param onHover **/
    this.watchMouseHover = (onHover) => {
        this.canvas.onmousemove = event => {
            const imageData = getImageDataFromMousePosition(event);
            if(!this.segmentClicked && imageData.value > this.threshold) {
                markSegment(imageData.x, imageData.y, 0.75);
            } else if(!this.segmentClicked && this.segment.length !== 0) {
                clearSegment();
            }
            onHover(imageData);
        }
    }

    const getImageDataFromMousePosition = mouseEvent => {
        const x = mouseEvent.offsetX;
        const y = mouseEvent.offsetY;
        const value = this.pixels[y][x].getValue();
        return {
            x: x,
            y: y,
            value: value
        };
    }

    const markSegment = (x, y, opacity) => {
        const context = this.canvas.getContext("2d");
        clearSegment();
        const segment = getSegment(y, x);  // offsetX and Y are counterintuitive, so we switch them
        for (let pixel of segment) {
            pixel.setYellow(this.imageData.data, opacity);
        }
        context.putImageData(this.imageData, 0, 0);
        this.segment = segment;
    }

    const clearSegment = () => {
        const context = this.canvas.getContext("2d");
        for (let pixel of this.segment) {
            pixel.setGrey(this.imageData.data);
        }
        context.putImageData(this.imageData, 0, 0);
        this.segment = [];
    }

    const getImageData = () => {
        const context = this.canvas.getContext("2d");
        return context.getImageData(0, 0, this.width, this.height);
    }

    const getPixels = (imageData) => {
        const pixels = new Array(this.height);
        for (let i = 0; i < pixels.length; i++) {
            pixels[i]  = new Array(this.width);
        }
        for (let i = 0; i < imageData.length; i+=4) {
            const pixel = i/4;
            const row = Math.floor(pixel/this.width);
            const column = pixel % this.width;
            pixels[row][column] = new Pixel(
                i, row, column, imageData[i], imageData[i+1], imageData[i+2], imageData[i+3]);
        }
        return pixels;
    }

    const getSegment = (posX, posY) => {
        const startPixel = this.pixels[posX][posY];
        const visited = new Set();
        const segment = [];
        const queue = [startPixel];
        while (queue.length !== 0) {
            const pixel = queue.pop();
            if(visited.has(pixel))
                continue;
            if (pixel.getValue() > this.threshold) {
                segment.push(pixel);
                const neighbors = getNeighbors(pixel);
                queue.push(...neighbors);
            }
            visited.add(pixel);
        }
        return segment;
    }

    const getNeighbors = (pixel) => {
        const neighbors = [];
        const x = pixel.getX();
        const y = pixel.getY();
        if (x > 0) {
            neighbors.push(this.pixels[x-1][y]);
            if(y > 0) {
                neighbors.push(this.pixels[x-1][y-1]);
            }
            if(y < this.pixels[0].length-1) {
                neighbors.push(this.pixels[x-1][y+1]);
            }
        }
        if (y > 0) {
            neighbors.push(this.pixels[x][y-1]);
        }
        if (y < this.pixels[0].length-1) {
            neighbors.push(this.pixels[x][y+1]);
        }

        if (x < this.pixels.length) {
            neighbors.push(this.pixels[x+1][y]);
            if (y > 0) {
                neighbors.push(this.pixels[x+1][y-1]);
            }
            if (y < this.pixels[0].length-1) {
                neighbors.push(this.pixels[x+1][y+1]);
            }
        }
        return neighbors;
    }

    this.init = () => {
        return this.drawImage(blob).then(() => {
            this.imageData = getImageData();
            this.pixels = getPixels(this.imageData.data);
            return this;
        })
    }

    return this;
}