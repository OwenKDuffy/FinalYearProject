const dublinBusClient = require('dublinbus-client');
const ObjectsToCsv = require('objects-to-csv')

var stops = dublinBusClient.busStop.getAllInformation()
  .then(async function(x) {
      // console.log("Running")
      // console.log(typeof x)
      let stopsArray = x.results;
      // console.log(stopsArray)
      let outputArray = [];
      stopsArray.forEach(function(stop) {
          let stopID = stop.stopid;
          let lat = stop.latitude;
          let long = stop.longitude;
          outputArray.push({
              StopID: stopID,
              Latitude: lat,
              Longitude: long
          });
          // console.log(outputArray.length)
      });
      // let csvContent = "data:text/csv;charset=utf-8," + outputArray.map(e => e.join(",")).join("\n");
      // console.log(outputArray)
      const csv = new ObjectsToCsv(outputArray);
      await csv.toDisk('./ProducedData/StopsCoordsJS.csv')
  })
  .catch(console.error);
