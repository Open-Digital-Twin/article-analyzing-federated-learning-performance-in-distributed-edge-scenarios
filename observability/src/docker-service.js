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
 * Retrieves an array of container information for every 
 * containers of the given nodes alongside their stats
 * @param {string[]} nodes - List of nodes.
 * @param {string} [port=2375] - Port to access node.
 * @returns {Promise<ContainerInfo[]>} containerInfos - List of container information with stats.
 */
exports.getAllContainersInfosWithStats = async (nodes, port) => {
    const containerInfos = await this.getAllContainersInfos(nodes, port);
    for (const containerInfo of containerInfos) {
        const stats = await this.getContainerStats(containerInfo.host, containerInfo.ID);
        containerInfo.stats = [stats];
    }

    return containerInfos;
}

/**
 * Retrieves an array of container information for every containers of the given nodes.
 * The stats are not retrieved, only the current information for the container.
 * @param {string[]} nodes - List of nodes.
 * @param {string} [port=2375] - Port to access node.
 * @returns {Promise<ContainerInfo[]>} containerInfos - List of container information.
 */
exports.getAllContainersInfos = async (nodes, port) => {
    const containerInfos = [];
    for (let node of nodes) {
        const defaultPort = '2375';
        const response = await sendGetRequest(`http://${node}:${port || defaultPort}/containers/json`);
        response.data.forEach(container => {
            containerInfos.push({
                ID: container.Id,
                host: node,
                image: getContainerImageName(container.Image),
                state: container.State,
                status: container.Status,
                stats: []
            });
        });
    }

    return containerInfos;
}

/**
 * Retrieves stats for a given container in a given host.
 * @param {string} id - ID of the container.
 * @param {string} host - Host node of the container.
 * @returns {Promise<Object>} containerStats - Stats of the container.
 */
exports.getContainerStats = async (host, id) => {
    const response = await sendGetRequest(`http://${host}:2375/containers/${id}/stats?stream=false`);
    return response.data;
}

const getContainerImageName = (image) => {
    const regex = /(?<=\:)(.*?)(?=\@)/;
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
