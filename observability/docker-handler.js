const axios = require('axios');

const getAllContainers = () => {
    const nodes = ['ffremde01', 'ffremde02', 'ffremde03', 'ffremde-master'];
    let containerIds = [];
    nodes.forEach(node => {
        axios
        .get(`https://${node}:2375/containers/json`)
        .then(res => {
            res.forEach(container => containerIds.push(container.Id))
        })
        .catch(error => {
            console.error(error);
        })
    });

    console.log(containerIds);
    return containerIds;
}

module.exports = getAllContainers();