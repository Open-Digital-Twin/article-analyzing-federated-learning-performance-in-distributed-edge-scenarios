const dockerHandler = require('./docker-handler.js')

observe = async () => {
    const nodes = ['ffremde01', 'ffremde02', 'ffremde03', 'ffremde-master'];
    const containerInfos = await dockerHandler.getAllContainerInfo(nodes);
    for (let containerInfo of containerInfos) {
        containerInfo.stats = await dockerHandler.getContainerStats(containerInfo.host, containerInfo.ID);
    }
    console.log(containerInfos);
}

module.exports = observe()
