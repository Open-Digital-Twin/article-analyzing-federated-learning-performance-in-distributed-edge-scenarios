const axios = require('axios');

exports.getAllContainers = async () => {
    const nodes = ['ffremde01', 'ffremde02', 'ffremde03', 'ffremde-master'];
    let containerIds = [];
    for (let node of nodes) {
        const response = await sendGetRequest(`http://${node}:2375/containers/json`);
	response.data.forEach(container => containerIds.push(container.Id))
    }

    return containerIds;
}

const sendGetRequest = async (url) => {
    try {
        const response = await axios.get(url);
        return response;
    } catch (err) {
        console.error(err);
    }
};
