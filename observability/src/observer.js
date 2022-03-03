const dockerService = require('./docker-service');

observe = async () => {
    const nodes = ['ffremde01', 'ffremde02', 'ffremde03', 'ffremde-master'];
    const containerInfos = await dockerService.getAllContainerInfo(nodes);
    for (const containerInfo of containerInfos) {
        const stats = await dockerService.getContainerStats(containerInfo.host, containerInfo.ID);
        containerInfo.stats.push(stats);
    }

    while(await anyContainerIsRunning()) {
        for (const containerInfo of containerInfos) {
            const stats = await dockerService.getContainerStats(containerInfo.host, containerInfo.ID);
            containerInfo.push(stats);
        }
        await sleep(2000);
    }

    console.log(containerInfos);
}

const anyContainerIsRunning = async () => {
    const containerInfos = await dockerService.getAllContainerInfo();
    return containerInfos.some(containerInfo => containerInfo.state === 'Running');
}

const sleep = (ms) => {
    return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports = observe();
