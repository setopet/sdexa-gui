/** @author Sebastian Peter (s.peter@tum.de) - student of computer science at TUM **/
/** Makes HTTP requests.
 * Status codes from the server indicating errors (e.g. 404) will lead to rejected promises. **/
export function HttpService() {
    this.get = url => {
        return request(url);
    }

    this.put = (url, data) => {
        return request(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
    }

    this.delete = (url) => {
        return request(url, {method: 'DELETE'});
    }

    this.downloadFile = (url, fileName) => {
        // Credits to https://stackoverflow.com/questions/32545632/how-can-i-download-a-file-using-window-fetch
        return request(url, { method: 'GET'})
            .then(response => response.blob())
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
        return request(route, {
            method: 'POST',
            body: data,
            contentType: 'multipart/form-data'
        });
    }

    /** Enable error management on status codes from the server indicating failures **/
    const request = (url, requestObject) => {
        return fetch(url, requestObject).then(response => {
            if (!response.ok) {
                return response.text().then(message => {
                    throw Error(message);
                });
            }
            return response;
        })
    }

    return this;
}