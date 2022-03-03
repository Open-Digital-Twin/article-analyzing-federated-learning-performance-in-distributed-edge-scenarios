const axios = require('axios');

/**
 * @typedef {Object} ContainerInfo
 * @property {string} containerInfos[].ID - The container ID.
 * @property {string} containerInfos[].host - The node hosting the container.
 * @property {string} containerInfos[].image - The name of the image.
 * @property {string} containerInfos[].state - The state of a container.
 * @property {string} containerInfos[].status - The status of a container.
 * @property {Object[]} containerInfos[].stats - Array of stats of a container.
 */

/**
 * Retrieves an array of container information for every containers of the given nodes
 * @param {string[]} nodes - List of nodes.
 * @returns {ContainerInfo[]} containerInfos - List of container information.
 */
exports.getAllContainerInfo = async (nodes) => {
    const containerInfos = []
    for (let node of nodes) {
        const response = await sendGetRequest(`http://${node}:2375/containers/json`);
        response.data.forEach(container => {
            containerInfos.push({
                ID: container.Id,
                host: node,
                image: getContainerImageName(container.Image),
                state: container.State,
                status: container.Status
            });
        });
    }

    return containerInfos;
}

/**
 * Retrieves stats for a given container in a given host.
 * @param {string} id - ID of the container.
 * @param {string} host - Host node of the container.
 * @returns {Object} containerStats - Stats of the container.
 */
exports.getContainerStats = async (host, id) => {
    const response = await sendGetRequest(`http://${host}:2375/containers/${id}/stats?stream=false`);
    return response.data.cpu_stats;
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
