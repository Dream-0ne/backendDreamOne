import { createStackNavigator } from 'react-navigation-stack';
// This file contains all the template code to fetch data from the flask app



// This method will return a json of the User occasions
async function getOccasions() {
  const url = 'http://localhost:5000/occasions'
  fetch(url)
  .then(response => response.json())  
  .then(json => {
      console.log(json);
  })
}
getOccasions();