

// data points
var data = [
    [2, 10],
    [2, 5],
    [8, 4],
    [5, 8],
    [7, 5],
    [6, 4],
    [1, 2],
    [4, 9]
]


// could be set by the user
const numberOfClusters = 3;

// initialise clusters
var clusters = {};

for(var i=1; i <= numberOfClusters; i++){
    clusters[i] = [];
}

// specified centroids: could be set by the user as well
var centroids = [[2,10], [5, 8], [1,2]]



function kMeans() {

    // Iteration 1: Group the points into clusters
    for(point of data){
        let distances = []

        for (centroid of centroids){
            
            let dist = euclideanDistance(centroid, point)
            distances.push(parseFloat(dist))
        }

        // get the index of the minimum distance
        const clusterNumber = getClusterNumber(distances)

        // put the point in the cluster it belongs to
        clusters[clusterNumber].push(point);

    }

    

    // At the end of each iteration, update centroids
    for(var i=0; i<centroids.length; i++){
        const cluster = clusters[i+1]

        // compute the centroid for the cluster
        const centroid = computeCentroids(cluster)
        
        centroids[i] = centroid;
    }

    console.log(clusters)

    // reset clusters
    clusters = {};
    for(var i=1; i <= numberOfClusters; i++){
        clusters[i] = [];
    }

    
}



// calculate the euclidean distance
const euclideanDistance = function(vectorA, vectorB){
    const distances = []

    for (let i=0; i < vectorA.length; i++){
        let miniDistance = (vectorA[i] - vectorB[i])**2
        distances.push(miniDistance)
    }

    const totalDistance = distances.reduce((acc, curr) =>  acc + curr );

    const eucDist = Math.sqrt(totalDistance).toFixed(2)
    
    return eucDist

}


const getClusterNumber = function(vector){
    // find the minimum number in the vector
    const minimum = Math.min(...vector);

    // find the index of the minimum number
    const clusterNumber = vector.indexOf(minimum) + 1

    return clusterNumber.toString();
}


/* This function takes a vector of vectors*/
const computeCentroids = function(vecOfVectors){

    const meanVector = []

    // check the dimensionality of each tuple
    const dimensionality = vecOfVectors[0].length;

    // get all the X-values

    for (let i=0; i < dimensionality; i++){
        const coordinates = []
        for (point of vecOfVectors){
            coordinates.push(point[i])
        }

        // calculate the mean
        const sumOfCoordinates = coordinates.reduce((acc, curr) => acc + curr)
        const meanOfCoordinates = sumOfCoordinates/vecOfVectors.length;

        // push the mean of the coordinate
        meanVector.push(parseFloat(meanOfCoordinates.toFixed(1)));

    }

    return meanVector;
}

kMeans();