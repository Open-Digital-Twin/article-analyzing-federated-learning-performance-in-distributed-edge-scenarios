const dockerService = require('./docker-service');
fs = require('fs');

const NODES = ['ffremde01', 'ffremde02', 'ffremde03', 'ffremde-master'];

observe = async () => {
    let containerInfos = await dockerService.getAllContainersInfosWithStats(NODES);

    while(anyContainerIsRunning(containerInfos)) {
        const containerInfosIds = containerInfos.map(containerInfo => containerInfo.ID);
        const updatedContainerInfos = await dockerService.getAllContainersInfosWithStats(NODES);
        const updatedContainerInfosIds = updatedContainerInfos.map(updatedContainerInfo => updatedContainerInfo.ID);

        updatedContainerInfos.forEach(updatedContainerInfo => {
            // If container already retrieved, only update the State,
            // Status, and push the retrieved Stats to the array.
            // Else it's a new container, then add it to the containerInfos list.
            if (containerInfosIds.includes(updatedContainerInfo.ID)) {
                containerInfos.forEach(containerInfo => {
                    if (containerInfo.ID === updatedContainerInfo.ID) {
                        containerInfo.state = updatedContainerInfo.state;
                        containerInfo.status = updatedContainerInfo.status;
                        containerInfo.stats.push(updatedContainerInfo.stats);
                    }
                })
            } else {
                containerInfos.push(updatedContainerInfo);
            }
        })

        // If there is a container in containerInfo which hasn't been retrieved,
        // it means the container stopped. Therefore, we can persist its stats
        // and remove it from the list
        containerInfos.forEach((containerInfo, index) => {
            if (!updatedContainerInfosIds.includes(containerInfo.ID)) {
                console.info(containerInfo);
                containerInfos.splice(index, 1);
            }
        })

        await sleep(5000);
    }
}

const anyContainerIsRunning = (containerInfos) => {
    return containerInfos.some(containerInfo => containerInfo.state === 'running');
}

const sleep = (ms) => {
    return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports = observe();
