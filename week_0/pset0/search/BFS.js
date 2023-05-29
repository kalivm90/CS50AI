class Queue {
    constructor() {
        this.items = [];
    }

    enqueue() {
        this.items.push(obj)
    }

    dequeue() {
        return this.items.shift()
    }

    isEmpty() {
        return this.items.length === 0
    }
}

const doBFS = (graph, source) => {
    const bfsInfo = []

    graph.forEach((i, index) => {
        bfsInfo[index] = {
            distance: null,
            predecessor: null,
        }
    })

    bfsInfo[source].distance = 0
    
    const queue = new Queue();
    queue.enqueue(source);

    console.log(queue.items)

    return bfsInfo
}

const adjList = [
    [1],
    [0, 4, 5],
    [3, 4, 5],
    [2, 6],
    [1, 2],
    [1, 2, 6],
    [3, 5],
    []
];

const bfsInfo = doBFS(adjList, 3);

// bfsInfo.forEach(i => {
//     console.log(`vertex ${i} distance = ${bfsInfo[i]?.distance} predecessor = ${bfsInfo[i]?.predecessor}`);
// })