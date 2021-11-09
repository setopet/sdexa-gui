export function FileService() {
    'use strict';

    this.downloadFile = (url, fileName) => {
        // Credits to https://stackoverflow.com/questions/32545632/how-can-i-download-a-file-using-window-fetch
        return fetch(url, { method: 'GET'})
            .then(response => {
                if (!response.ok)
                    throw Error(response.statusText);
                return response.blob()
            })
            .then(blob => {
                const link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = fileName;
                document.body.appendChild(link);
                link.click();
                link.remove();
                return this;
            });
    }

    this.uploadFile = (file, route) => {
        const data = new FormData();
        data.append('file', file);
        return fetch(route, {
            method: 'POST',
            body: data
        });
    }

    this.getInputFile = field_id => {
        return document.querySelector(`input[id=${field_id}]`).files[0];
    }

    return this;
}