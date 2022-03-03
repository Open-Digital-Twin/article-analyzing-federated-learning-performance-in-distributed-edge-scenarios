const dockerHandler = require('./docker-handler.js')

observe = async () => {
    const containerInfo = await dockerHandler.getAllContainerInfo();
    console.log(containerInfo);
    const containerInfoWithStats = await dockerHandler.getContainerStats(containerInfo);
    console.log(containerInfo);
}

module.exports = observe()
