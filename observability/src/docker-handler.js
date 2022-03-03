const axios = require('axios');

exports.getAllContainerInfo = async() => {
    const containerInfo = []
    const nodes = ['ffremde01', 'ffremde02', 'ffremde03', 'ffremde-master'];
    for (let node of nodes) {
        const response = await sendGetRequest(`http://${node}:2375/containers/json`);
        response.data.forEach(container => {
            containerInfo.push({
                ID: container.Id,
                host: node,
                image: getContainerImageName(container.Image),
                state: container.State,
                status: container.Status,
                stats: null
            });
        });
    }

    return containerInfo;
}

/*
/ Adds the stats property to each container info object
/ containing the stats for the given container
*/
exports.getContainerStats = async(containerInfo) => {
    for (let container of containerInfo) {
        const stats = await sendGetRequest(`http://${container.host}:2375/containers/${container.ID}/stats?stream=false`);
        container.stats = stats.cpu_stats
    }
}

const getContainerImageName = (image) => {
    const regex = /(?<=\:)(.*?)(?=\@)/
    const found = image.match(regex);
    return found[0];
}

const sendGetRequest = async (url) => {
    try {
        const response = await axios.get(url);
        return response;
    } catch (err) {
        console.error(err);
    }
};
