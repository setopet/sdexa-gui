/** @author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM **/
import {baseUrl} from "./config.js";
import {SelectionCanvas} from "./canvas/SelectionCanvas.js";
import {LoadingAnimation} from "./LoadingAnimation.js";
import {SelectionModal} from "./modal/SelectionModal.js";
import {ResultModal} from "./modal/ResultModal.js";
import {ResultCanvas} from "./canvas/ResultCanvas.js";

/** Central control object, which is visible in the templates. **/
export function Controller(httpService, fileService, alertService) {
    const vm = this;

    vm.deleteImage = (route) => {
        httpService.delete(route)
            .then(reloadPage)
            .catch(alertService.error);
    }

    vm.switchImageView = (route) => {
        httpService.put(baseUrl + route)
            .then(reloadPage)
            .catch(alertService.error);
    }

    vm.downloadImage = (route, fileName) => {
        httpService
            .downloadFile(baseUrl + route, fileName)
            .catch(alertService.error);
    }

    vm.uploadScatter = (file) => {
        const animation = new LoadingAnimation("scatter-input-label");
        httpService
            .uploadFile(file, baseUrl + "surview/scatter")
            .then(() => getImage("surview"))
            .then(blob => initModalCanvas(blob, 50, 50))
            .then(animation.stop)
            .then(openSoftTissueSelectionModal)
            .catch(error => {
                animation.stop();
                alertService.error(error);
            });
    }

    vm.clickCalculate = () => {
        const animation = new LoadingAnimation("calculate-abmd-button");
        httpService.put("/surview/sdexa/calculation")
            .then(() => getImage("/surview/sdexa/bone-density-image"))
            .then(blob => {
                const resultCanvas = new ResultCanvas();
                return resultCanvas.drawImage(blob);
            })
            .then(() => httpService.getJson("/surview/sdexa/bone-density-results"))
            .then(results => {
                animation.stop();
                return new ResultModal(results["abmd_mean"], results["abmd_std"]).open();
            })
            .catch(error => {
                animation.stop();
                alertService.error(error);
            });
    }

    const openSoftTissueSelectionModal = () => {
        const selectionModal = new SelectionModal("Select the soft tissue ", {
            onFinish: () => putSelectionRegion("surview/sdexa/soft-tissue-region"),
            onAbort: () => httpService.delete("/surview/scatter"),
            onWindowChange: () => putImageWindow("surview"),
            onSelectionSizeChange: vm.modalCanvas.updateSelectionSize
        });
        selectionModal.defaultWindowFields("0", "2000");
        selectionModal.defaultSelectionSizeFields("50", "50");
        return selectionModal.open();
    }

    const putSelectionRegion = (route) => {
        const region = {
            posX: vm.modalCanvas.posX,
            posY: vm.modalCanvas.posY,
            dx: vm.modalCanvas.selectionSizeX,
            dy: vm.modalCanvas.selectionSizeY
        }
        return httpService.put(route, region)
            .then(reloadPage);
    }

    const uploadImage = (file, imageName, modalTitle) => {
        const animation = new LoadingAnimation(imageName + "-spinner");
        httpService.uploadFile(file, baseUrl + imageName)
            .then(() => getImage(imageName + "/full"))
            .then(blob => initModalCanvas(blob, 512, 512))
            .then(animation.stop)
            .then(() => openSelectionModal(imageName, modalTitle))
            .catch(error => {
                animation.stop();
                console.log(error);
                alertService.error(error);
            });
    }

    const putImageWindow = (route) => (windowMin, windowMax) => {
        httpService.put(baseUrl + route + "/window", { min: windowMin, max: windowMax })
            .then(() => getImage(route + "/full"))
            .then(vm.modalCanvas.updateImage)
    }

    const openSelectionModal = (imageName, title) => {
        const selectionModal = new SelectionModal(title, {
            onFinish: () => putSelectionRegion(baseUrl + imageName + "/position"),
            onAbort: () => vm.deleteImage(imageName),
            onWindowChange: putImageWindow(imageName),
            onSelectionSizeChange: vm.modalCanvas.updateSelectionSize
        });
        selectionModal.defaultSelectionSizeFields("512", "512");
        selectionModal.defaultWindowFields("0", "2000");
        return selectionModal.open();
    }

    const initModalCanvas = (blob, selectionSizeX, selectionSizeY) =>  {
        vm.modalCanvas = new SelectionCanvas(blob, selectionSizeX, selectionSizeY);
        return vm.modalCanvas.init();
    }

    const getImage = (route) => {
        return httpService.get(baseUrl + route)
            .then(response => response.blob())
    }

    const reloadPage = () => {
        location.href = '/';
        return Promise.resolve(this);
    }

    const init = () => {
        const surviewUploadCallback = file => uploadImage(file, "surview",
            "Move the rectangle by clicking on the surview image to select the area for segmenation. " +
            "Click the OK button when you are finished.");
        const projectionUploadCallback = file => uploadImage(file, "projection",
            "Move the rectangle by clicking on the projection image to select the area for registration. " +
            "Click the OK button when you are finished.");
        fileService.watchFileInput("surview-input", surviewUploadCallback);
        fileService.watchFileDrop("surview-drop", surviewUploadCallback);
        fileService.watchFileInput("projection-input", projectionUploadCallback);
        fileService.watchFileDrop("projection-drop", projectionUploadCallback);
        fileService.watchFileInput("scatter-input", vm.uploadScatter);
    }

    init();

    return vm;
}