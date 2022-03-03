const dockerHandler = require('./docker-handler.js')

observe = async () => {
    const containerInfo = await dockerHandler.getAllContainerInfo();
    const containerInfoWithStats = await dockerHandler.getContainerStats(containerInfo);
    console.log(containerInfo);
}

module.exports = observe()
