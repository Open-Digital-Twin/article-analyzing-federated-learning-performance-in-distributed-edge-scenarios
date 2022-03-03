const dockerHandler = require('./docker-handler.js')

main = async () => {
    const containerIds = await dockerHandler.getAllContainers()
    console.log(containerIds)
}

module.exports = main()
