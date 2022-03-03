import { sleep } from 'time';
import * as dockerService from './docker-service.js';

observe = async () => {
    const nodes = ['ffremde01', 'ffremde02', 'ffremde03', 'ffremde-master'];
    const containerInfos = await dockerService.getAllContainerInfo(nodes);
    for (const containerInfo of containerInfos) {
        const stats = await dockerService.getContainerStats(containerInfo.host, containerInfo.ID);
        containerInfo.push(stats);
    }

    while(await anyContainerIsRunning()) {
        for (const containerInfo of containerInfos) {
            const stats = await dockerService.getContainerStats(containerInfo.host, containerInfo.ID);
            containerInfo.push(stats);
        }
        sleep(2);
    }

    console.log(containerInfos);
}

const anyContainerIsRunning = async () => {
    const containerInfos = await dockerService.getAllContainerInfo();
    return containerInfos.some(containerInfo => containerInfo.state === 'Running');
}

export default observe()
